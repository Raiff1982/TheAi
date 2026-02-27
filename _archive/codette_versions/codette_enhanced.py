import logging
import warnings
import os
import sys

# Suppress PyTensor C++ warnings before importing pymc
os.environ["PYTENSOR_FLAGS"] = "device=cpu,floatX=float32,cxx="
warnings.filterwarnings("ignore", category=UserWarning, module="pytensor")
warnings.filterwarnings("ignore", message=".*g\\+\\+ not.*")

import nltk
# Require a compatible NumPy build before proceeding
import numpy as np
import sympy as sp

# Import pymc with warning suppression
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pymc as pm
    import arviz as az

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from typing import List, Dict, Any

nltk.download('punkt', quiet=True)

# =========================================================================
# IMPORT TRAINING DATA
# =========================================================================

# Add parent directory to path to find training data
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import comprehensive training data
try:
    from codette_training_data import CodetteTrainingData, GENRE_KNOWLEDGE, MIXING_STANDARDS, PLUGIN_SUGGESTIONS, EXTENDED_INSTRUMENTS_DATABASE, PRODUCTION_CHECKLIST
    TRAINING_DATA_AVAILABLE = True
    training_data = CodetteTrainingData()
    logging.info("[OK] Codette training data loaded successfully")
except ImportError as e:
    TRAINING_DATA_AVAILABLE = False
    training_data = None
    logging.warning(f"[WARNING] Could not import training data: {e}")

