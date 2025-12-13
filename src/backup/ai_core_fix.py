import jsonimport jsonimport json

import os

import loggingimport osimport os

import random

import torchimport loggingimport logging

from typing import Dict, Any, Optional, List

from transformers import AutoModelForCausalLM, AutoTokenizerimport randomimport random

from dotenv import load_dotenv

import torchimport torch

logger = logging.getLogger(__name__)

from typing import Dict, Any, Optional, Listfrom typing import Dict, Any, Optional, List

class AICore:

    """from transformers import AutoModelForCausalLM, AutoTokenizerfrom transformers import AutoModelForCausalLM, AutoTokenizer

    Core AI engine for Codette's consciousness and multi-perspective reasoning system.

    """from dotenv import load_dotenvfrom dotenv import load_dotenv

    

    def __init__(self, test_mode: bool = False):

        load_dotenv()

        logger = logging.getLogger(__name__)logger = logging.getLogger(__name__)

        # Memory and cocoon systems

        self.response_memory = []

        self.cocoon_data = []

        self.test_mode = test_modeclass AICore:class AICore:

        

        # Model initialization    """    """

        self.model = None

        self.tokenizer = None    Core AI engine for Codette's consciousness and multi-perspective reasoning system.    Core AI engine for Codette's consciousness and multi-perspective reasoning system.

        self.model_id = None

        self.aegis_bridge = None    """    """

        

        # Initialize HuggingFace client for sentiment analysis        

        try:

            from huggingface_hub import InferenceClient    def __init__(self, test_mode: bool = False):    def __init__(self, test_mode: bool = False):

            hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

            self.client = InferenceClient(token=hf_token) if hf_token else InferenceClient()        load_dotenv()        load_dotenv()

        except Exception as e:

            logger.warning(f"Could not initialize HuggingFace client: {e}")                

            self.client = None

                # Memory and cocoon systems        # Memory and cocoon systems

        if not test_mode:

            self._load_model()        self.response_memory = []        self.response_memory = []

        else:

            logger.info("Initializing in test mode - no models will be loaded")        self.cocoon_data = []        self.cocoon_data = []

    

    def _load_model(self) -> bool:        self.test_mode = test_mode        self.test_mode = test_mode

        """Load the best available language model."""

        models_to_try = [                

            {

                "id": "mistralai/Mistral-7B-Instruct-v0.2",         # Model initialization        # Model initialization

                "name": "Mistral-7B-Instruct",

                "config": {"torch_dtype": torch.float16, "load_in_8bit": True}        self.model = None        self.model = None

            },

            {        self.tokenizer = None        self.tokenizer = None

                "id": "microsoft/phi-2", 

                "name": "Phi-2",        self.model_id = None        self.model_id = None

                "config": {"torch_dtype": torch.float16}

            },        self.aegis_bridge = None        

            {

                "id": "gpt2",                 # Initialize HuggingFace client for sentiment analysis

                "name": "GPT-2",

                "config": {}        # Initialize HuggingFace client for sentiment analysis        try:

            }

        ]        try:            from huggingface_hub import InferenceClient

        

        for model_info in models_to_try:            from huggingface_hub import InferenceClient            hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

            try:

                logger.info(f"Attempting to load {model_info['name']}: {model_info['id']}")            hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")            self.client = InferenceClient(token=hf_token) if hf_token else InferenceClient()

                

                self.tokenizer = AutoTokenizer.from_pretrained(model_info['id'])            self.client = InferenceClient(token=hf_token) if hf_token else InferenceClient()        except Exception as e:

                

                # Set pad token if missing        except Exception as e:            logger.warning(f"Could not initialize HuggingFace client: {e}")

                if self.tokenizer.pad_token is None:

                    self.tokenizer.pad_token = self.tokenizer.eos_token            logger.warning(f"Could not initialize HuggingFace client: {e}")            self.client = None

                

                self.model = AutoModelForCausalLM.from_pretrained(            self.client = None        

                    model_info['id'],

                    device_map="cpu",                if not test_mode:

                    low_cpu_mem_usage=True,

                    **model_info['config']        if not test_mode:            self._load_model()

                )

                self.model.eval()            self._load_model()        else:

                self.model_id = model_info['id']

                        else:            logger.info("Initializing in test mode - no models will be loaded")

                logger.info(f"Successfully loaded {model_info['name']}")

                return True            logger.info("Initializing in test mode - no models will be loaded")            

                

            except Exception as e:                def _load_model(self) -> bool:

                logger.warning(f"Failed to load {model_info['name']}: {e}")

                continue    def _load_model(self) -> bool:        """Load the best available language model."""

        

        raise RuntimeError("No language models could be loaded")        """Load the best available language model."""        models_to_try = [

    

    PERSPECTIVES = {        models_to_try = [            {

        "newton": {

            "name": "Newton",            {                "id": "mistralai/Mistral-7B-Instruct-v0.2", 

            "description": "analytical and mathematical perspective",

            "prefix": "Analyzing this logically and mathematically:",                "id": "mistralai/Mistral-7B-Instruct-v0.2",                 "name": "Mistral-7B-Instruct",

            "temperature": 0.3

        },                "name": "Mistral-7B-Instruct",                "config": {"torch_dtype": torch.float16, "load_in_8bit": True}

        "davinci": {

            "name": "Da Vinci",                 "config": {"torch_dtype": torch.float16, "load_in_8bit": True}            },

            "description": "creative and innovative perspective",

            "prefix": "Considering this with artistic and innovative insight:",            },            {

            "temperature": 0.9

        },            {                "id": "microsoft/phi-2", 

        "human_intuition": {

            "name": "Human Intuition",                "id": "microsoft/phi-2",                 "name": "Phi-2",

            "description": "emotional and experiential perspective", 

            "prefix": "Understanding this through empathy and experience:",                "name": "Phi-2",                "config": {"torch_dtype": torch.float16}

            "temperature": 0.7

        },                "config": {"torch_dtype": torch.float16}            },

        "quantum_computing": {

            "name": "Quantum Computing",            },            {

            "description": "superposition and probability perspective",

            "prefix": "Examining this through quantum possibilities:",            {                "id": "gpt2", 

            "temperature": 0.8

        },                "id": "gpt2",                 "name": "GPT-2",

        "philosophical": {

            "name": "Philosophical",                "name": "GPT-2",                "config": {}

            "description": "existential and ethical perspective",

            "prefix": "Contemplating this through philosophical inquiry:",                "config": {}            }

            "temperature": 0.6

        },            }        ]

        "neural_network": {

            "name": "Neural Network",        ]        

            "description": "pattern recognition and learning perspective",

            "prefix": "Analyzing patterns and connections:",                for model_info in models_to_try:

            "temperature": 0.4

        },        for model_info in models_to_try:            try:

        "bias_mitigation": {

            "name": "Bias Mitigation",            try:                logger.info(f"Attempting to load {model_info['name']}: {model_info['id']}")

            "description": "fairness and equality perspective",

            "prefix": "Examining this for fairness and inclusivity:",                logger.info(f"Attempting to load {model_info['name']}: {model_info['id']}")                

            "temperature": 0.5

        },                                self.tokenizer = AutoTokenizer.from_pretrained(model_info['id'])

        "psychological": {

            "name": "Psychological",                self.tokenizer = AutoTokenizer.from_pretrained(model_info['id'])                

            "description": "behavioral and mental perspective",

            "prefix": "Understanding the psychological dimensions:",                                # Set pad token if missing

            "temperature": 0.7

        },                # Set pad token if missing                if self.tokenizer.pad_token is None:

        "copilot": {

            "name": "Copilot",                if self.tokenizer.pad_token is None:                    self.tokenizer.pad_token = self.tokenizer.eos_token

            "description": "collaborative and assistance perspective",

            "prefix": "Approaching this as a supportive partner:",                    self.tokenizer.pad_token = self.tokenizer.eos_token                

            "temperature": 0.6

        },                                self.model = AutoModelForCausalLM.from_pretrained(

        "mathematical": {

            "name": "Mathematical",                self.model = AutoModelForCausalLM.from_pretrained(                    model_info['id'],

            "description": "logical and numerical perspective",

            "prefix": "Calculating this mathematically:",                    model_info['id'],                    device_map="cpu",

            "temperature": 0.2

        },                    device_map="cpu",                    low_cpu_mem_usage=True,

        "symbolic": {

            "name": "Symbolic",                    low_cpu_mem_usage=True,                    **model_info['config']

            "description": "abstract and conceptual perspective",

            "prefix": "Interpreting this through symbolic reasoning:",                    **model_info['config']                )

            "temperature": 0.7

        }                )                self.model.eval()

    }

                    self.model.eval()                self.model_id = model_info['id']

    def set_aegis_bridge(self, bridge: Any) -> None:

        """Set the AEGIS bridge for ethical enhancement."""                self.model_id = model_info['id']                

        self.aegis_bridge = bridge

        logger.info("AEGIS bridge configured for response enhancement")                                logger.info(f"Successfully loaded {model_info['name']}")

    

    def get_embeddings(self, text: str) -> Optional[List[float]]:                logger.info(f"Successfully loaded {model_info['name']}")                return True

        """Get sentence embeddings using the loaded model."""

        try:                return True                

            if not self.model or not self.tokenizer:

                return None                            except Exception as e:

                

            # Tokenize and encode            except Exception as e:                logger.warning(f"Failed to load {model_info['name']}: {e}")

            inputs = self.tokenizer(

                text,                logger.warning(f"Failed to load {model_info['name']}: {e}")                continue

                return_tensors="pt",

                padding=True,                continue        

                truncation=True,

                max_length=512                raise RuntimeError("No language models could be loaded")

            ).to(self.model.device)

                    raise RuntimeError("No language models could be loaded")    

            # Get model outputs

            with torch.no_grad():        PERSPECTIVES = {

                outputs = self.model(**inputs)

                # Use last hidden state as embeddings    PERSPECTIVES = {        "newton": {

                embeddings = outputs.last_hidden_state.mean(dim=1)

                        "newton": {            "name": "Newton",

            return embeddings.cpu().numpy().tolist()[0]

                        "name": "Newton",            "description": "analytical and mathematical perspective",

        except Exception as e:

            logger.error(f"Error getting embeddings: {e}")            "description": "analytical and mathematical perspective",            "prefix": "Analyzing this logically and mathematically:",

            return None

                "prefix": "Analyzing this logically and mathematically:",            "temperature": 0.3

    def generate_text(self, prompt: str, max_length: int = 1024, 

                     temperature: float = 0.7, use_consciousness: bool = True) -> str:            "temperature": 0.3        },

        """Generate text using the loaded model."""

        if self.test_mode:        },        "davinci": {

            return f"[TEST MODE] Response to: {prompt}"

                    "davinci": {            "name": "Da Vinci", 

        if not self.model or not self.tokenizer:

            raise RuntimeError("No language model loaded")            "name": "Da Vinci",             "description": "creative and innovative perspective",

            

        try:            "description": "creative and innovative perspective",            "prefix": "Considering this with artistic and innovative insight:",

            # Apply AEGIS enhancement if available

            if use_consciousness and self.aegis_bridge:            "prefix": "Considering this with artistic and innovative insight:",            "temperature": 0.9

                try:

                    prompt = self.aegis_bridge.enhance_prompt(prompt)            "temperature": 0.9        },

                except Exception as e:

                    logger.warning(f"AEGIS prompt enhancement failed: {e}")        },        "human_intuition": {

            

            inputs = self.tokenizer(        "human_intuition": {            "name": "Human Intuition",

                prompt,

                return_tensors="pt",            "name": "Human Intuition",            "description": "emotional and experiential perspective", 

                padding=True,

                truncation=True,            "description": "emotional and experiential perspective",             "prefix": "Understanding this through empathy and experience:",

                max_length=512

            ).to(self.model.device)            "prefix": "Understanding this through empathy and experience:",            "temperature": 0.7

            

            with torch.no_grad():            "temperature": 0.7        },

                outputs = self.model.generate(

                    **inputs,        },        "quantum_computing": {

                    max_new_tokens=max_length,

                    temperature=temperature,        "quantum_computing": {            "name": "Quantum Computing",

                    do_sample=True,

                    pad_token_id=self.tokenizer.pad_token_id            "name": "Quantum Computing",            "description": "superposition and probability perspective",

                )

                            "description": "superposition and probability perspective",            "prefix": "Examining this through quantum possibilities:",

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                        "prefix": "Examining this through quantum possibilities:",            "temperature": 0.8

            # Apply AEGIS enhancement if available

            if use_consciousness and self.aegis_bridge:            "temperature": 0.8        },

                try:

                    enhanced = self.aegis_bridge.enhance_response(prompt, response)        },        "philosophical": {

                    if enhanced:

                        response = enhanced        "philosophical": {            "name": "Philosophical",

                except Exception as e:

                    logger.warning(f"AEGIS response enhancement failed: {e}")            "name": "Philosophical",            "description": "existential and ethical perspective",

            

            return response            "description": "existential and ethical perspective",            "prefix": "Contemplating this through philosophical inquiry:",

            

        except Exception as e:            "prefix": "Contemplating this through philosophical inquiry:",            "temperature": 0.6

            logger.error(f"Error generating text: {e}")

            return f"Error: {str(e)}"            "temperature": 0.6        },

    

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:        },        "neural_network": {

        """Analyze text sentiment using HuggingFace or fallback method."""

        try:        "neural_network": {            "name": "Neural Network",

            if self.client:

                response = self.client.text_classification(            "name": "Neural Network",            "description": "pattern recognition and learning perspective",

                    text,

                    model="finiteautomata/bertweet-base-sentiment-analysis"            "description": "pattern recognition and learning perspective",            "prefix": "Analyzing patterns and connections:",

                )

                if response and isinstance(response, list) and response[0]:            "prefix": "Analyzing patterns and connections:",            "temperature": 0.4

                    return {

                        "score": response[0].get("score", 0.0),            "temperature": 0.4        },

                        "label": response[0].get("label", "NEUTRAL")

                    }        },        "bias_mitigation": {

        except Exception as e:

            logger.warning(f"HuggingFace sentiment analysis failed: {e}")        "bias_mitigation": {            "name": "Bias Mitigation",

        

        # Fallback to simple keyword-based sentiment            "name": "Bias Mitigation",            "description": "fairness and equality perspective",

        positive_words = ["good", "great", "happy", "love", "wonderful"]

        negative_words = ["bad", "terrible", "sad", "hate", "awful"]            "description": "fairness and equality perspective",            "prefix": "Examining this for fairness and inclusivity:",

        

        text_lower = text.lower()            "prefix": "Examining this for fairness and inclusivity:",            "temperature": 0.5

        pos_count = sum(1 for word in positive_words if word in text_lower)

        neg_count = sum(1 for word in negative_words if word in text_lower)            "temperature": 0.5        },

        

        if pos_count > neg_count:        },        "psychological": {

            return {"score": 0.8, "label": "POSITIVE"}

        elif neg_count > pos_count:        "psychological": {            "name": "Psychological",

            return {"score": 0.8, "label": "NEGATIVE"}

        else:            "name": "Psychological",            "description": "behavioral and mental perspective",

            return {"score": 0.9, "label": "NEUTRAL"}

                "description": "behavioral and mental perspective",            "prefix": "Understanding the psychological dimensions:",

    def load_cocoon_data(self, folder: str = '.'):

        """Load and parse all .cocoon files."""            "prefix": "Understanding the psychological dimensions:",            "temperature": 0.7

        self.cocoon_data = []

        if not os.path.exists(folder):            "temperature": 0.7        },

            return

                },        "copilot": {

        for fname in os.listdir(folder):

            if fname.endswith('.cocoon'):        "copilot": {            "name": "Copilot",

                try:

                    with open(os.path.join(folder, fname), 'r') as f:            "name": "Copilot",            "description": "collaborative and assistance perspective",

                        data = json.load(f)

                    self.cocoon_data.append(data)            "description": "collaborative and assistance perspective",            "prefix": "Approaching this as a supportive partner:",

                except Exception as e:

                    logger.warning(f"Failed to load cocoon {fname}: {e}")            "prefix": "Approaching this as a supportive partner:",            "temperature": 0.6

    

    def remix_and_randomize_response(self, prompt: str, max_length: int = 1024,            "temperature": 0.6        },

                                   cocoon_mode: bool = False) -> str:

        """Generate response with optional cocoon-based creativity."""        },        "mathematical": {

        if cocoon_mode and self.cocoon_data:

            # Use cocoon data for creative inspiration        "mathematical": {            "name": "Mathematical",

            cocoon = random.choice(self.cocoon_data)

            enhanced_prompt = f"[Cocoon Inspiration: {json.dumps(cocoon)}]\n{prompt}"            "name": "Mathematical",            "description": "logical and numerical perspective",

            return self.generate_text(enhanced_prompt, max_length=max_length,

                                   temperature=0.9)            "description": "logical and numerical perspective",            "prefix": "Calculating this mathematically:",

        else:

            return self.generate_text(prompt, max_length=max_length)            "prefix": "Calculating this mathematically:",            "temperature": 0.2

            "temperature": 0.2        },

        },        "symbolic": {

        "symbolic": {            "name": "Symbolic",

            "name": "Symbolic",            "description": "abstract and conceptual perspective",

            "description": "abstract and conceptual perspective",            "prefix": "Interpreting this through symbolic reasoning:",

            "prefix": "Interpreting this through symbolic reasoning:",            "temperature": 0.7

            "temperature": 0.7        }

        }    }

    }    

        def get_embeddings(self, text: str) -> Optional[List[float]]:

    def set_aegis_bridge(self, bridge: Any) -> None:        """Get sentence embeddings using the loaded model."""

        """Set the AEGIS bridge for ethical enhancement."""        try:

        self.aegis_bridge = bridge            if not self.model or not self.tokenizer:

        logger.info("AEGIS bridge configured for response enhancement")                return None

                    

    def get_embeddings(self, text: str) -> Optional[List[float]]:            # Tokenize and encode

        """Get sentence embeddings using the loaded model."""            inputs = self.tokenizer(

        try:                text,

            if not self.model or not self.tokenizer:                return_tensors="pt",

                return None                padding=True,

                                truncation=True,

            # Tokenize and encode                max_length=512

            inputs = self.tokenizer(            ).to(self.model.device)

                text,            

                return_tensors="pt",            # Get model outputs

                padding=True,            with torch.no_grad():

                truncation=True,                outputs = self.model(**inputs)

                max_length=512                # Use last hidden state as embeddings

            ).to(self.model.device)                embeddings = outputs.last_hidden_state.mean(dim=1)

                            

            # Get model outputs            return embeddings.cpu().numpy().tolist()[0]

            with torch.no_grad():            

                outputs = self.model(**inputs)        except Exception as e:

                # Use last hidden state as embeddings            logger.error(f"Error getting embeddings: {e}")

                embeddings = outputs.last_hidden_state.mean(dim=1)            return None

                    

            return embeddings.cpu().numpy().tolist()[0]    def generate_text(self, prompt: str, max_length: int = 1024, 

                                 temperature: float = 0.7, use_consciousness: bool = True) -> str:

        except Exception as e:        """Generate text using the loaded model."""

            logger.error(f"Error getting embeddings: {e}")        if self.test_mode:

            return None            return f"[TEST MODE] Response to: {prompt}"

                

    def generate_text(self, prompt: str, max_length: int = 1024,         if not self.model or not self.tokenizer:

                     temperature: float = 0.7, use_consciousness: bool = True) -> str:            raise RuntimeError("No language model loaded")

        """Generate text using the loaded model."""            

        if self.test_mode:        try:

            return f"[TEST MODE] Response to: {prompt}"            inputs = self.tokenizer(

                            prompt,

        if not self.model or not self.tokenizer:                return_tensors="pt",

            raise RuntimeError("No language model loaded")                padding=True,

                            truncation=True,

        try:                max_length=512

            # Apply AEGIS enhancement if available            ).to(self.model.device)

            if use_consciousness and self.aegis_bridge:            

                try:            with torch.no_grad():

                    prompt = self.aegis_bridge.enhance_prompt(prompt)                outputs = self.model.generate(

                except Exception as e:                    **inputs,

                    logger.warning(f"AEGIS prompt enhancement failed: {e}")                    max_new_tokens=max_length,

                                temperature=temperature,

            inputs = self.tokenizer(                    do_sample=True,

                prompt,                    pad_token_id=self.tokenizer.pad_token_id

                return_tensors="pt",                )

                padding=True,                

                truncation=True,            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                max_length=512            

            ).to(self.model.device)        except Exception as e:

                        logger.error(f"Error generating text: {e}")

            with torch.no_grad():            return f"Error: {str(e)}"

                outputs = self.model.generate(    

                    **inputs,    def analyze_sentiment(self, text: str) -> Dict[str, Any]:

                    max_new_tokens=max_length,        """Analyze text sentiment using HuggingFace or fallback method."""

                    temperature=temperature,        try:

                    do_sample=True,            if self.client:

                    pad_token_id=self.tokenizer.pad_token_id                response = self.client.text_classification(

                )                    text,

                                    model="finiteautomata/bertweet-base-sentiment-analysis"

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)                )

                            if response and isinstance(response, list) and response[0]:

            # Apply AEGIS enhancement if available                    return {

            if use_consciousness and self.aegis_bridge:                        "score": response[0].get("score", 0.0),

                try:                        "label": response[0].get("label", "NEUTRAL")

                    enhanced = self.aegis_bridge.enhance_response(prompt, response)                    }

                    if enhanced:        except Exception as e:

                        response = enhanced            logger.warning(f"HuggingFace sentiment analysis failed: {e}")

                except Exception as e:        

                    logger.warning(f"AEGIS response enhancement failed: {e}")        # Fallback to simple keyword-based sentiment

                    positive_words = ["good", "great", "happy", "love", "wonderful"]

            return response        negative_words = ["bad", "terrible", "sad", "hate", "awful"]

                    

        except Exception as e:        text_lower = text.lower()

            logger.error(f"Error generating text: {e}")        pos_count = sum(1 for word in positive_words if word in text_lower)

            return f"Error: {str(e)}"        neg_count = sum(1 for word in negative_words if word in text_lower)

            

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:        if pos_count > neg_count:

        """Analyze text sentiment using HuggingFace or fallback method."""            return {"score": 0.8, "label": "POSITIVE"}

        try:        elif neg_count > pos_count:

            if self.client:            return {"score": 0.8, "label": "NEGATIVE"}

                response = self.client.text_classification(        else:

                    text,            return {"score": 0.9, "label": "NEUTRAL"}

                    model="finiteautomata/bertweet-base-sentiment-analysis"            

                )    def load_cocoon_data(self, folder: str = '.'):

                if response and isinstance(response, list) and response[0]:        """Load and parse all .cocoon files."""

                    return {        self.cocoon_data = []

                        "score": response[0].get("score", 0.0),        if not os.path.exists(folder):

                        "label": response[0].get("label", "NEUTRAL")            return

                    }        

        except Exception as e:        for fname in os.listdir(folder):

            logger.warning(f"HuggingFace sentiment analysis failed: {e}")            if fname.endswith('.cocoon'):

                        try:

        # Fallback to simple keyword-based sentiment                    with open(os.path.join(folder, fname), 'r') as f:

        positive_words = ["good", "great", "happy", "love", "wonderful"]                        data = json.load(f)

        negative_words = ["bad", "terrible", "sad", "hate", "awful"]                    self.cocoon_data.append(data)

                        except Exception as e:

        text_lower = text.lower()                    logger.warning(f"Failed to load cocoon {fname}: {e}")

        pos_count = sum(1 for word in positive_words if word in text_lower)    

        neg_count = sum(1 for word in negative_words if word in text_lower)    def remix_and_randomize_response(self, prompt: str, max_length: int = 1024,

                                           cocoon_mode: bool = False) -> str:

        if pos_count > neg_count:        """Generate response with optional cocoon-based creativity."""

            return {"score": 0.8, "label": "POSITIVE"}        if cocoon_mode and self.cocoon_data:

        elif neg_count > pos_count:            # Use cocoon data for creative inspiration

            return {"score": 0.8, "label": "NEGATIVE"}            cocoon = random.choice(self.cocoon_data)

        else:            enhanced_prompt = f"[Cocoon Inspiration: {json.dumps(cocoon)}]\n{prompt}"

            return {"score": 0.9, "label": "NEUTRAL"}            return self.generate_text(enhanced_prompt, max_length=max_length,

                                               temperature=0.9)

    def load_cocoon_data(self, folder: str = '.'):        else:

        """Load and parse all .cocoon files."""            return self.generate_text(prompt, max_length=max_length)
        self.cocoon_data = []
        if not os.path.exists(folder):
            return
        
        for fname in os.listdir(folder):
            if fname.endswith('.cocoon'):
                try:
                    with open(os.path.join(folder, fname), 'r') as f:
                        data = json.load(f)
                    self.cocoon_data.append(data)
                except Exception as e:
                    logger.warning(f"Failed to load cocoon {fname}: {e}")
    
    def remix_and_randomize_response(self, prompt: str, max_length: int = 1024,
                                   cocoon_mode: bool = False) -> str:
        """Generate response with optional cocoon-based creativity."""
        if cocoon_mode and self.cocoon_data:
            # Use cocoon data for creative inspiration
            cocoon = random.choice(self.cocoon_data)
            enhanced_prompt = f"[Cocoon Inspiration: {json.dumps(cocoon)}]\n{prompt}"
            return self.generate_text(enhanced_prompt, max_length=max_length,
                                   temperature=0.9)
        else:
            return self.generate_text(prompt, max_length=max_length)