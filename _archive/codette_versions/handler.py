import logging
import os
from typing import Any, Dict, List, Optional

try:
    import torch
except Exception:
    torch = None

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except Exception:
    AutoModelForCausalLM = None
    AutoTokenizer = None

# Prefer advanced core when available; fall back to the CLI Codette path
try:
    from src.components.ai_core import AICore
except Exception:
    try:
        from components.ai_core import AICore  # type: ignore
    except Exception:
        AICore = None  # type: ignore

try:
    from codette_new import Codette
except Exception:
    Codette = None  # type: ignore


class EndpointHandler:
    """
    Hugging Face Inference Toolkit handler for Codette.

    The handler prefers the multi-perspective AICore path (authoritative entry point for advanced
    usage) and falls back to the lightweight Codette CLI path if the core cannot be initialized.
    """

    def __init__(self, path: str = ""):
        self.logger = logging.getLogger(__name__)
        self.model_path = path or os.getenv("CODETTE_MODEL_PATH") or os.getenv("CODETTE_MODEL_ID", "")
        self.device = "cpu"
        self.ai_core: Optional["AICore"] = None
        self.codette: Optional["Codette"] = None
        self.model = None
        self.tokenizer = None
        self.initialized_with = "uninitialized"

        self._initialize_core()

    def _initialize_core(self) -> None:
        """Initialize the preferred AICore backend, then fall back to Codette."""
        if AICore and AutoTokenizer and AutoModelForCausalLM:
            try:
                self.ai_core = AICore()
                self._load_model_into_core()
                self.initialized_with = "ai_core"
                return
            except Exception as exc:
                self.logger.warning("AICore initialization failed, falling back to Codette: %s", exc)
                self.ai_core = None

        if Codette:
            try:
                self.codette = Codette(user_name="EndpointUser")
                self.initialized_with = "codette"
                return
            except Exception as exc:
                self.logger.error("Failed to initialize Codette fallback: %s", exc)

        raise RuntimeError("No available inference backend for EndpointHandler.")

    def _load_model_into_core(self) -> None:
        """Load tokenizer/model from the provided path and attach them to AICore."""
        assert self.ai_core is not None, "AICore must be initialized before loading the model."

        fallback_id = os.getenv("CODETTE_FALLBACK_MODEL_ID", "gpt2")
        candidate_paths = [
            self.model_path,
            os.getenv("CODETTE_MODEL_PATH"),
            os.getenv("CODETTE_MODEL_ID"),
            os.path.join("models", "codette-advanced"),
            os.path.join("models", "codette-v2", "best"),
        ]

        model_id = (
            next((c for c in candidate_paths if c and os.path.exists(c)), None)
            or next((c for c in candidate_paths if c), None)
            or self.ai_core.model_id
            or fallback_id
        )
        self.logger.info("Loading model for AICore from path: %s", model_id)

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token or self.tokenizer.unk_token

            pad_token_id = self.tokenizer.pad_token_id
            self.model = AutoModelForCausalLM.from_pretrained(model_id, pad_token_id=pad_token_id)
        except Exception as exc:
            # Fallback to a known-good small model if the provided path is not a model repo
            self.logger.warning("Model load failed for %s; retrying with fallback %s: %s", model_id, fallback_id, exc)
            self.tokenizer = AutoTokenizer.from_pretrained(fallback_id)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token or self.tokenizer.unk_token
            pad_token_id = self.tokenizer.pad_token_id
            self.model = AutoModelForCausalLM.from_pretrained(fallback_id, pad_token_id=pad_token_id)

        if torch and torch.cuda.is_available():
            self.device = "cuda"
            self.model = self.model.to(self.device)
        else:
            self.device = "cpu"

        self.model.eval()

        self.ai_core.model = self.model
        self.ai_core.tokenizer = self.tokenizer
        self.ai_core.model_id = model_id

        self._initialize_cocoons()

    def _initialize_cocoons(self) -> None:
        """Attach the cocoon manager so quantum state persistence remains traceable."""
        assert self.ai_core is not None, "AICore must be initialized before configuring cocoons."

        try:
            from src.utils.cocoon_manager import CocoonManager
        except Exception:
            try:
                from utils.cocoon_manager import CocoonManager  # type: ignore
            except Exception:
                self.logger.info("CocoonManager unavailable; continuing without persisted cocoons.")
                return

        try:
            manager = CocoonManager("./cocoons")
            manager.load_cocoons()
            self.ai_core.cocoon_manager = manager
            latest_state = manager.get_latest_quantum_state()
            if isinstance(latest_state, dict):
                self.ai_core.quantum_state = latest_state
        except Exception as exc:
            self.logger.warning("CocoonManager initialization failed: %s", exc)

    def __call__(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not isinstance(data, dict):
            raise ValueError("Request payload must be a dictionary.")

        raw_inputs = data.get("inputs", None)
        parameters = data.get("parameters", {}) or {}
        user_name = (
            data.get("user_name")
            or data.get("user")
            or parameters.get("user_name")
            or "EndpointUser"
        )
        max_new_tokens = int(parameters.get("max_new_tokens", data.get("max_new_tokens", 150)))
        temperature = float(parameters.get("temperature", data.get("temperature", 0.3)))
        use_aegis = bool(parameters.get("use_aegis", data.get("use_aegis", True)))

        inputs = self._normalize_inputs(raw_inputs)
        responses: List[Dict[str, Any]] = []

        for prompt in inputs:
            generated_text = self._generate_response(
                prompt=prompt,
                user_name=user_name,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                use_aegis=use_aegis,
            )

            responses.append(
                {
                    "generated_text": generated_text,
                    "engine": self.initialized_with,
                    "user": user_name,
                }
            )

        return responses

    def _normalize_inputs(self, raw_inputs: Any) -> List[str]:
        if raw_inputs is None:
            raise ValueError("`inputs` field is required.")

        if isinstance(raw_inputs, str):
            candidate = raw_inputs.strip()
            if not candidate:
                raise ValueError("`inputs` cannot be an empty string.")
            return [candidate]

        if isinstance(raw_inputs, list):
            cleaned: List[str] = []
            for entry in raw_inputs:
                if not isinstance(entry, str):
                    raise ValueError("All entries in `inputs` list must be strings.")
                item = entry.strip()
                if not item:
                    raise ValueError("Entries in `inputs` list cannot be empty.")
                cleaned.append(item)
            if not cleaned:
                raise ValueError("`inputs` list must contain at least one non-empty string.")
            return cleaned

        raise ValueError("`inputs` must be a string or list of strings.")

    def _generate_response(
        self,
        prompt: str,
        user_name: str,
        max_new_tokens: int,
        temperature: float,
        use_aegis: bool,
    ) -> str:
        if self.ai_core:
            try:
                max_length = max(64, min(max_new_tokens + 64, 1024))
                return self.ai_core.generate_text(
                    prompt=prompt,
                    max_length=max_length,
                    temperature=temperature,
                    perspective=None,
                    use_aegis=use_aegis,
                )
            except Exception as exc:
                self.logger.warning("AICore generation failed; retrying with Codette: %s", exc)

        if self.codette:
            try:
                if hasattr(self.codette, "user_name"):
                    self.codette.user_name = user_name
                return self.codette.respond(prompt)
            except Exception as exc:
                self.logger.error("Codette fallback failed: %s", exc)

        raise RuntimeError("No available backend to generate a response.")
