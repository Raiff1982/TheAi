import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class DAWAddOn:
    """Optional DAW-focused add-on. Encapsulates all DAW detection and guidance.

    This keeps the main Codette components domain-neutral by default and only
    activates when explicitly enabled and imported.
    """

    def __init__(self) -> None:
        self.knowledge = self._initialize_daw_knowledge()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def is_daw_query(self, prompt: str, concepts: List[str]) -> bool:
        prompt_lower = prompt.lower()
        concept_set = set(concepts)
        daw_semantic_indicators = {
            "audio_production",
            "mixing",
            "mastering",
            "recording",
            "eq",
            "compression",
            "reverb",
            "delay",
            "frequency",
            "gain",
            "volume",
            "pan",
            "stereo",
            "track",
            "plugin",
        }
        if daw_semantic_indicators & concept_set:
            return True
        return any(term in prompt_lower for term in ["mix", "eq", "compress", "audio", "track"])

    def generate_responses(self, prompt: str, concepts: List[str], sentiment: Dict[str, Any]) -> List[str]:
        responses: List[str] = []
        main = self._generate_daw_specific_response(prompt, concepts, sentiment)
        if main:
            responses.append(main)
        technical = self._generate_technical_insight(concepts, sentiment)
        if technical:
            responses.append(technical)
        return responses

    def generate_followups(self, prompt: str, concepts: List[str]) -> Optional[str]:
        return self._generate_followup_suggestions(prompt, concepts, is_daw_query=True)

    def generate_mixing_suggestions(self, track_type: str, track_info: dict) -> List[str]:
        suggestions = []
        peak_level = track_info.get("peak_level", 0)
        if peak_level > -3:
            suggestions.append("Reduce level to prevent clipping (aim for -6dB peak)")
        elif peak_level < -20:
            suggestions.append("Increase level - track is very quiet (aim for -12dB to -6dB)")
        if track_type == "audio":
            suggestions.append("Apply high-pass filter at 80-100Hz to remove rumble")
            suggestions.append("Check for phase issues if recording in stereo")
            suggestions.append("Use compression to control dynamics (4:1 ratio, 10ms attack)")
        elif track_type == "instrument":
            suggestions.append("Add gentle compression for consistency (3:1 ratio)")
            suggestions.append("EQ to fit in frequency spectrum - boost presence around 3-5kHz")
            suggestions.append("Consider reverb send for spatial depth")
        elif track_type == "midi":
            suggestions.append("Adjust velocity curves for natural dynamics")
            suggestions.append("Layer with EQ and compression for polish")
        if track_info.get("muted"):
            suggestions.append("⚠️ Track is muted - unmute to hear in mix")
        if track_info.get("soloed"):
            suggestions.append("ℹ️ Track is soloed - unsolo to hear full mix context")
        return suggestions[:4]

    def analyze_daw_context(self, daw_context: dict) -> Dict[str, Any]:
        tracks = daw_context.get("tracks", []) if isinstance(daw_context, dict) else []
        analysis = {
            "track_count": len(tracks),
            "recommendations": [],
            "potential_issues": [],
            "session_health": "good",
        }
        if analysis["track_count"] > 64:
            analysis["potential_issues"].append("High track count (>64) may impact CPU performance")
            analysis["session_health"] = "warning"
        if analysis["track_count"] > 100:
            analysis["potential_issues"].append("Very high track count (>100) - consider bouncing to audio")
            analysis["session_health"] = "critical"
        muted_count = len([t for t in tracks if t.get("muted", False)])
        if muted_count > len(tracks) * 0.3 and len(tracks) > 0:
            analysis["potential_issues"].append(f"{muted_count} muted tracks - consider archiving unused content")
        analysis["recommendations"].append("Use color coding for track organization")
        analysis["recommendations"].append("Create buses for grouped processing (drums, vocals, etc)")
        analysis["recommendations"].append("Leave 6dB headroom on master for mastering")
        bpm = daw_context.get("bpm", 120) if isinstance(daw_context, dict) else 120
        if bpm:
            analysis["recommendations"].append(f"Current BPM: {bpm} - sync delay times to tempo for musical results")
        return analysis

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _generate_daw_specific_response(self, prompt: str, concepts: List[str], sentiment: Dict[str, Any]) -> str:
        prompt_lower = prompt.lower()
        if any(term in prompt_lower for term in ["gain", "level", "volume", "loud"]):
            return self.knowledge["mixing_principles"]["gain_staging"]
        if any(term in prompt_lower for term in ["eq", "frequency", "boost", "cut"]):
            return self.knowledge["mixing_principles"]["eq_fundamentals"]
        if any(term in prompt_lower for term in ["compress", "ratio", "attack", "release"]):
            return self.knowledge["mixing_principles"]["compression_strategy"]
        if any(term in prompt_lower for term in ["pan", "stereo", "width"]):
            return self.knowledge["mixing_principles"]["panning_technique"]
        if any(term in prompt_lower for term in ["muddy", "unclear", "boomy"]):
            return self.knowledge["problem_detection"]["muddy_mix"]
        if any(term in prompt_lower for term in ["harsh", "bright", "sibilant"]):
            return self.knowledge["problem_detection"]["harsh_highs"]
        if any(term in prompt_lower for term in ["thin", "weak bass", "no low end"]):
            return self.knowledge["problem_detection"]["weak_low_end"]
        if any(term in prompt_lower for term in ["flat", "depth", "dimension"]):
            return self.knowledge["problem_detection"]["lack_of_depth"]
        if isinstance(sentiment, dict) and sentiment.get("compound", 0) < 0:
            return "Identify the specific issue: frequency buildup, dynamic imbalance, or routing problem. Isolate and address systematically."
        return "Continue with gain staging, then EQ for balance, compression for control, and spatial effects for depth. Follow signal flow logically."

    def _generate_technical_insight(self, concepts: List[str], sentiment: Dict[str, Any]) -> str:
        if not concepts:
            return ""
        variations = [
            f"Technical analysis of '{concepts[0]}' identifies specific optimization opportunities through systematic parameter adjustment.",
            f"Engineering principles applied to '{concepts[0]}' enable precise calibration for measurable improvements.",
            f"Detailed technical examination of '{concepts[0]}' reveals performance characteristics worth optimizing.",
            f"Quantitative evaluation of '{concepts[0]}' provides data-driven recommendations for enhancement.",
        ]
        return variations[0]

    def _generate_followup_suggestions(self, prompt: str, concepts: List[str], is_daw_query: bool) -> Optional[str]:
        prompt_lower = prompt.lower()
        suggestions: List[str] = []
        if is_daw_query:
            if any(term in prompt_lower for term in ["vocal", "singer", "voice"]):
                suggestions.extend([
                    "Ask for a vocal chain order (HPF → EQ → compression → de-ess → reverb send).",
                    "Check de-esser thresholds or sibilant bands if highs feel harsh.",
                    "Request suggested attack/release times for your vocal style (spoken vs sung).",
                ])
            elif any(term in prompt_lower for term in ["guitar", "bass", "drum", "kick", "snare"]):
                suggestions.extend([
                    "Compare mic/DI blend tips for your instrument to tighten tone.",
                    "Ask for frequency slots to avoid masking with vocals or synths.",
                    "Request parallel processing ideas (parallel comp or saturation) for punch without losing transients.",
                ])
            elif any(term in prompt_lower for term in ["reverb", "delay", "space", "ambience"]):
                suggestions.extend([
                    "Ask for predelay/decay starting points matched to your BPM.",
                    "Check which elements should stay dry vs sent to the shared verb bus.",
                    "Try mid-side EQ on reverb returns to keep lows centered and highs airy.",
                ])
            elif any(term in prompt_lower for term in ["mix", "master", "muddy", "harsh", "boomy", "mud"]):
                suggestions.extend([
                    "Request a 3-step cleanup checklist (HPF targets, surgical EQ, gain staging).",
                    "Ask for reference track matching tips (loudness and tonal balance).",
                    "Check mono-compatibility and phase if the mix collapses when summed.",
                ])
            else:
                target = concepts[0] if concepts else "your track"
                suggestions.extend([
                    f"Ask for a quick signal-flow plan tailored to {target} (gain → EQ → compression → space).",
                    "Request starter EQ bands and ratios for common sources (vocals, drums, bass).",
                    "Ask for a minimal CPU chain if your session is lagging (shared sends, render heavy FX).",
                ])
        if not suggestions:
            return None
        trimmed = suggestions[:3]
        return "Follow-up ideas:\n- " + "\n- ".join(trimmed)

    def _initialize_daw_knowledge(self) -> Dict[str, Any]:
        return {
            "frequency_ranges": {
                "sub_bass": (20, 60),
                "bass": (60, 250),
                "low_mid": (250, 500),
                "mid": (500, 2000),
                "high_mid": (2000, 4000),
                "presence": (4000, 6000),
                "brilliance": (6000, 20000),
            },
            "mixing_principles": {
                "gain_staging": "Set master fader to -6dB headroom before mixing. Individual tracks should peak around -12dB to -6dB.",
                "eq_fundamentals": "Cut before boost. Use high-pass filters to remove unnecessary low-end. EQ to fit tracks in the frequency spectrum, not in isolation.",
                "compression_strategy": "Start with 4:1 ratio, adjust attack/release based on transient content. Use parallel compression for drums.",
                "panning_technique": "Pan rhythmic elements for width, keep bass and kick centered. Use mid-side processing for stereo field control.",
            },
            "problem_detection": {
                "muddy_mix": "Excessive energy in 200-500Hz range. Solution: High-pass filters on non-bass elements, surgical EQ cuts.",
                "harsh_highs": "Peak around 3-5kHz causing fatigue. Solution: Gentle EQ reduction, de-esser on vocals.",
                "weak_low_end": "Insufficient bass presence. Solution: Check phase relationships, ensure bass/kick complement each other.",
                "lack_of_depth": "Everything sounds flat. Solution: Use reverb/delay strategically, automate wet/dry mix.",
            },
        }
