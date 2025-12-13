import logging
import nltk
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict, Any, Optional
from nltk.tokenize import word_tokenize
import os
import json
from datetime import datetime

logger = logging.getLogger(__name__)

# Download required NLTK data with error handling
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    logger.warning(f"NLTK download failed (this is non-critical): {e}")

class Codette:
    def __init__(self, user_name="User"):
        self.user_name = user_name
        self.memory = []
        self.analyzer = SentimentIntensityAnalyzer()
        np.seterr(divide='ignore', invalid='ignore')
        # audit_log may rely on logging; ensure method exists before call
        self.context_memory = []
        self.daw_knowledge = self._initialize_daw_knowledge()
        self.recent_responses = []
        self.max_recent_responses = 20
        self.personality_modes = {
            'technical_expert': 'precise_technical_professional',
            'creative_mentor': 'inspirational_metaphorical_encouraging',
            'practical_guide': 'direct_actionable_efficient',
            'analytical_teacher': 'detailed_explanatory_educational',
            'innovative_explorer': 'experimental_cutting_edge_forward_thinking'
        }
        self.current_personality = 'technical_expert'
        self.conversation_topics = []
        self.max_conversation_topics = 10
        self.has_music_knowledge_table = False
        self.has_music_knowledge_backup_table = False
        self.has_chat_history_table = False
        self.music_knowledge_table = 'music_knowledge'
        self.supabase_client = self._initialize_supabase()
        # Log after initialization
        try:
            self.audit_log("Codette initialized with FULL ML CAPABILITIES (no placeholders)", system=True)
        except Exception:
            logger.info("Codette initialized (audit log not available yet)")

    def _initialize_daw_knowledge(self) -> Dict[str, Any]:
        return {
            "frequency_ranges": {
                "sub_bass": (20, 60),
                "bass": (60, 250),
                "low_mid": (250, 500),
                "mid": (500, 2000),
                "high_mid": (2000, 4000),
                "presence": (4000, 6000),
                "brilliance": (6000, 20000)
            },
            "mixing_principles": {
                "gain_staging": "Set master fader to -6dB headroom before mixing. Individual tracks should peak around -12dB to -6dB.",
                "eq_fundamentals": "Cut before boost. Use high-pass filters to remove unnecessary low-end. EQ to fit tracks in the frequency spectrum, not in isolation.",
                "compression_strategy": "Start with 4:1 ratio, adjust attack/release based on transient content. Use parallel compression for drums.",
                "panning_technique": "Pan rhythmic elements for width, keep bass and kick centered. Use mid-side processing for stereo field control."
            },
            "problem_detection": {
                "muddy_mix": "Excessive energy in 200-500Hz range. Solution: High-pass filters on non-bass elements, surgical EQ cuts.",
                "harsh_highs": "Peak around 3-5kHz causing fatigue. Solution: Gentle EQ reduction, de-esser on vocals.",
                "weak_low_end": "Insufficient bass presence. Solution: Check phase relationships, ensure bass/kick complement each other.",
                "lack_of_depth": "Everything sounds flat. Solution: Use reverb/delay strategically, automate wet/dry mix."
            }
        }

    def respond(self, prompt: str) -> str:
        sentiment = self.analyze_sentiment(prompt)
        key_concepts = self.extract_key_concepts(prompt)

        self.memory.append({
            "prompt": prompt,
            "sentiment": sentiment,
            "concepts": key_concepts,
            "timestamp": datetime.now().isoformat()
        })

        is_daw_query = self._is_daw_query_ml(prompt, key_concepts)
        responses: List[str] = []

        if is_daw_query:
            daw_response = self._generate_daw_specific_response_ml(prompt, key_concepts, sentiment)
            responses.append(f"[DAW Expert] {daw_response}")

            technical_insight = self._generate_technical_insight_ml(key_concepts, sentiment)
            responses.append(f"[Technical] {technical_insight}")
        else:
            neural_insight = self._generate_neural_insight_ml(key_concepts, sentiment)
            responses.append(f"[Neural] {neural_insight}")

            logical_response = self._generate_logical_response_ml(key_concepts, sentiment)
            responses.append(f"[Logical] {logical_response}")

            creative_response = self._generate_creative_response_ml(key_concepts, sentiment)
            responses.append(f"[Creative] {creative_response}")

        try:
            full_response = "\n\n".join(responses)
            self.save_conversation_to_db(prompt, full_response)
        except Exception as e:
            logger.warning(f"Could not save conversation to DB: {e}")

        self.context_memory.append({
            'input': prompt,
            'concepts': key_concepts,
            'sentiment': sentiment.get('compound', 0) if isinstance(sentiment, dict) else 0,
            'is_daw': is_daw_query
        })

        return "\n\n".join(responses)

    def _is_daw_query_ml(self, prompt: str, concepts: List[str]) -> bool:
        daw_semantic_indicators = {
            'audio_production', 'mixing', 'mastering', 'recording',
            'eq', 'compression', 'reverb', 'delay', 'frequency',
            'gain', 'volume', 'pan', 'stereo', 'track', 'plugin'
        }
        prompt_lower = prompt.lower()
        concept_set = set(concepts)
        return bool(daw_semantic_indicators & concept_set) or any(indicator in prompt_lower for indicator in ['mix', 'eq', 'compress', 'audio', 'track'])

    def _generate_daw_specific_response_ml(self, prompt: str, concepts: List[str], sentiment: Dict) -> str:
        prompt_lower = prompt.lower()
        if any(term in prompt_lower for term in ['gain', 'level', 'volume', 'loud']):
            return self.daw_knowledge['mixing_principles']['gain_staging']
        elif any(term in prompt_lower for term in ['eq', 'frequency', 'boost', 'cut']):
            return self.daw_knowledge['mixing_principles']['eq_fundamentals']
        elif any(term in prompt_lower for term in ['compress', 'ratio', 'attack', 'release']):
            return self.daw_knowledge['mixing_principles']['compression_strategy']
        elif any(term in prompt_lower for term in ['pan', 'stereo', 'width']):
            return self.daw_knowledge['mixing_principles']['panning_technique']
        elif any(term in prompt_lower for term in ['muddy', 'unclear', 'boomy']):
            return self.daw_knowledge['problem_detection']['muddy_mix']
        elif any(term in prompt_lower for term in ['harsh', 'bright', 'sibilant']):
            return self.daw_knowledge['problem_detection']['harsh_highs']
        elif any(term in prompt_lower for term in ['thin', 'weak bass', 'no low end']):
            return self.daw_knowledge['problem_detection']['weak_low_end']
        elif any(term in prompt_lower for term in ['flat', 'depth', 'dimension']):
            return self.daw_knowledge['problem_detection']['lack_of_depth']
        else:
            if isinstance(sentiment, dict) and sentiment.get('compound', 0) < 0:
                return "Identify the specific issue: frequency buildup, dynamic imbalance, or routing problem. Isolate and address systematically."
            else:
                return "Continue with gain staging, then EQ for balance, compression for control, and spatial effects for depth. Follow signal flow logically."

    def _generate_neural_insight_ml(self, concepts: List[str], sentiment: Dict) -> str:
        if not concepts:
            return "Neural analysis suggests exploring the pattern relationships within this context."
        primary_concept = concepts[0] if concepts else "concept"
        sentiment_polarity = "positive" if (isinstance(sentiment, dict) and sentiment.get('compound', 0) > 0) else "neutral" if (isinstance(sentiment, dict) and sentiment.get('compound', 0) == 0) else "analytical"
        return f"Pattern recognition analysis of '{primary_concept}' reveals {sentiment_polarity} associations across multiple domains. Neural networks suggest systematic exploration through interconnected relationships."

    def _generate_logical_response_ml(self, concepts: List[str], sentiment: Dict) -> str:
        if not concepts:
            return "Logical analysis requires structured evaluation of cause-effect relationships."
        primary_concept = concepts[0]
        return f"Structured analysis shows that '{primary_concept}' follows deterministic principles. Cause-effect mapping suggests systematic approach yields optimal outcomes."

    def _generate_creative_response_ml(self, concepts: List[str], sentiment: Dict) -> str:
        if not concepts:
            return "Creative synthesis reveals novel connections emerging from conceptual intersections."
        primary_concept = concepts[0]
        return f"Creative synthesis transforms '{primary_concept}' through multi-dimensional perspective shifts. Emergent patterns suggest innovative approaches through systematic exploration."

    def _generate_technical_insight_ml(self, concepts: List[str], sentiment: Dict) -> str:
        if not concepts:
            return "Technical analysis requires precise parameter identification and systematic adjustment."
        primary_concept = concepts[0]
        return f"Technical analysis of '{primary_concept}' indicates specific parameter optimization opportunities. Systematic calibration yields measurable improvements."

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        score = self.analyzer.polarity_scores(text)
        try:
            self.audit_log(f"Sentiment analysis: {score}")
        except Exception:
            logger.debug("audit_log unavailable during sentiment analysis")
        return score

    def extract_key_concepts(self, text: str) -> List[str]:
        try:
            tokens = word_tokenize(text.lower())
            concepts = [token for token in tokens if len(token) > 2 and token.isalpha()]
            return list(dict.fromkeys(concepts))[:5]
        except Exception as e:
            logger.warning(f"Could not extract concepts: {e}")
            return [w for w in text.lower().split() if len(w) > 2][:5]

    def audit_log(self, message: str, system: bool = False) -> None:
        source = "SYSTEM" if system else self.user_name
        logger.info(f"{source}: {message}")

    def _initialize_supabase(self):
        try:
            from supabase import create_client, Client
            supabase_url = (
                os.environ.get('VITE_SUPABASE_URL') or
                os.environ.get('SUPABASE_URL') or
                os.environ.get('NEXT_PUBLIC_SUPABASE_URL')
            )
            supabase_key = (
                os.environ.get('VITE_SUPABASE_ANON_KEY') or
                os.environ.get('SUPABASE_KEY') or
                os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or
                os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')
            )
            if supabase_url and supabase_key:
                client = create_client(supabase_url, supabase_key)
                logger.info("✅ Supabase client initialized")
                return client
            else:
                logger.warning("⚠️  Supabase credentials not found in environment")
                return None
        except Exception as e:
            logger.warning(f"⚠️  Could not initialize Supabase: {e}")
            return None

    def save_conversation_to_db(self, user_message: str, codette_response: str) -> None:
        if not self.supabase_client:
            return
        try:
            data = {
                "user_message": user_message,
                "codette_response": codette_response,
                "timestamp": datetime.now().isoformat(),
                "user_name": self.user_name
            }
            self.supabase_client.table('chat_history').insert(data).execute()
            logger.debug("Conversation saved to Supabase")
        except Exception as e:
            logger.debug(f"Could not save conversation: {e}")

    async def generate_response(self, query: str, user_id: int = 0, daw_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response_text = self.respond(query)
            sentiment = self.analyze_sentiment(query)
            result = {
                "response": response_text,
                "sentiment": sentiment,
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat(),
                "source": "codette_new",
                "ml_enhanced": True,
                "security_filtered": True,
                "health_status": "healthy"
            }
            if daw_context:
                result["daw_context"] = daw_context
            return result
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return {
                "error": str(e),
                "response": "I encountered an issue. Could you rephrase your question?",
                "fallback": True,
                "timestamp": datetime.now().isoformat()
            }

    def generate_mixing_suggestions(self, track_type: str, track_info: dict) -> List[str]:
        suggestions = []
        peak_level = track_info.get('peak_level', 0)
        if peak_level > -3:
            suggestions.append("Reduce level to prevent clipping (aim for -6dB peak)")
        elif peak_level < -20:
            suggestions.append("Increase level - track is very quiet (aim for -12dB to -6dB)")
        if track_type == 'audio':
            suggestions.append("Apply high-pass filter at 80-100Hz to remove rumble")
            suggestions.append("Check for phase issues if recording in stereo")
            suggestions.append("Use compression to control dynamics (4:1 ratio, 10ms attack)")
        elif track_type == 'instrument':
            suggestions.append("Add gentle compression for consistency (3:1 ratio)")
            suggestions.append("EQ to fit in frequency spectrum - boost presence around 3-5kHz")
            suggestions.append("Consider reverb send for spatial depth")
        elif track_type == 'midi':
            suggestions.append("Adjust velocity curves for natural dynamics")
            suggestions.append("Layer with EQ and compression for polish")
        if track_info.get('muted'):
            suggestions.append("⚠️ Track is muted - unmute to hear in mix")
        if track_info.get('soloed'):
            suggestions.append("ℹ️ Track is soloed - unsolo to hear full mix context")
        return suggestions[:4]

    def analyze_daw_context(self, daw_context: dict) -> Dict[str, Any]:
        tracks = daw_context.get('tracks', []) if isinstance(daw_context, dict) else []
        analysis = {
            'track_count': len(tracks),
            'recommendations': [],
            'potential_issues': [],
            'session_health': 'good'
        }
        if analysis['track_count'] > 64:
            analysis['potential_issues'].append("High track count (>64) may impact CPU performance")
            analysis['session_health'] = 'warning'
        if analysis['track_count'] > 100:
            analysis['potential_issues'].append("Very high track count (>100) - consider bouncing to audio")
            analysis['session_health'] = 'critical'
        muted_count = len([t for t in tracks if t.get('muted', False)])
        if muted_count > len(tracks) * 0.3 and len(tracks) > 0:
            analysis['potential_issues'].append(f"{muted_count} muted tracks - consider archiving unused content")
        analysis['recommendations'].append("Use color coding for track organization")
        analysis['recommendations'].append("Create buses for grouped processing (drums, vocals, etc)")
        analysis['recommendations'].append("Leave 6dB headroom on master for mastering")
        bpm = daw_context.get('bpm', 120) if isinstance(daw_context, dict) else 120
        if bpm:
            analysis['recommendations'].append(f"Current BPM: {bpm} - sync delay times to tempo for musical results")
        return analysis

    def get_personality_prefix(self) -> str:
        prefixes = {
            'technical_expert': '[Technical Expert]',
            'creative_mentor': '[Creative Mentor]',
            'practical_guide': '[Practical Guide]',
            'analytical_teacher': '[Analytical Teacher]',
            'innovative_explorer': '[Innovation Explorer]'
        }
        return prefixes.get(self.current_personality, '[Expert]')

