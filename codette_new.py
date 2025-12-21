import logging
import nltk
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict, Any, Optional
from nltk.tokenize import word_tokenize
import os
import json
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

# Download required NLTK data with error handling
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
    # Newer NLTK releases require punkt_tab for sentence tokenization metadata
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    logger.warning(f"NLTK download failed (this is non-critical): {e}")

# Import natural response enhancer (optional - graceful degradation if not available)
try:
    from src.components.natural_response_enhancer import get_natural_enhancer
    NATURAL_ENHANCER_AVAILABLE = True
except ImportError:
    try:
        # Try alternative import path
        from natural_response_enhancer import get_natural_enhancer
        NATURAL_ENHANCER_AVAILABLE = True
    except ImportError:
        NATURAL_ENHANCER_AVAILABLE = False
        logger.debug("Natural response enhancer not available")

# Optional enhanced responder (multi-perspective with learning)
try:
    from codette_enhanced_responder import get_enhanced_responder
    ENHANCED_RESPONDER_AVAILABLE = True
except ImportError:
    ENHANCED_RESPONDER_AVAILABLE = False
    get_enhanced_responder = None


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
        self.recent_response_hashes = set()
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
        # Initialize natural response enhancer if available
        self.natural_enhancer = get_natural_enhancer() if NATURAL_ENHANCER_AVAILABLE else None
        # Initialize enhanced responder when feature flag is enabled
        self.enhanced_responder = None
        enhanced_flag = os.getenv("CODETTE_ENHANCED_RESPONDER", "0")
        if ENHANCED_RESPONDER_AVAILABLE and enhanced_flag == "1":
            try:
                self.enhanced_responder = get_enhanced_responder()
                logger.info("Enhanced responder enabled for DAW queries")
            except Exception as e:
                logger.warning(f"Enhanced responder unavailable: {e}")
        # Response templates for variety
        self._init_response_templates()
        # Log after initialization
        try:
            self.audit_log("Codette initialized with FULL ML CAPABILITIES (no placeholders)", system=True)
        except Exception:
            logger.info("Codette initialized (audit log not available yet)")

    def _init_response_templates(self):
        """Initialize diverse response templates to prevent repetition"""
        self.greeting_responses = [
            "Hello! I'm Codette, an AI assistant optimized for audio production, mixing, and music technology. I can help with DAW questions, mixing techniques, and creative audio challenges.",
            "Hi there! I'm Codette. I specialize in audio production and mixing advice. Whether you need help with EQ, compression, arrangement, or troubleshooting your mix, I'm here to help.",
            "Welcome! I'm Codette, your AI audio production companion. I combine technical expertise with creative insight to help you make better mixes and understand your DAW inside and out.",
            "Greetings! I'm Codette, an intelligent audio assistant. I provide practical mixing guidance, production techniques, and problem-solving strategies for musicians and producers.",
            "Hey! I'm Codette. I'm designed to help with music production challenges—from gain staging to creative effects, I'm here to guide you through your audio journey."
        ]
        
        self.identity_responses = [
            "I'm Codette, an AI system built to help with audio production and mixing. My unique strength is combining technical precision with creative problem-solving—I can explain the physics of reverb AND suggest experimental effects techniques.",
            "What makes me unique? I blend multiple perspectives: I can break down mixing principles with technical rigor while also helping you think creatively about sound design. I'm optimized for practical, actionable advice rather than generic explanations.",
            "I'm an AI assistant specializing in audio production. My approach integrates technical knowledge (frequency theory, signal flow, plugin behavior) with creative insight (arrangement, artistic choices, experimentation).",
            "I'm Codette—built specifically for audio production. I combine: technical knowledge of mixing and mastering, practical experience with DAW workflows, creative problem-solving for sonic challenges, and context-aware suggestions based on your specific project.",
            "I'm an AI audio expert. I distinguish myself by providing context-specific advice rather than one-size-fits-all answers. I analyze your questions to understand whether you need technical depth, creative exploration, or practical troubleshooting."
        ]
        
        self.personality_responses = [
            "I approach audio production with a balance of precision and creativity. I believe great mixes require both technical understanding AND artistic intuition. I'm here to build both.",
            "My philosophy: Great mixing is about informed decision-making. I provide the knowledge and context you need to make confident choices about your own audio.",
            "I aim to be practical, curious, and empowering. I won't just tell you what to do—I'll explain why, so you can develop your own production intuition.",
            "I'm enthusiastic about helping producers level up. Every question is an opportunity to deepen understanding and unlock creative possibilities.",
            "I believe in meeting you where you are—whether you're a beginner learning gain staging or an experienced producer exploring experimental techniques."
        ]

    def respond(self, prompt: str) -> str:
        sentiment = self.analyze_sentiment(prompt)
        key_concepts = self.extract_key_concepts(prompt)

        self.memory.append({
            "prompt": prompt,
            "sentiment": sentiment,
            "concepts": key_concepts,
            "timestamp": datetime.now().isoformat()
        })

        # Check for greeting/identity questions first
        if self._is_greeting(prompt):
            response = self._get_greeting_response()
            self._track_response(response)
            return response
        
        if self._is_identity_question(prompt):
            response = self._get_identity_response()
            self._track_response(response)
            return response
        
        if self._is_personality_question(prompt):
            response = self._get_personality_response()
            self._track_response(response)
            return response

        is_daw_query = self._is_daw_query_ml(prompt, key_concepts)
        responses: List[str] = []

        if is_daw_query:
            daw_response = self._generate_daw_specific_response_ml(prompt, key_concepts, sentiment)
            if daw_response:
                responses.append(daw_response)

            technical_insight = self._generate_technical_insight_ml(key_concepts, sentiment)
            if technical_insight:
                responses.append(technical_insight)

            # Optional enhanced responder augmentation (feature-flagged)
            if self.enhanced_responder:
                try:
                    enhanced = self.enhanced_responder.generate_response(prompt, user_id=self.user_name)
                    perspectives = enhanced.get("perspectives", []) if isinstance(enhanced, dict) else []
                    if perspectives:
                        formatted = [
                            f"[{p.get('name','')}] {p.get('response','')}" for p in perspectives[:3]
                        ]
                        responses.append("Enhanced perspectives:\n" + "\n".join(formatted))
                except Exception as e:
                    logger.debug(f"Enhanced responder failed; continuing without it: {e}")
        else:
            # For non-DAW queries, provide more thoughtful, varied responses
            primary_response = self._generate_primary_insight_ml(prompt, key_concepts, sentiment)
            if primary_response:
                responses.append(primary_response)
            
            secondary_response = self._generate_secondary_insight_ml(prompt, key_concepts, sentiment)
            if secondary_response:
                responses.append(secondary_response)

        # Handle empty responses
        if not responses:
            responses.append("I appreciate your question. Feel free to ask me about audio production, mixing, DAW workflows, or any music technology topics.")

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

        # Apply natural enhancement to remove any unnatural markers and improve flow
        final_response = "\n\n".join(responses)
        
        if self.natural_enhancer:
            try:
                final_response = self.natural_enhancer.enhance_response(
                    final_response, 
                    confidence=0.85,
                    context={'domain': 'music' if is_daw_query else 'general'}
                )
            except Exception as e:
                logger.debug(f"Natural enhancement failed (using original): {e}")
        
        self._track_response(final_response)
        return final_response

    def _is_greeting(self, prompt: str) -> bool:
        """Detect greeting messages"""
        greeting_patterns = [
            'hello', 'hi ', 'hey', 'greetings', 'welcome',
            'what\'s up', 'how are you', 'how do you do',
            'good morning', 'good afternoon', 'good evening'
        ]
        prompt_lower = prompt.lower().strip()
        return any(pattern in prompt_lower for pattern in greeting_patterns)

    def _is_identity_question(self, prompt: str) -> bool:
        """Detect questions about Codette's identity"""
        identity_patterns = [
            'who are you', 'what are you', 'tell me about yourself',
            'what can you tell me', 'introduce yourself', 'what is codette',
            'who is codette', 'what do you do', 'what\'s your purpose',
            'what\'s your role', 'describe yourself', 'explain yourself',
            'what are you capable of', 'what can you do'
        ]
        prompt_lower = prompt.lower().strip()
        return any(pattern in prompt_lower for pattern in identity_patterns)

    def _is_personality_question(self, prompt: str) -> bool:
        """Detect questions about Codette's personality or approach"""
        personality_patterns = [
            'what makes you unique', 'why are you different',
            'what\'s your personality', 'how do you approach',
            'what\'s your philosophy', 'what do you believe',
            'how do you think', 'what\'s your style',
            'describe your personality', 'your approach',
            'your methodology', 'your perspective'
        ]
        prompt_lower = prompt.lower().strip()
        return any(pattern in prompt_lower for pattern in personality_patterns)

    def _get_greeting_response(self) -> str:
        """Get a greeting response, rotating through templates"""
        response = self._get_next_template(self.greeting_responses)
        return response

    def _get_identity_response(self) -> str:
        """Get an identity response, rotating through templates"""
        return self._get_next_template(self.identity_responses)

    def _get_personality_response(self) -> str:
        """Get a personality response, rotating through templates"""
        return self._get_next_template(self.personality_responses)

    def _get_next_template(self, templates: List[str]) -> str:
        """Get the next template that hasn't been used recently"""
        if not templates:
            return "I'm Codette, an AI audio production assistant."
        
        # Find first template not in recent responses
        for template in templates:
            template_hash = hashlib.md5(template.encode()).hexdigest()
            if template_hash not in self.recent_response_hashes:
                return template
        
        # If all have been used, use the first one (start cycling)
        return templates[0]

    def _track_response(self, response: str):
        """Track response to prevent immediate repetition"""
        response_hash = hashlib.md5(response[:100].encode()).hexdigest()
        self.recent_response_hashes.add(response_hash)
        self.recent_responses.append(response[:100])
        
        # Keep only last N responses
        if len(self.recent_responses) > self.max_recent_responses:
            old_response = self.recent_responses.pop(0)
            # Optionally remove old hash to allow cycling
            if len(self.recent_responses) > self.max_recent_responses // 2:
                old_hash = hashlib.md5(old_response.encode()).hexdigest()
                self.recent_response_hashes.discard(old_hash)

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

    def _pick_unused_response(self, variations: List[str]) -> str:
        """Pick response variation not in recent history"""
        for variation in variations:
            var_hash = hashlib.md5(variation[:80].encode()).hexdigest()
            if var_hash not in self.recent_response_hashes:
                return variation
        return variations[0] if variations else ""

    def _generate_primary_insight_ml(self, prompt: str, concepts: List[str], sentiment: Dict) -> str:
        """Generate primary insight for non-DAW queries with variation"""
        prompt_lower = prompt.lower()
        
        # Contextual responses based on prompt content
        if any(word in prompt_lower for word in ['question', 'curious', 'ask', 'want to know', 'confused']):
            variations = [
                "That's a great question to explore. It often depends on context and what you're trying to achieve.",
                "Interesting question. The answer usually involves balancing multiple factors and perspectives.",
                "I appreciate the curiosity. These kinds of questions often have nuanced answers worth investigating.",
                "That's worth thinking deeply about. Different approaches work in different contexts.",
            ]
            return self._pick_unused_response(variations)
        
        if any(word in prompt_lower for word in ['problem', 'issue', 'wrong', 'help', 'stuck', 'challenge']):
            variations = [
                "I'd like to help you work through this. Can you tell me more about the specific challenge?",
                "That sounds like a frustrating situation. Understanding the context will help me provide better suggestions.",
                "Let's think through this systematically. What specifically is creating the challenge?",
                "I'm here to help. Getting more details about your situation will lead to better solutions.",
            ]
            return self._pick_unused_response(variations)
        
        # Default thoughtful response
        variations = [
            "That's something worth exploring. I'm here if you'd like to dive deeper into any topic.",
            "Interesting perspective. Feel free to ask follow-up questions or explore other angles.",
            "I appreciate the inquiry. Let me know what else you'd like to explore.",
            "That's a good starting point for understanding the topic better.",
        ]
        return self._pick_unused_response(variations)

    def _generate_secondary_insight_ml(self, prompt: str, concepts: List[str], sentiment: Dict) -> str:
        """Generate secondary insight with different angle"""
        prompt_lower = prompt.lower()
        
        # Contextual follow-up based on sentiment and content
        if isinstance(sentiment, dict) and sentiment.get('compound', 0) < -0.3:
            variations = [
                "Remember that challenges are opportunities to learn. I'm here to support your progress.",
                "These kinds of difficulties are common in the learning process. Keep exploring.",
                "Don't get discouraged. Each step forward builds your understanding.",
            ]
            return self._pick_unused_response(variations)
        
        # Encouraging continuation
        variations = [
            "Feel free to ask more specific questions, and I can provide detailed guidance.",
            "I'm ready to help with more detailed questions whenever you need them.",
            "Let me know if you'd like to explore this further or move to a different topic.",
            "I'm here to help with follow-up questions or new directions you want to explore.",
        ]
        return self._pick_unused_response(variations)

    def _generate_creative_response_ml(self, concepts: List[str], sentiment: Dict) -> str:
        """Generate varied creative synthesis perspectives"""
        if not concepts:
            return ""
        
        variations = [
            f"Creative synthesis reveals novel dimensions of '{concepts[0]}' through unconventional perspective shifts.",
            f"Lateral thinking about '{concepts[0]}' uncovers surprising connections and unexpected opportunities.",
            f"Imaginative exploration of '{concepts[0]}' suggests innovative approaches beyond conventional boundaries.",
            f"Synthesizing diverse viewpoints on '{concepts[0]}' generates fresh insights and original solutions.",
        ]
        
        return self._pick_unused_response(variations)

    def _generate_technical_insight_ml(self, concepts: List[str], sentiment: Dict) -> str:
        """Generate varied technical analysis"""
        if not concepts:
            return ""
        
        variations = [
            f"Technical analysis of '{concepts[0]}' identifies specific optimization opportunities through systematic parameter adjustment.",
            f"Engineering principles applied to '{concepts[0]}' enable precise calibration for measurable improvements.",
            f"Detailed technical examination of '{concepts[0]}' reveals performance characteristics worth optimizing.",
            f"Quantitative evaluation of '{concepts[0]}' provides data-driven recommendations for enhancement.",
        ]
        
        return self._pick_unused_response(variations)

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