class Codette:
    def __init__(self, user_name="User"):
        self.user_name = user_name
        self.memory = []
        self.analyzer = SentimentIntensityAnalyzer()
        self._qlp_cache = {}
        
        # Load comprehensive training data if available
        if TRAINING_DATA_AVAILABLE and training_data:
            self.training_data = training_data
            self.genre_knowledge = training_data.genre_knowledge
            self.mixing_standards = training_data.audio_standards
            self.plugin_suggestions = training_data.plugin_suggestions
            self.instruments_db = training_data.instruments_database
            self.production_checklist = training_data.production_checklist
            logging.info("[OK] Codette using comprehensive training data")
        else:
            self.training_data = None
            self.genre_knowledge = {}
            self.mixing_standards = {}
            self.plugin_suggestions = {}
            self.instruments_db = {}
            self.production_checklist = {}
            logging.info("[NOTE] Codette using fallback DAW knowledge")
        
        # DAW-specific knowledge base (fallback + enhancements)
        self.daw_knowledge = self._initialize_daw_knowledge()
        
        # Configure PyMC settings for stability
        self.mcmc_settings = {
            'chains': 4,
            'tune': 1000,
            'draws': 1000,
            'target_accept': 0.95,
            'return_inferencedata': True
        }
        
        # Set numpy error handling
        np.seterr(divide='ignore', invalid='ignore')
        
        self.audit_log("Codette initialized", system=True)

    def _initialize_daw_knowledge(self) -> Dict[str, Any]:
        """Initialize DAW-specific knowledge base"""
        return {
            "mixing": {
                "gain_staging": "Set individual tracks to peak around -12dB to -6dB, leaving -6dB headroom on the master.",
                "eq": "Cut before boost. Use high-pass filters on non-bass elements. EQ in context, not solo.",
                "compression": "Start with 4:1 ratio for vocals, 2-4:1 for instruments. Adjust attack/release based on transients.",
                "panning": "Keep bass and kick centered. Pan guitars, keys, and backing vocals for width.",
                "reverb": "Use sends, not inserts. Short reverb for presence, long for depth. Less is more.",
                "delay": "Sync to tempo. Use 1/8 or 1/4 notes. Duck delays during vocal phrases."
            },
            "problems": {
                "muddy": "Cut 200-400Hz on non-bass elements. Use high-pass filters aggressively.",
                "harsh": "Reduce 2-5kHz. Use de-esser on vocals. Check for over-compression.",
                "thin": "Check phase relationships. Add subtle low-mid boost (200-400Hz).",
                "no_depth": "Add reverb/delay to create front-to-back space. Automate wet/dry."
            },
            "workflow": {
                "organization": "Color-code tracks by type. Use buses for grouped processing.",
                "efficiency": "Create templates. Use keyboard shortcuts. Batch similar tasks.",
                "cpu": "Freeze heavy plugins. Increase buffer size when mixing. Bounce to audio."
            }
        }
        
    def audit_log(self, message, system=False):
        source = "SYSTEM" if system else self.user_name
        logging.info(f"{source}: {message}")

    def analyze_sentiment(self, text):
        score = self.analyzer.polarity_scores(text)
        return score

    def _is_daw_query(self, prompt: str) -> bool:
        """Check if query is DAW/audio related"""
        daw_keywords = [
            # Core mixing terms
            'mix', 'master', 'eq', 'compress', 'reverb', 'delay', 'audio', 'track',
            'bass', 'vocal', 'drum', 'frequency', 'gain', 'volume', 'pan', 'stereo',
            'plugin', 'effect', 'fx', 'bus', 'send', 'daw', 'recording', 'muddy',
            'harsh', 'thin', 'loud', 'quiet', 'clip', 'distort', 'sidechain',
            'automation', 'fade', 'crossfade', 'bounce', 'export', 'sample', 'midi',
            # Additional common terms
            'improve', 'better', 'sound', 'add', 'create', 'use', 'recommend',
            'instrument', 'aux', 'key', 'tempo', 'bpm', 'pitch', 'tone', 'music',
            'song', 'project', 'production', 'producer', 'engineer', 'studio',
            'channel', 'fader', 'level', 'db', 'decibel', 'peak', 'rms', 'lufs',
            'what', 'how', 'should', 'can', 'help', 'advice', 'tip', 'suggestion',
            # Effects
            'chorus', 'flanger', 'phaser', 'saturation', 'limiter', 'gate',
            'expander', 'de-esser', 'exciter', 'enhancer', 'stereo width',
            # Instruments
            'guitar', 'piano', 'synth', 'keyboard', 'strings', 'brass', 'percussion',
            'hi-hat', 'kick', 'snare', 'cymbal', 'tom', 'shaker', 'tambourine'
        ]
        prompt_lower = prompt.lower()
        return any(kw in prompt_lower for kw in daw_keywords)

    def _get_daw_context(self, prompt: str) -> Dict[str, Any]:
        """Extract DAW context from prompt"""
        prompt_lower = prompt.lower()
        context = {
            "category": "general",
            "element": None,
            "problem": None
        }
        
        # Detect category
        if any(w in prompt_lower for w in ['eq', 'frequency', 'hz', 'boost', 'cut']):
            context["category"] = "eq"
        elif any(w in prompt_lower for w in ['compress', 'ratio', 'attack', 'release', 'threshold']):
            context["category"] = "compression"
        elif any(w in prompt_lower for w in ['reverb', 'delay', 'echo', 'space', 'room']):
            context["category"] = "spatial"
        elif any(w in prompt_lower for w in ['gain', 'level', 'volume', 'loud', 'quiet', 'headroom']):
            context["category"] = "gain_staging"
        elif any(w in prompt_lower for w in ['pan', 'stereo', 'width', 'mono']):
            context["category"] = "panning"
        elif any(w in prompt_lower for w in ['mix', 'balance', 'blend']):
            context["category"] = "mixing"
        
        # Detect element
        if any(w in prompt_lower for w in ['vocal', 'voice', 'sing']):
            context["element"] = "vocals"
        elif any(w in prompt_lower for w in ['bass', 'sub', 'low end', '808']):
            context["element"] = "bass"
        elif any(w in prompt_lower for w in ['drum', 'kick', 'snare', 'hi-hat', 'cymbal']):
            context["element"] = "drums"
        elif any(w in prompt_lower for w in ['guitar', 'keys', 'piano', 'synth']):
            context["element"] = "instruments"
        
        # Detect problem
        if any(w in prompt_lower for w in ['muddy', 'boomy', 'unclear']):
            context["problem"] = "muddy"
        elif any(w in prompt_lower for w in ['harsh', 'bright', 'sibilant', 'piercing']):
            context["problem"] = "harsh"
        elif any(w in prompt_lower for w in ['thin', 'weak', 'no body']):
            context["problem"] = "thin"
        elif any(w in prompt_lower for w in ['flat', 'no depth', '2d', 'boring']):
            context["problem"] = "no_depth"
        
        return context

    # =========================================================================
    # MAIN RESPOND METHOD (UPDATED WITH FOLLOW-UP DETECTION)
    # =========================================================================

    def respond(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        sentiment = self.analyze_sentiment(prompt)
        self.memory.append({"prompt": prompt, "sentiment": sentiment, "daw_context": daw_context})
        
        # If we have DAW context, always treat as DAW query
        is_daw = self._is_daw_query(prompt) or (daw_context is not None and daw_context.get("selected_track"))
        context = self._get_daw_context(prompt)
        
        # Detect follow-up questions to avoid repetitive context dumps
        is_followup = self._is_followup_question(prompt)
        
        # Build context-aware introduction if we have DAW state (only on first message or explicit context request)
        context_intro = ""
        if daw_context and not is_followup:
            selected = daw_context.get("selected_track")
            track_counts = daw_context.get("track_counts", {})
            
            if selected:
                context_intro = f"**Currently working on: {selected.get('name', 'Unknown')} ({selected.get('type', 'audio')} track)**\n"
                vol = selected.get('volume', 0)
                # Format volume nicely
                if isinstance(vol, float):
                    vol = round(vol, 1)
                context_intro += f"Volume: {vol}dB | Pan: {selected.get('pan', 0)}\n"
                if selected.get('muted'):
                    context_intro += "?? Track is MUTED\n"
                if selected.get('soloed'):
                    context_intro += "?? Track is SOLOED\n"
                context_intro += "\n"
            
            if track_counts.get('total', 0) > 0:
                context_intro += f"?? Project has {track_counts['total']} tracks"
                types = []
                for t, count in track_counts.items():
                    if t != 'total' and count > 0:
                        types.append(f"{count} {t}")
                if types:
                    context_intro += f" ({', '.join(types)})"
                context_intro += "\n\n"
        
        # All perspective methods
        modules = [
            self.neuralNetworkPerspective,
            self.newtonianLogic,
            self.daVinciSynthesis,
            self.resilientKindness,
            self.quantumLogicPerspective,
            self.philosophicalInquiry,
            self.copilotAgent,
            self.mathematicalRigor,
            self.symbolicReasoning
        ]
        
        # For DAW queries (or when we have context), prioritize relevant perspectives
        if is_daw:
            # For follow-up questions, use different perspectives to vary the response
            if is_followup:
                # Rotate perspectives for follow-up questions
                priority_modules = [
                    self.daVinciSynthesis,        # Creative ideas
                    self.resilientKindness,       # Supportive guidance  
                    self.philosophicalInquiry,    # Deeper questions
                    self.quantumLogicPerspective, # Alternative approaches
                ]
            else:
                # Prioritize practical perspectives for initial DAW queries
                priority_modules = [
                    self.copilotAgent,        # Step-by-step guidance
                    self.neuralNetworkPerspective,  # Analysis
                    self.newtonianLogic,      # Cause-effect
                    self.mathematicalRigor,   # Technical specs
                    self.daVinciSynthesis,    # Creative ideas
                ]
            selected_modules = priority_modules[:4]  # Use top 4 for focused response
        else:
            # For non-DAW queries, suggest DAW focus
            selected_modules = [self.copilotAgent, self.resilientKindness]

        responses = []
        
        # Add context intro if available (only for non-followup)
        if context_intro:
            responses.append(context_intro)
        
        for module in selected_modules:
            try:
                result = module(prompt, daw_context)
                responses.append(result)
            except Exception as e:
                logging.warning(f"Perspective {module.__name__} failed: {e}")

        self.audit_log(f"Perspectives used: {[m.__name__ for m in selected_modules]}")
        return "\n\n".join(responses)
    
    def _is_followup_question(self, prompt: str) -> bool:
        """Detect if this is a follow-up question that doesn't need full context dump"""
        prompt_lower = prompt.lower().strip()
        
        # Common follow-up phrases
        followup_patterns = [
            'what else',
            'anything else',
            'more tips',
            'more advice',
            'tell me more',
            'go on',
            'continue',
            'and',
            'also',
            'what about',
            'how about',
            'any other',
            'other suggestions',
            'other ideas',
            'more ideas',
            'next',
            'then what',
            'what next',
            'ok',
            'okay',
            'got it',
            'thanks',
            'thank you',
            'cool',
            'nice',
            'great',
            'good',
            'yes',
            'yeah',
            'yep',
            'sure',
            'right',
            'hmm',
            'interesting',
        ]
        
        # Check if prompt is a short follow-up
        if len(prompt_lower.split()) <= 4:
            for pattern in followup_patterns:
                if pattern in prompt_lower:
                    return True
        
        # Check if prompt starts with follow-up words
        followup_starters = ['and ', 'also ', 'what else', 'anything else', 'more ', 'other ']
        for starter in followup_starters:
            if prompt_lower.startswith(starter):
                return True
        
        return False
    
    # =========================================================================
    # DAW-AWARE PERSPECTIVE METHODS
    # =========================================================================
    
    def neuralNetworkPerspective(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Neural network perspective - pattern recognition for audio using training data"""
        is_daw = self._is_daw_query(prompt)
        context = self._get_daw_context(prompt)
        selected = daw_context.get("selected_track") if daw_context else None
        
        if is_daw:
            if selected:
                track_type = selected.get('type', 'audio')
                track_name = selected.get('name', 'your track')
                volume = selected.get('volume', 0)
                track_name_lower = track_name.lower()
                
                # Use training data for intelligent analysis
                if self.training_data:
                    # Detect instrument category from track name
                    if 'vocal' in track_name_lower or 'voice' in track_name_lower or 'sing' in track_name_lower:
                        info = self.instruments_db.get('vocals', {}).get('lead_vocals', {})
                        freq_range = info.get('frequency_range', (50, 3500))
                        return f"**neural_network**: [Vocal Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Recommended chain: High-pass at 80-100Hz, presence boost at 3-5kHz, de-ess at 6-8kHz if sibilant. Compress for consistency (4:1 to 6:1)."
                    
                    elif 'kick' in track_name_lower:
                        info = self.instruments_db.get('drums', {}).get('kick', {})
                        freq_range = info.get('frequency_range', (20, 250))
                        return f"**neural_network**: [Kick Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: Focus on sub (50-80Hz) for weight, 2-4kHz for click/attack. High-pass at 20Hz to remove rumble. Compress with fast attack for punch."
                    
                    elif 'snare' in track_name_lower:
                        info = self.instruments_db.get('drums', {}).get('snare', {})
                        freq_range = info.get('frequency_range', (100, 8000))
                        return f"**neural_network**: [Snare Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: 200Hz for body, 5kHz for snap/crack. Gate to reduce bleed, compress 2:1-4:1 for consistency."
                    
                    elif 'hi-hat' in track_name_lower or 'hihat' in track_name_lower or 'hat' in track_name_lower:
                        info = self.instruments_db.get('drums', {}).get('hihat_closed', {})
                        freq_range = info.get('frequency_range', (2000, 12000))
                        return f"**neural_network**: [Hi-Hat Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: High-pass aggressively (300-500Hz), slight presence boost at 8-10kHz. Keep dynamics natural."
                    
                    elif 'drum' in track_name_lower or 'tom' in track_name_lower:
                        info = self.instruments_db.get('drums', {}).get('tom', {})
                        freq_range = info.get('frequency_range', (80, 3000))
                        return f"**neural_network**: [Drum Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: Gate for clean hits, EQ for punch (100-200Hz) and attack (3-5kHz). Pan toms for width."
                    
                    elif 'bass' in track_name_lower:
                        info = self.instruments_db.get('bass', {}).get('electric_bass', {})
                        freq_range = info.get('frequency_range', (40, 2000))
                        return f"**neural_network**: [Bass Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: High-pass at 30-40Hz, focus 60-100Hz for weight, 600-800Hz for definition. Keep centered."
                    
                    elif 'guitar' in track_name_lower:
                        if 'acoustic' in track_name_lower:
                            info = self.instruments_db.get('guitars', {}).get('acoustic_guitar', {})
                        else:
                            info = self.instruments_db.get('guitars', {}).get('electric_guitar_clean', {})
                        freq_range = info.get('frequency_range', (80, 8000))
                        return f"**neural_network**: [Guitar Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: High-pass at 80-100Hz, cut mud at 200-400Hz, add presence at 3-5kHz. Pan for stereo width."
                    
                    elif 'piano' in track_name_lower or 'keys' in track_name_lower:
                        info = self.instruments_db.get('keyboards', {}).get('piano', {})
                        freq_range = info.get('frequency_range', (27, 4000))
                        return f"**neural_network**: [Piano/Keys Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: Wide frequency content, EQ to fit mix. Light compression 2:1 for consistency. Natural reverb."
                    
                    elif 'synth' in track_name_lower or 'pad' in track_name_lower:
                        info = self.instruments_db.get('keyboards', {}).get('synth_pad', {})
                        freq_range = info.get('frequency_range', (30, 12000))
                        return f"**neural_network**: [Synth Analysis for '{track_name}'] Current volume: {volume}dB. Frequency range: {freq_range[0]}-{freq_range[1]}Hz. Analysis: EQ to carve space around vocals/leads. Add chorus or stereo widening. Use sidechain for pump effect if desired."
                    
                    else:
                        return f"**neural_network**: [Track Analysis for '{track_name}'] Type: {track_type}, Volume: {volume}dB. Pattern recognition suggests: EQ for frequency clarity, compression for dynamics control, spatial effects for depth."
                else:
                    # Fallback without training data
                    return f"**neural_network**: [Track Analysis for '{track_name}'] Type: {track_type}, Volume: {volume}dB. Pattern recognition suggests: EQ for frequency clarity, compression for dynamics control, spatial effects for depth."
            
            # Generic DAW advice based on context
            if context["category"] == "eq":
                return "**neural_network**: [Audio Analysis] Pattern recognition identifies frequency buildup. Recommended: Apply surgical EQ cuts at problem frequencies (typically 200-400Hz for mud, 2-5kHz for harshness). Use spectrum analyzer to visualize."
            elif context["category"] == "compression":
                return "**neural_network**: [Dynamics Analysis] Transient patterns detected. For consistent dynamics: Use 4:1 ratio as starting point, set attack to preserve transients (10-30ms), release to match tempo. Watch gain reduction meter."
            else:
                return f"**neural_network**: [Mix Analysis] Audio patterns suggest systematic approach: Start with gain staging, then EQ for clarity, compression for dynamics, spatial effects for depth."
        else:
            return "**neural_network**: [Analysis] I'm optimized for DAW and audio production questions. Try asking about mixing, EQ, compression, or specific instruments!"

    def copilotAgent(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Copilot agent - practical mixing steps with context and training data"""
        is_daw = self._is_daw_query(prompt)
        context = self._get_daw_context(prompt)
        selected = daw_context.get("selected_track") if daw_context else None
        track_counts = daw_context.get("track_counts", {}) if daw_context else {}
        
        # Always give helpful advice when we have a selected track
        if selected:
            track_type = selected.get('type', 'audio')
            track_name = selected.get('name', 'your track')
            volume = selected.get('volume', 0)
            if isinstance(volume, float):
                volume = round(volume, 1)
            inserts = selected.get('inserts', 0)
            muted = selected.get('muted', False)
            soloed = selected.get('soloed', False)
            
            steps = []
            
            # Check for muted/soloed state first
            if muted:
                steps.append(f"?? '{track_name}' is MUTED - unmute to hear your changes")
            
            # Volume recommendations using training data standards
            if self.training_data:
                gain_standards = self.mixing_standards.get("gain_staging", {})
                recommended_headroom = gain_standards.get("input_headroom", -6.0)
            else:
                recommended_headroom = -6.0
            
            if volume > -3:
                steps.append(f"?? '{track_name}' is hot ({volume}dB) - reduce to {recommended_headroom}dB for headroom")
            elif volume < -18:
                steps.append(f"?? '{track_name}' is quiet ({volume}dB) - consider boosting or check gain staging")
            else:
                steps.append(f"? '{track_name}' volume ({volume}dB) is in good range")
            
            # Insert chain recommendations using training data
            if inserts == 0:
                # Get plugin suggestions from training data if available
                plugin_suggestions = self.suggest_plugins_for_track_type(track_name.lower())
                if plugin_suggestions:
                    suggestion_text = ", ".join([f"{p['category']}: {p['suggestion']}" for p in plugin_suggestions[:3]])
                    steps.append(f"?? No plugins on track - recommended: {suggestion_text}")
                else:
                    steps.append("?? No plugins on track - consider adding: 1) EQ for cleanup, 2) Compressor for dynamics")
            
            # Track-type specific advice using training data
            track_name_lower = track_name.lower()
            
            # Check instruments database for specific processing tips
            if self.training_data:
                # Map track name to instrument category
                if 'vocal' in track_name_lower:
                    tips = self.get_instrument_processing_tips('vocals', 'lead_vocals')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Vocal chain: High-pass ? EQ (cut mud) ? Compressor ? EQ (add presence) ? De-esser ? Reverb send")
                elif 'kick' in track_name_lower:
                    tips = self.get_instrument_processing_tips('drums', 'kick')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Kick processing: High-pass at 20Hz ? EQ (sub + click) ? Compression ? Saturation")
                elif 'snare' in track_name_lower:
                    tips = self.get_instrument_processing_tips('drums', 'snare')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Snare processing: Gate ? EQ (body + snap) ? Compression ? Reverb")
                elif 'bass' in track_name_lower:
                    tips = self.get_instrument_processing_tips('bass', 'electric_bass')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Bass processing: High-pass at 30Hz ? EQ ? Compressor ? Sidechain to kick if needed")
                elif 'guitar' in track_name_lower:
                    if 'acoustic' in track_name_lower:
                        tips = self.get_instrument_processing_tips('guitars', 'acoustic_guitar')
                    else:
                        tips = self.get_instrument_processing_tips('guitars', 'electric_guitar_clean')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Guitar processing: High-pass at 80Hz ? EQ (cut mud 200-400Hz) ? Compression ? Stereo widening")
                elif 'piano' in track_name_lower or 'keys' in track_name_lower:
                    tips = self.get_instrument_processing_tips('keyboards', 'piano')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Keys/Piano: EQ to fit with other elements ? Light compression ? Stereo width as needed")
                elif 'synth' in track_name_lower:
                    tips = self.get_instrument_processing_tips('keyboards', 'synth_pad')
                    if tips != "No specific instrument data available":
                        steps.append(f"?? {tips}")
                    else:
                        steps.append("?? Synth: EQ for presence ? Light compression ? Reverb/Chorus for space")
                elif track_type == 'instrument':
                    steps.append("?? Instrument track: Add virtual instrument, then process with EQ ? Compression ? Effects")
                elif track_type == 'aux':
                    steps.append("?? Aux/Bus track: Set up as effects return (reverb, delay) or group bus for parallel processing")
                else:
                    steps.append("?? General processing: EQ for cleanup ? Compression for dynamics ? Effects to taste")
            else:
                # Fallback without training data
                if 'vocal' in track_name_lower or track_type == 'vocal':
                    steps.append("?? Vocal chain: High-pass ? EQ (cut mud) ? Compressor ? EQ (add presence) ? De-esser ? Reverb send")
                elif 'drum' in track_name_lower or 'kick' in track_name_lower or 'snare' in track_name_lower:
                    steps.append("?? Drum processing: Phase check ? Gate ? EQ ? Compressor ? Parallel compression bus")
                elif 'bass' in track_name_lower or track_type == 'bass':
                    steps.append("?? Bass processing: High-pass at 30Hz ? EQ ? Compressor ? Sidechain to kick if needed")
                elif 'guitar' in track_name_lower:
                    steps.append("?? Guitar processing: High-pass at 80Hz ? EQ (cut mud 200-400Hz) ? Compression ? Stereo widening")
                elif 'synth' in track_name_lower or 'keys' in track_name_lower or 'piano' in track_name_lower:
                    steps.append("?? Keys/Synth: EQ to fit with other elements ? Light compression ? Stereo width as needed")
                elif track_type == 'instrument':
                    steps.append("?? Instrument track: Add virtual instrument, then process with EQ ? Compression ? Effects")
                elif track_type == 'aux':
                    steps.append("?? Aux/Bus track: Set up as effects return (reverb, delay) or group bus for parallel processing")
                else:
                    steps.append("?? General processing: EQ for cleanup ? Compression for dynamics ? Effects to taste")
            
            # Project-wide suggestions based on track counts
            total_tracks = track_counts.get('total', 0)
            if total_tracks > 1:
                steps.append(f"?? With {total_tracks} tracks, consider: bus routing, gain staging across all tracks, and frequency separation")
            
            # Question-specific additions
            prompt_lower = prompt.lower()
            if 'fx' in prompt_lower or 'effect' in prompt_lower:
                steps.append("? Recommended FX order: EQ ? Compression ? Saturation ? Modulation ? Time-based (delay/reverb)")
            if 'aux' in prompt_lower or 'bus' in prompt_lower:
                steps.append("?? Aux/Send tips: Create reverb and delay sends, use buses to group similar tracks (drums, vocals, etc.)")
            if 'key' in prompt_lower or 'pitch' in prompt_lower:
                steps.append("?? Key detection: Use a tuner or pitch analyzer plugin to identify the root note of your audio")
            if 'instrument' in prompt_lower:
                steps.append("?? Instrument tracks: Add MIDI instruments for layering or use samples/loops for quick arrangements")
            
            # Genre-specific advice if mentioned
            if self.training_data:
                for genre in self.genre_knowledge.keys():
                    if genre in prompt_lower:
                        genre_advice = self.get_genre_mixing_advice(genre)
                        steps.append(f"?? {genre_advice}")
                        break
            
            return "**copilot_agent**: [Action Plan for " + track_name + "]\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        
        # Generic workflow advice when no track selected
        if context["category"] == "mixing":
            return "**copilot_agent**: [Step-by-Step] Mixing workflow: 1) Gain stage all tracks (-12dB peaks), 2) Static balance with faders only, 3) EQ for clarity and separation, 4) Compress for dynamics control, 5) Add spatial effects, 6) Automate for movement, 7) Reference and iterate."
        elif context["element"] == "vocals":
            return "**copilot_agent**: [Vocal Chain] Recommended vocal processing order: 1) Gain staging, 2) High-pass filter (80-100Hz), 3) Subtractive EQ (cut mud/harshness), 4) Compression (4:1, medium attack), 5) Additive EQ (presence, air), 6) De-esser if needed, 7) Reverb/delay sends."
        else:
            return "**copilot_agent**: [Action Plan] Select a track to get specific recommendations! General tips: Start with gain staging, then EQ ? Compression ? Effects."
    
    def newtonianLogic(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Newtonian logic - cause and effect in audio"""
        is_daw = self._is_daw_query(prompt)
        context = self._get_daw_context(prompt)
        selected = daw_context.get("selected_track") if daw_context else None
        
        if is_daw:
            if selected and selected.get('muted'):
                return f"**newtonian_logic**: [Cause-Effect] Track '{selected['name']}' is MUTED - you won't hear any changes until you unmute it."
            
            if context["problem"] == "muddy":
                return "**newtonian_logic**: [Cause-Effect] Muddy mix cause: Frequency buildup in 200-400Hz range from multiple sources. Solution: High-pass filter non-bass elements at 80-150Hz, cut competing frequencies with surgical EQ."
            elif context["problem"] == "harsh":
                return "**newtonian_logic**: [Cause-Effect] Harsh sound cause: Excessive energy at 2-5kHz or over-compression. Solution: Reduce presence frequencies, use de-esser on vocals, check compressor attack times."
            elif context["category"] == "gain_staging":
                return "**newtonian_logic**: [Signal Flow] Gain staging principle: Input level determines signal-to-noise ratio. Set tracks to peak at -12dB to -6dB, leaving -6dB headroom on master for mastering."
            else:
                return "**newtonian_logic**: [Audio Physics] In audio: Every processing decision has consequences. Signal flow matters - gain staging ? EQ ? compression ? effects. Address problems at the source first."
        else:
            return "**newtonian_logic**: [DAW Logic] I specialize in audio production cause-and-effect analysis. Ask me about why your mix sounds a certain way or how to fix specific problems!"

    def mathematicalRigor(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Mathematical rigor - technical audio specs"""
        is_daw = self._is_daw_query(prompt)
        context = self._get_daw_context(prompt)
        selected = daw_context.get("selected_track") if daw_context else None
        
        if is_daw:
            if selected:
                volume = selected.get('volume', 0)
                # Calculate headroom
                headroom = -volume if volume < 0 else 0
                return f"**mathematical_rigor**: [Technical Specs for '{selected['name']}'] Current level: {volume}dB, Headroom to 0dBFS: {headroom}dB. Target: -18dBFS RMS for analog-modeled plugins. Peak recommendation: -6dB for mix, -3dB for buses, -1dB on master."
            
            if context["category"] == "gain_staging":
                return "**mathematical_rigor**: [Technical Specs] Gain staging math: Target -18dBFS RMS for analog-modeled plugins (0dBVU = -18dBFS). Peak headroom: -6dB on tracks, -3dB on buses, -1dB on master for mastering headroom."
            elif context["category"] == "compression":
                return "**mathematical_rigor**: [Compression Math] Ratio 4:1 means: for every 4dB above threshold, only 1dB passes. Attack 10ms preserves transients, 30ms+ smooths them. Release: 4x attack time as starting point, or use auto-release."
            else:
                return "**mathematical_rigor**: [Audio Specs] Technical targets: Streaming loudness -14 LUFS (Spotify), -16 LUFS (Apple Music). Sample rate 44.1kHz or 48kHz. Bit depth 24-bit for recording, 16-bit for final delivery."
        else:
            return "**mathematical_rigor**: [Technical Audio] I provide precise technical specifications for audio production. Ask about frequencies, levels, or processing parameters!"

    def daVinciSynthesis(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Da Vinci synthesis - creative audio production"""
        is_daw = self._is_daw_query(prompt)
        context = self._get_daw_context(prompt)
        selected = daw_context.get("selected_track") if daw_context else None
        
        if is_daw:
            if selected:
                track_name = selected.get('name', 'your track')
                if 'vocal' in track_name.lower():
                    return f"**davinci_synthesis**: [Creative Ideas for '{track_name}'] Try: Double-track for width, add subtle pitch shift (+/- 7 cents) on doubles, automate reverb throws on key phrases for drama, use telephone EQ effect for contrast."
                elif 'drum' in track_name.lower():
                    return f"**davinci_synthesis**: [Creative Ideas for '{track_name}'] Try: Layer samples for unique character, use parallel compression (NY compression) for punch, automate reverb sends for dynamic builds, try gated reverb on snare."
                else:
                    return f"**davinci_synthesis**: [Creative Ideas for '{track_name}'] Experiment with: Automation for movement, unexpected reverb/delay settings, parallel processing for impact, creative EQ for character."
            
            return "**davinci_synthesis**: [Creative Mix Approach] Art meets science in mixing: Use technical tools (EQ, compression) to serve the emotional intent. Reference professional mixes in your genre for inspiration."
        else:
            return "**davinci_synthesis**: [Creative Audio] I blend technical knowledge with artistic vision for audio production. Ask about creative mixing techniques or sound design!"

    def resilientKindness(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Resilient kindness - supportive mixing guidance"""
        sentiment = self.analyze_sentiment(prompt)
        is_daw = self._is_daw_query(prompt)
        track_count = daw_context.get("track_counts", {}).get("total", 0) if daw_context else 0
        
        if is_daw:
            if sentiment['compound'] < -0.3:
                return "**resilient_kindness**: [Supportive Guidance] Mixing challenges can be frustrating - that's completely normal! Take a break, rest your ears for 15-20 minutes, then return with fresh perspective. Small incremental changes are better than drastic moves."
            elif track_count > 0:
                return f"**resilient_kindness**: [Encouraging Guidance] Great work on your project with {track_count} tracks! Remember: There's no 'wrong' - only different artistic choices. Trust your ears, reference often, and enjoy the creative process."
            else:
                return "**resilient_kindness**: [Encouraging Guidance] Great that you're working on your mix! Trust your ears, reference often, and enjoy the creative process."
        else:
            return "**resilient_kindness**: [Friendly Reminder] I'm here to help with your DAW and mixing questions! Don't hesitate to ask about any audio production challenges."

    def quantumLogicPerspective(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Quantum logic - multiple mixing approaches"""
        is_daw = self._is_daw_query(prompt)
        context = self._get_daw_context(prompt)
        
        if is_daw:
            if context["category"] == "eq":
                return "**quantum_logic**: [Multiple Approaches] EQ superposition: You could cut the mud OR boost the clarity - both achieve separation. Try subtractive EQ first (cutting problem frequencies), then additive if needed. A/B test both approaches."
            elif context["category"] == "compression":
                return "**quantum_logic**: [Multiple Approaches] Compression paths: Serial compression (multiple light compressors) vs parallel compression (blend compressed with dry) vs single heavy compression. Each creates different textures - experiment to find what serves the song."
            else:
                return "**quantum_logic**: [Multiple Solutions] In mixing, multiple valid approaches exist simultaneously. The 'right' one depends on genre, taste, and context. Try A/B testing different approaches."
        else:
            return "**quantum_logic**: [DAW Possibilities] I explore multiple audio production approaches. Ask about mixing decisions and I'll show you different valid paths!"

    def philosophicalInquiry(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Philosophical inquiry - deeper mixing questions"""
        is_daw = self._is_daw_query(prompt)
        
        if is_daw:
            return "**philosophical_inquiry**: [Mix Philosophy] The deeper question: What emotion should this mix convey? Technical decisions (EQ, compression, space) should serve the artistic vision. Ask yourself: Does this processing enhance or distract from the song's message?"
        else:
            return "**philosophical_inquiry**: [Audio Philosophy] I ponder the deeper questions of audio production. What's the purpose of your mix? Let's align technical decisions with artistic intent."

    def symbolicReasoning(self, prompt: str, daw_context: Dict[str, Any] = None) -> str:
        """Symbolic reasoning - signal flow and routing"""
        is_daw = self._is_daw_query(prompt)
        selected = daw_context.get("selected_track") if daw_context else None
        
        if is_daw:
            if selected:
                return f"**symbolic_reasoning**: [Signal Flow for '{selected['name']}'] Chain: Input ? Gain Stage ? Insert FX (EQ, Comp) ? Fader ({selected.get('volume', 0)}dB) ? Pan ({selected.get('pan', 0)}) ? Sends ? Bus ? Master. Check each stage for optimal levels."
            return "**symbolic_reasoning**: [Signal Flow] Audio signal chain: Input ? Gain ? Insert FX (EQ, Comp) ? Fader ? Pan ? Sends (Reverb, Delay) ? Bus ? Master. Understanding this flow helps diagnose where problems occur."
        else:
            return "**symbolic_reasoning**: [DAW Signal Flow] I analyze signal flow and routing in DAWs. Ask about signal chains, bus routing, or effect ordering!"

    # =========================================================================
    # SERVER INTEGRATION METHODS
    # =========================================================================
    
    def generate_mixing_suggestions(self, track_type: str, track_info: dict) -> List[str]:
        """Generate mixing suggestions for a specific track"""
        suggestions = []
        
        peak_level = track_info.get('peak_level', -6)
        if peak_level > -3:
            suggestions.append("?? Reduce level to prevent clipping (aim for -6dB peak)")
        elif peak_level < -18:
            suggestions.append("?? Increase level - track is very quiet (aim for -12dB to -6dB)")
        
        if track_type in ['audio', 'vocal', 'vocals']:
            suggestions.append("?? Apply high-pass filter at 80-100Hz to remove rumble")
            suggestions.append("?? Use compression (4:1 ratio) for consistent dynamics")
            suggestions.append("? Boost presence at 3-5kHz for clarity")
        elif track_type in ['instrument', 'synth', 'keys']:
            suggestions.append("?? EQ to fit in frequency spectrum - avoid clashing with vocals")
            suggestions.append("?? Light compression (2:1 to 3:1) for consistency")
        elif track_type in ['drums', 'drum', 'percussion']:
            suggestions.append("?? Check phase alignment if multi-miked")
            suggestions.append("?? Use parallel compression for punch")
        elif track_type in ['bass', 'sub']:
            suggestions.append("?? Keep centered in stereo field")
            suggestions.append("?? Consider sidechain to kick drum")
        
        if track_info.get('muted'):
            suggestions.append("?? Track is muted - unmute to hear in mix")
        if track_info.get('soloed'):
            suggestions.append("?? Track is soloed - unsolo to hear full mix context")
        
        return suggestions[:5]

    # =========================================================================
    # TRAINING DATA INTEGRATION METHODS
    # =========================================================================
    
    def get_genre_mixing_advice(self, genre: str) -> str:
        """Get mixing advice specific to a genre using training data"""
        if self.training_data and genre.lower() in self.genre_knowledge:
            genre_info = self.genre_knowledge[genre.lower()]
            advice = f"**{genre.title()} Mixing Guide**\n"
            advice += f"- Tempo Range: {genre_info.get('tempo_range', 'N/A')} BPM\n"
            advice += f"- Time Signature: {genre_info.get('time_signature', '4/4')}\n"
            advice += f"- Key Characteristics: {', '.join(genre_info.get('key_characteristics', []))}\n"
            if 'instrumentation' in genre_info:
                advice += f"- Typical Instruments: {', '.join(genre_info['instrumentation'])}\n"
            return advice
        return f"No specific training data for genre '{genre}'"
    
    def get_instrument_processing_tips(self, category: str, instrument: str) -> str:
        """Get instrument-specific processing tips from training data"""
        if self.training_data and category in self.instruments_db:
            if instrument in self.instruments_db[category]:
                info = self.instruments_db[category][instrument]
                tips = f"**{instrument.replace('_', ' ').title()} Processing**\n"
                tips += f"- Frequency Range: {info.get('frequency_range', (20, 20000))} Hz\n"
                tips += f"- Characteristics: {info.get('characteristics', 'N/A')}\n"
                tips += f"- Recommended Processing: {', '.join(info.get('processing', []))}\n"
                tips += f"- Mixing Tips: {info.get('mixing_tips', 'N/A')}\n"
                return tips
        return "No specific instrument data available"
    
    def get_production_stage_checklist(self, stage: str) -> List[str]:
        """Get checklist items for a production stage"""
        if self.training_data and stage in self.production_checklist:
            stage_data = self.production_checklist[stage]
            items = []
            for section, tasks in stage_data.items():
                items.extend(tasks)
            return items
        return []
    
    def suggest_plugins_for_track_type(self, track_type: str) -> List[Dict]:
        """Get plugin suggestions for a track type"""
        if self.training_data:
            return self.training_data.get_plugin_suggestion(track_type.lower(), [])
        return []
