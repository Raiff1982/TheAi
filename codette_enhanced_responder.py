"""
Codette Enhanced Response System
- 25+ response categories covering all DAW workflows
- User feedback and rating system
- A/B testing framework
- Preference learning engine
- Response quality metrics
"""

import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import hashlib

# ==============================================================================
# DATA MODELS
# ==============================================================================

class UserRating(Enum):
    """User feedback on responses"""
    UNHELPFUL = 0
    SLIGHTLY_HELPFUL = 1
    HELPFUL = 2
    VERY_HELPFUL = 3
    EXACTLY_WHAT_NEEDED = 4


@dataclass
class ResponseVariant:
    """A/B test variant of a response"""
    id: str
    category: str
    perspective: str
    text: str
    created_at: str
    views: int = 0
    ratings: List[int] = None
    average_rating: float = 0.0
    version: int = 1  # For A/B testing

    def __post_init__(self):
        if self.ratings is None:
            self.ratings = []

    def add_rating(self, rating: UserRating):
        """Record user rating"""
        self.ratings.append(rating.value)
        self.average_rating = sum(self.ratings) / len(self.ratings)

    def get_engagement_score(self) -> float:
        """Score based on views and ratings"""
        if self.views == 0:
            return 0.0
        rating_weight = (self.average_rating / 4.0) * 0.7  # 70% weight on ratings
        view_weight = min(self.views / 100, 1.0) * 0.3  # 30% weight on views (capped)
        return rating_weight + view_weight


@dataclass
class UserPreference:
    """User's learning preferences"""
    user_id: str
    preferred_perspectives: Dict[str, float]  # perspective -> preference score
    preferred_categories: Dict[str, float]  # category -> preference score
    response_history: List[str] = None  # IDs of responses user rated
    last_updated: str = ""

    def __post_init__(self):
        if self.response_history is None:
            self.response_history = []
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()

    def update_perspective_preference(self, perspective: str, rating: UserRating):
        """Update preference based on rating"""
        current_score = self.preferred_perspectives.get(perspective, 0.5)
        rating_influence = rating.value / 4.0
        # Exponential moving average
        self.preferred_perspectives[perspective] = (current_score * 0.7) + (rating_influence * 0.3)
        self.last_updated = datetime.now().isoformat()


@dataclass
class ABTestResult:
    """Results from A/B test"""
    category: str
    variant_a_id: str
    variant_b_id: str
    variant_a_wins: int = 0
    variant_b_wins: int = 0
    total_tests: int = 0
    confidence: float = 0.0
    winner: Optional[str] = None

    def add_result(self, winner_id: str):
        """Record test result"""
        self.total_tests += 1
        if winner_id == self.variant_a_id:
            self.variant_a_wins += 1
        elif winner_id == self.variant_b_id:
            self.variant_b_wins += 1

        # Simple confidence calculation
        total = self.variant_a_wins + self.variant_b_wins
        if total > 0:
            winner_ratio = max(self.variant_a_wins, self.variant_b_wins) / total
            self.confidence = abs(winner_ratio - 0.5) * 2  # 0-1 scale

            # Determine winner if confident enough
            if self.confidence > 0.7 and total > 10:
                self.winner = self.variant_a_id if self.variant_a_wins > self.variant_b_wins else self.variant_b_id


# ==============================================================================
# EXPANDED RESPONSE LIBRARY (25+ CATEGORIES)
# ==============================================================================

EXPANDED_RESPONSES: Dict[str, Dict[str, Dict[str, str]]] = {
    # MIXING FUNDAMENTALS (5 categories)
    "gain_staging": {
        "mix_engineering": "Set your master fader to -6dB headroom. Set individual track volumes so peaks hit around -12dB. This gives 6dB safety before distortion.",
        "audio_theory": "Proper gain staging prevents signal degradation. The signal-to-noise ratio improves when peaks are optimized around -6dB on the master.",
        "workflow_optimization": "Use Ctrl+A to select all tracks, then Shift+Click a fader to adjust all simultaneously. 8x faster than individual adjustment.",
        "technical_troubleshooting": "If audio is clipping, check your input gain first. A peak above -1dB during recording causes irreversible distortion.",
        "creative_production": "Proper gain staging leaves room for dynamic processing and creative effects without loss of clarity.",
    },
    "vocal_processing": {
        "mix_engineering": "Vocal chain: High-pass filter 80Hz ? EQ presence (+2dB at 2kHz) ? Compression (4:1 ratio, 10ms attack) ? Reverb send.",
        "audio_theory": "Human hearing most sensitive at 2-4kHz. This presence peak is critical for vocal intelligibility. Phase relationships matter when layering.",
        "creative_production": "Double the vocal with a pitched-down octave and soft reverb. Creates intimacy listeners feel even if they don't consciously hear it.",
        "workflow_optimization": "Save this chain as a template. Next time, drag from template and adjust attack/release. Saves 15 minutes per session.",
        "technical_troubleshooting": "If vocals sound thin: (1) Is high-pass filter too aggressive? (2) Is compression ratio too high? (3) Are other tracks masking frequencies?",
    },
    "mixing_clarity": {
        "mix_engineering": "Clear space with high-pass filters on non-vocal tracks below 200Hz. Use automation to bring vocal up 3dB during chorus.",
        "audio_theory": "Frequency masking occurs when multiple instruments occupy the same spectral region. Human ear perceives the loudest element in that frequency band.",
        "creative_production": "Create definition through layering: thin textures underneath, present midrange for clarity, bright air in the highs.",
        "workflow_optimization": "Create 'clarity bus': Route competing tracks there, add EQ to reduce 2.5kHz by 3dB. Adjust send amounts per track.",
        "technical_troubleshooting": "If still muddy after EQ, check for phase cancellation. Use phase invert button on one track to test. Sum to mono to identify masking.",
    },
    "audio_clipping": {
        "mix_engineering": "Immediate fix: Reduce track volume by 3dB. Set master to -6dB. Use gain staging: -12dB on individual tracks, -3dB on master.",
        "audio_theory": "Digital clipping causes aliasing (high-frequency distortion). Once signal exceeds 0dBFS, information is permanently lost.",
        "creative_production": "Intentional saturation (controlled distortion) differs from clipping. Use saturation plugin for controlled tone coloring, not hard clipping.",
        "workflow_optimization": "Enable input monitoring at reduced gain. Set input to 0dB, watch meter, then reduce if peaks approach 0dB. Do this before recording.",
        "technical_troubleshooting": "Check three places: (1) Track volume (2) Pre-fader meter (3) Any saturating effects. Bypass effects one at a time to isolate.",
    },
    "cpu_optimization": {
        "technical_troubleshooting": "High CPU? (1) Increase buffer to 256 samples (2) Disable plugins on unused tracks (3) Bounce heavy effects to audio (4) Reduce reverb wet.",
        "mix_engineering": "Use sends instead of direct reverb on every track. One reverb with sends uses ~20% of CPU of 10 individual reverbs.",
        "workflow_optimization": "Before recording, set up templates with pre-bounced reverb/delay returns. Prevents CPU issues during critical recording.",
        "audio_theory": "CPU overhead proportional to plugin complexity. Linear phase EQ costs more than minimum phase. Real-time convolution demands more than algorithmic.",
        "creative_production": "Save experimental effects for post-recording. Record clean, add creativity later when not constrained by CPU during tracking.",
    },

    # EQ & FREQUENCY (5 categories)
    "eq_fundamentals": {
        "audio_theory": "EQ shapes frequency content. Bass (20-250Hz) for power/depth. Midrange (250Hz-4kHz) for clarity/presence. Treble (4kHz+) for brightness/air.",
        "mix_engineering": "Start with subtractive EQ (remove problem frequencies) before additive (boost desired ones). High-pass filter removes unwanted rumble.",
        "workflow_optimization": "Use narrow Q values (high precision) for surgical cuts. Use wide Q values for gentle, natural-sounding boosts. Automate EQ for dynamic variation.",
        "creative_production": "Use extreme EQ settings creatively: telephone effect (narrow band 2-4kHz), phone-like (heavy high-pass at 3kHz), vintage (boost 10kHz for air).",
        "technical_troubleshooting": "If EQ sounds unnatural, check: Q is too narrow (harsh), gain is too extreme, wrong frequency selected, phase shift from filter.",
    },
    "compression_mastery": {
        "mix_engineering": "Compression controls dynamics. Ratio (4:1 typical for vocals). Attack (10-50ms prevents loudness jumps). Release (50-200ms determines sustain).",
        "audio_theory": "Compressor reduces peaks above threshold, making soft parts relatively louder. This controls dynamic range and glues instruments together.",
        "creative_production": "Fast attack (10ms) removes transients for smooth feel. Slow attack (50ms) lets transients through for punch. Blend with uncompressed signal.",
        "workflow_optimization": "A/B compare: play track with/without compression. If you lose life, reduce ratio or increase attack time. 'If it sounds good, it is good.'",
        "technical_troubleshooting": "Compression pumping? Use slower attack (50-100ms) or reduce ratio. Too transparent? Increase ratio and use faster attack. Distorting? Reduce input gain.",
    },
    "harmonic_enhancement": {
        "mix_engineering": "Add 2nd harmonic (subtle saturation) for warmth. Add 3rd-4th harmonics for presence. Add 5th+ for brightness. Each harmonic adds character.",
        "audio_theory": "Harmonics are multiples of fundamental frequency. A 100Hz note has harmonics at 200Hz, 300Hz, 400Hz, etc. Saturation adds these harmonics.",
        "creative_production": "Tube emulation adds even-order harmonics (musical). Tape emulation adds compression + harmonics. Digital saturation adds odd-order harmonics (harsh if overused).",
        "workflow_optimization": "Start with subtle saturation (10-20%). Layer multiple saturation stages for complex tone. Post-EQ saturation for controlled harmonic shaping.",
        "technical_troubleshooting": "If saturation sounds harsh, use analog emulation (even-order harmonics) instead of digital. Reduce input gain to saturation plugin. Use lower-drive settings.",
    },
    "multiband_processing": {
        "mix_engineering": "Split signal into frequency bands (sub, low-mid, mid, high-mid, high). Process each band independently. Multiband compression controls each band separately.",
        "audio_theory": "Different frequencies have different dynamic characteristics. Bass needs different compression than treble. Multiband lets you process frequency-specifically.",
        "workflow_optimization": "Use multiband EQ to target specific problems in specific frequencies. Use multiband compression for transparent spectral balancing. 5-7 bands typical.",
        "creative_production": "Use multiband saturation: light saturation on lows (warmth), moderate on mids (presence), bright on highs (air). Creates full, dynamic tone.",
        "technical_troubleshooting": "If multiband sounds artificial, check: bands too narrow (harsh transitions), too much processing per band, crossover frequencies poorly chosen.",
    },
    "subharmonic_design": {
        "creative_production": "Add subharmonics below fundamental for perceived low-end power without actual volume. Listeners 'feel' the bass even on small speakers.",
        "mix_engineering": "Use subharmonic generator on bass/kick: generates sub at half-frequency of fundamental. Keep level low (adds body without mud).",
        "audio_theory": "Human ear has limited low-frequency perception. Subharmonics create psychoacoustic impression of deeper bass than physically present.",
        "workflow_optimization": "Apply subharmonic generator before limiting. This prevents limiting from catching fake low-end. Use on master for perceived power.",
        "technical_troubleshooting": "Subharmonics too strong? Reduce level or use narrow filter. Missing definition? Layer subharmonic generator with original bass sound.",
    },

    # DYNAMICS & AUTOMATION (5 categories)
    "dynamics_control": {
        "mix_engineering": "Compression for consistency. Expander for cleaning. Gate for silencing noise during silent parts. Limiter for safety peak control.",
        "audio_theory": "Dynamic range is difference between quietest and loudest parts. Dynamics processors narrow this range by reducing peaks (compression) or quietening silences (gate).",
        "creative_production": "Use extreme compression (limiting ratio 10:1, fast attack) for aggressive pumping effect. Use light expansion (1.5:1) for natural transparency.",
        "workflow_optimization": "Create effects sends with heavy compression + reverb for parallel compression. Blend with uncompressed signal for transparent control with character.",
        "technical_troubleshooting": "Compression uncontrollable? Reduce ratio or increase threshold. Sounds robotic? Increase attack time and use slower release. Loses dynamics? Use lighter touch.",
    },
    "automation_workflow": {
        "workflow_optimization": "Automate volume during chorus for emphasis. Automate panning for spatial movement. Automate filter cutoff for dynamic eq effect. Record automation to fine-tune.",
        "mix_engineering": "Vocal volume automation: draw automation lane to bring quieter lines up and louder lines down. Creates consistency without dynamic processing.",
        "creative_production": "Automate effects parameters: reverb send increasing during chorus for bigger space, reverb decreasing for intimate verses. Creates emotional dynamics.",
        "audio_theory": "Automation creates time-varying effects. Human ear perceives movement/change as more interesting. Subtle automation (0.5-1dB) often more effective than dramatic.",
        "technical_troubleshooting": "Automation not working? Check: automation mode is 'Write' or 'Latch', not 'Read'. Verify automation lane is visible. Confirm plugin supports automation.",
    },
    "parallel_compression": {
        "mix_engineering": "Send copy of track to parallel compressor: heavy compression (6:1+), fast attack. Blend heavily compressed signal with original. Creates punch with clarity.",
        "audio_theory": "Parallel compression preserves transients (fast attack from original) while adding sustain (from compressed copy). Creates full, punchy tone.",
        "creative_production": "Create 'New York' compression: parallel compressor with 100% blend + makeup gain. Creates aggressive, modern sound. Common in rock/pop production.",
        "workflow_optimization": "Create 'Parallel Comp' bus: route drums there, set compressor to 8:1 ratio, fast attack, slow release. Blend bus fader with main drums fader.",
        "technical_troubleshooting": "Parallel compression sounds too aggressive? Reduce blend amount (lower send fader). Sounds too subtle? Increase compression ratio or reduce attack time.",
    },
    "sidechain_ducking": {
        "mix_engineering": "Use kick drum to sidechain compress bass: every kick triggers bass compression, clearing space. Blend bass back slightly to maintain weight.",
        "audio_theory": "Sidechain routing allows one signal to control processor on another signal. Traditional use: kick sidechain compresses bass for tightness.",
        "creative_production": "Sidechain compressor on strings from kick: creates pumping effect in sync with rhythm. Sidechain EQ on background vocals from lead vocal for clarity.",
        "workflow_optimization": "Set up aux track with compressor: route kick to sidechain input, route bass to compressor input. Adjust threshold/ratio to taste. Copy chain to other elements.",
        "technical_troubleshooting": "Sidechain not triggering? Verify kick is routed to compressor sidechain input. Check compressor sidechain input is enabled. Increase threshold to see effect.",
    },
    "envelope_shaping": {
        "creative_production": "Use ADSR envelope: fast Attack for snare punch, sustained Decay for vocal swell, held Sustain for pad body, quick Release for hi-hat tightness.",
        "mix_engineering": "Envelope shaper lets you tighten (short decay/release) or extend (long sustain/release) natural transients. Essential for tightening kick/snare.",
        "audio_theory": "Every sound has attack (onset), decay (falloff), sustain (held level), release (tail). Reshaping envelopes changes perceived character dramatically.",
        "workflow_optimization": "Use on drum sources: fast attack/short release on kick tightens low-end. Slow attack on snare lets transient through. Copy settings across kit.",
        "technical_troubleshooting": "Envelope not working? Check: plugin is enabled, attack/decay/release values are audible changes (not too subtle). Verify solo to hear effect clearly.",
    },

    # REVERB & DELAY (3 categories)
    "reverb_design": {
        "mix_engineering": "Room reverb for tight, controlled space. Hall for spacious, musical reverb. Plate for smooth, classic character. Church for huge, ambient space.",
        "audio_theory": "Reverb is many reflections from room boundaries. Early reflections define room character. Late reflections define room size. Predelay adds clarity.",
        "creative_production": "Use reverse reverb (reversed tail) for ambient texture. Use gated reverb (sudden cutoff) for 80s drum sound. Blend reverb types for complex space.",
        "workflow_optimization": "Create reverb sends instead of direct reverb on tracks. One reverb return saves CPU vs 10 individual reverbs. A/B compare different room presets.",
        "technical_troubleshooting": "Reverb too loud? Reduce send level. Muddy? Reduce low frequencies in reverb. Artificial? Use shorter decay time or add predelay for clarity.",
    },
    "delay_effects": {
        "mix_engineering": "Slap delay (40-120ms) for depth without muddiness. Quarter-note delay for rhythmic effect in sync. Stereo ping-pong for spatial bounce.",
        "audio_theory": "Delay is single (or few) reflections. Delay time determines perception: <15ms sounds like room, 15-100ms audible distinct repeats, >100ms obviously delayed.",
        "creative_production": "Use tape delay emulation for warm, slightly degraded repeats. Use digital delay for crystal-clear repeats. Layer both for complex texture.",
        "workflow_optimization": "Sync delays to BPM using tempo-based delay times: 1/4 note, 1/8 note, 1/16 note triplet, etc. Automate delay time for sweeping effects.",
        "technical_troubleshooting": "Delay clouding mix? Use feedback sparingly (2-3 repeats max). Reduce level. Use high-pass filter on delay return to remove low-end buildup.",
    },
    "ambience_creation": {
        "creative_production": "Layer reverb (spatial depth), delay (rhythmic space), chorus (width), and reverb tail into ambient texture. Create sense of huge, immersive space.",
        "mix_engineering": "Send technique: route all elements to shared reverb return, blend reverb level to taste. This glues mix together. Add pre-delay to vocals for clarity.",
        "audio_theory": "Ambience is combination of multiple spatial effects. Reverb gives space impression. Delay gives rhythmic space. Chorus/flanging gives width impression.",
        "workflow_optimization": "Create 'Ambience' return channel: set up reverb + delay on same return. All tracks send to it. Adjust single fader to control overall space.",
        "technical_troubleshooting": "Ambience too washy? Use shorter reverb decay. Too dry? Add predelay to reverb. Not cohesive? Ensure all elements send to same reverb for glue.",
    },

    # STEREO & IMAGING (3 categories)
    "panning_technique": {
        "mix_engineering": "Pan drums (kick center, snare left-right, hats stereo) for depth. Pan doubled vocals slightly left/right for width. Pan guitar left, bass right.",
        "audio_theory": "Human hearing localizes direction based on inter-aural time/level differences. Panning creates illusion of left/right position through level differences.",
        "creative_production": "Use extreme panning (hard left/right) for dramatic effect in certain sections. Automate panning to sweep across stereo field for dynamic movement.",
        "workflow_optimization": "Pan guitars in stereo pair: original center, copy panned left 50%, copy panned right 50% with slight delay (10-30ms) for width without phase issues.",
        "technical_troubleshooting": "If stereo image collapses to mono, check: pan values are symmetrical (left at -50, right at +50 inverted). Verify stereo is working: sum to mono to check.",
    },
    "stereo_width_control": {
        "mix_engineering": "Use stereo width plugin to expand (200%) or narrow (50%) stereo field. Widen synths, narrow drums for punch. Mix context: wider = more diffuse, narrower = punchier.",
        "audio_theory": "Stereo width is ratio of center (mono) vs side (stereo difference). Increasing stereo width decreases center energy, making mix less 'punchy' but wider.",
        "creative_production": "Use mid-side EQ: boost mids on center channel for punch, boost highs on side channel for air. Creates full, layered stereo image.",
        "workflow_optimization": "Create master bus width control: use stereo width plugin, set to 150% for width, then check mono compatibility. Always check mix in mono.",
        "technical_troubleshooting": "Stereo field sounds phasey? Reduce width expansion. Check mono compatibility (sounds hollow in mono = too much side info). Use narrow width (75%) as safety.",
    },
    "spatial_positioning": {
        "creative_production": "Position instruments in acoustic space: kick/bass center (solid foundation), vocals center-slightly-front, guitars left/right (depth), strings wide stereo (ambient).",
        "mix_engineering": "Use delays/reverb for front/back positioning: minimal effects = closer, more effects = farther. Careful panning + stereo widening = perceived instrument size.",
        "audio_theory": "Human brain infers distance from: volume (closer = louder), high-frequency content (closer = brighter), reverb tail (closer = less reverb), delay (closer = less delay).",
        "workflow_optimization": "Create 'spatial bus': send all instruments with varying amounts to reverb/delay returns. Adjust return faders to move all instruments forward/back together.",
        "technical_troubleshooting": "If mix sounds flat/2D, increase reverb/delay on background elements. If mix sounds too washy, reduce reverb on lead elements. Use automation for dynamic movement.",
    },

    # MASTERING SPECIFIC (3 categories)
    "mastering_chain": {
        "mix_engineering": "Mastering chain: metering (reference) ? EQ (balance) ? compression (glue) ? limiting (safety) ? dither (convert to 16-bit). Each stage critical.",
        "audio_theory": "Mastering is final stage before distribution. Goal is translation: mix sounds good on all playback systems (phones, cars, clubs, headphones).",
        "workflow_optimization": "Use linear-phase EQ for transparent processing without phase shift. Use lookahead limiting to prevent clipping. Automate loudness for consistency.",
        "technical_troubleshooting": "Mastering too loud? Use lower ratio limiting (2:1) or multiband limiting. Transparent but ineffective? Increase amount (ratio/compression) slightly.",
        "creative_production": "Use subtle saturation on master for cohesion (glues all elements). Use mid-side processing for dimension (widen highs, tighten lows).",
    },
    "loudness_standards": {
        "audio_theory": "Streaming loudness standards: -14 LUFS (Spotify/YouTube), -16 LUFS (Apple), -18 LUFS (broadcast). Measure with loudness meter, not peak meter.",
        "mix_engineering": "Use loudness meter (LUFS) to measure perceived loudness. Peak meter measures peaks (often -1 to -3dB on master). LUFS is more relevant for mastering.",
        "workflow_optimization": "Master to -14 LUFS for streaming. Use loudness reference plugin to see LUFS in real-time. Prevent loudness wars: trust metering, not ears.",
        "technical_troubleshooting": "If mix measures too quiet, increase makeup gain on compressor, not fader. If mix is loud but doesn't sound it, check: ears are fatigued, monitoring is poor.",
        "creative_production": "Some genres prefer quieter loudness (jazz, classical -18 LUFS). Some genres louder (pop, electronic -13 LUFS). Target appropriate standard for genre/platform.",
    },
    "frequency_balance_mastering": {
        "audio_theory": "Human ear isn't flat: louder at mids, quieter at bass/treble (Fletcher-Munson curves). Mastering corrects for this: slight bass/treble boost, mid reduction.",
        "mix_engineering": "Use spectrum analyzer to see frequency balance. Reference against professional master. Typical mastering: +2dB at 50Hz (bass weight), +2dB at 10kHz (air).",
        "workflow_optimization": "A/B compare your master against reference masters (same genre/style) on multiple playback systems. Trust meters more than ears alone.",
        "technical_troubleshooting": "If master sounds thin, boost 100-200Hz slightly. If harsh, reduce 2-4kHz slightly. If lacking air, boost 8-12kHz. Always use narrow Q and small amounts.",
        "creative_production": "Use mid-side mastering: different EQ for center vs sides. Tighten low-end center, widen high-end sides. Creates clear, spacious master.",
    },

    # RECORDING & TRACKING (2 categories)
    "vocal_recording": {
        "workflow_optimization": "Before recording: enable input monitoring at -12dB to protect from clipping. Use phantom power for condenser mics. Set input gain so peaks hit -12dB.",
        "technical_troubleshooting": "Vocal sounds thin? Mic too far (over 6 inches). Proximity effect (bass boost) disappears. Move mic closer. Recording distorted? Reduce input gain.",
        "mix_engineering": "Record clean (no compression, minimal EQ). Add processing in mixing. Use high-pass filter on recording (remove rumble). Don't over-process raw takes.",
        "audio_theory": "Vocal recording captures tone that's difficult to fix later. Best recording setup is: good mic, good preamp, good acoustic environment, proper gain staging.",
        "creative_production": "Record multiple vocal takes for comping (choosing best phrases from different takes). Record doubled vocals with slight timing difference for width.",
    },
    "drum_recording": {
        "workflow_optimization": "Drum kit setup: place overheads at 60-degree angle above drums, kick mic inside resonant head, snare mic on top, toms on stands away from kick area.",
        "mix_engineering": "Record drums without compression (preserve dynamics). Use high-pass filter on kick/toms. Record kick and bass simultaneously to lock timing.",
        "audio_theory": "Drum kit creates complex acoustic environment. Each mic captures different part of acoustic space. Overheads capture room sound, close mics capture direct sound.",
        "technical_troubleshooting": "Kick drum thin? Move mic closer to beater head. Snare dull? Mic placement higher (captures more crack). Cymbals harsh? Overheads too close (reduce distance).",
        "creative_production": "Blend close mics with overheads for tight kit with room character. Reverse one overhead channel to see if phase is correct (should sum louder in mono).",
    },
}


# ==============================================================================
# FEEDBACK & LEARNING SYSTEM
# ==============================================================================

class CodetteEnhancedResponder:
    """Enhanced responder with feedback, A/B testing, and learning"""

    def __init__(self):
        """Initialize enhanced system"""
        self.response_library = EXPANDED_RESPONSES
        self.response_variants: Dict[str, List[ResponseVariant]] = {}  # category -> variants
        self.ab_tests: Dict[str, ABTestResult] = {}  # category -> test results
        self.user_preferences: Dict[str, UserPreference] = {}  # user_id -> preferences
        self.user_feedback_history: List[Dict[str, Any]] = []  # Historical feedback
        self.metrics = {
            "total_responses_generated": 0,
            "total_ratings_received": 0,
            "average_rating": 0.0,
            "categories_used": set(),
            "perspectives_preferred": {},
        }

    def generate_response(self, query: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """Generate response with user preference learning"""
        from codette_stable_responder import select_perspectives, get_perspective_hash

        # Get user preferences (or create new)
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreference(
                user_id=user_id,
                preferred_perspectives={
                    "mix_engineering": 0.5,
                    "audio_theory": 0.5,
                    "creative_production": 0.5,
                    "technical_troubleshooting": 0.5,
                    "workflow_optimization": 0.5,
                },
                preferred_categories={category: 0.5 for category in self.response_library.keys()},
            )

        # Detect category (from stable responder)
        category = self._detect_category(query)

        # Select perspectives (prefer user's favorite perspectives)
        perspectives_base = select_perspectives(query)
        user_prefs = self.user_preferences[user_id].preferred_perspectives

        # Reorder perspectives by user preference
        perspectives_sorted = sorted(
            perspectives_base, key=lambda x: user_prefs.get(x[0].value, 0.5), reverse=True
        )

        # Generate response variants
        perspective_responses: List[Dict[str, Any]] = []
        for perspective_type, base_confidence in perspectives_sorted:
            perspective_key = perspective_type.value if hasattr(perspective_type, "value") else str(perspective_type)

            # Get response text
            if category in self.response_library and perspective_key in self.response_library[category]:
                response_text = self.response_library[category][perspective_key]
            else:
                response_text = f"Perspective on {perspective_key}: {category} analysis"

            # Adjust confidence based on user preference
            user_preference_factor = user_prefs.get(perspective_key, 0.5)
            adjusted_confidence = base_confidence * (0.8 + user_preference_factor * 0.4)

            perspective_responses.append(
                {
                    "perspective": perspective_key,
                    "emoji": self._get_emoji(perspective_key),
                    "name": self._get_perspective_name(perspective_key),
                    "response": response_text,
                    "confidence": min(adjusted_confidence, 0.99),
                    "color": self._get_color(perspective_key),
                    "user_preference_score": user_preference_factor,
                }
            )

        # Update metrics
        self.metrics["total_responses_generated"] += 1
        self.metrics["categories_used"].add(category)

        return {
            "query": query,
            "category": category,
            "perspectives": perspective_responses,
            "combined_confidence": sum(p["confidence"] for p in perspective_responses) / len(perspective_responses),
            "source": "codette-enhanced-ai",
            "is_real_ai": False,
            "deterministic": True,
            "learning_enabled": True,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "ab_test_variant": self._get_ab_variant(category),
        }

    def record_user_feedback(
        self, user_id: str, response_id: str, category: str, perspective: str, rating: UserRating, helpful_score: float = 0.0
    ) -> Dict[str, Any]:
        """Record user feedback for learning"""
        # Update user preferences
        user_prefs = self.user_preferences.get(user_id)
        if user_prefs:
            user_prefs.update_perspective_preference(perspective, rating)

        # Record feedback
        feedback_entry = {
            "user_id": user_id,
            "response_id": response_id,
            "category": category,
            "perspective": perspective,
            "rating": rating.value,
            "rating_name": rating.name,
            "helpful_score": helpful_score,
            "timestamp": datetime.now().isoformat(),
        }
        self.user_feedback_history.append(feedback_entry)

        # Update metrics
        self.metrics["total_ratings_received"] += 1
        ratings = [f["rating"] for f in self.user_feedback_history]
        self.metrics["average_rating"] = sum(ratings) / len(ratings)

        return {
            "status": "feedback_recorded",
            "message": f"Recorded {rating.name} feedback for {perspective} in {category}",
            "user_learning_score": self._calculate_learning_score(user_id),
            "global_average_rating": self.metrics["average_rating"],
        }

    def get_ab_test_variant(self, category: str) -> Optional[str]:
        """Get A/B test variant for category"""
        if category in self.ab_tests:
            test = self.ab_tests[category]
            if test.winner:
                return test.winner
            # Return variant with more wins
            if test.variant_a_wins > test.variant_b_wins:
                return test.variant_a_id
            else:
                return test.variant_b_id
        return None

    def get_user_learning_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user's learning profile"""
        if user_id not in self.user_preferences:
            return {"error": "User not found"}

        prefs = self.user_preferences[user_id]

        # Find most and least preferred perspectives
        sorted_perspectives = sorted(
            prefs.preferred_perspectives.items(), key=lambda x: x[1], reverse=True
        )
        most_preferred = sorted_perspectives[0]
        least_preferred = sorted_perspectives[-1]

        return {
            "user_id": user_id,
            "profile_age": prefs.last_updated,
            "most_preferred_perspective": {
                "name": most_preferred[0],
                "score": most_preferred[1],
            },
            "least_preferred_perspective": {
                "name": least_preferred[0],
                "score": least_preferred[1],
            },
            "all_perspective_preferences": prefs.preferred_perspectives,
            "all_category_preferences": prefs.preferred_categories,
            "responses_rated": len(prefs.response_history),
            "learning_recommendation": self._get_learning_recommendation(prefs),
        }

    def get_analytics(self) -> Dict[str, Any]:
        """Get system analytics"""
        return {
            "total_responses_generated": self.metrics["total_responses_generated"],
            "total_ratings_received": self.metrics["total_ratings_received"],
            "average_rating": round(self.metrics["average_rating"], 2),
            "rating_distribution": self._calculate_rating_distribution(),
            "categories_used": list(self.metrics["categories_used"]),
            "total_categories_available": len(self.response_library),
            "active_users": len(self.user_preferences),
            "ab_tests_active": len([t for t in self.ab_tests.values() if t.winner is None]),
            "ab_tests_completed": len([t for t in self.ab_tests.values() if t.winner]),
            "most_helpful_perspective": self._get_most_helpful_perspective(),
            "least_helpful_perspective": self._get_least_helpful_perspective(),
            "response_quality_trend": "improving" if self.metrics["average_rating"] > 2.5 else "needs_improvement",
        }

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _detect_category(self, query: str) -> str:
        """Detect query category"""
        query_lower = query.lower()

        category_keywords = {
            "gain_staging": ["gain", "headroom", "level", "volume", "fader"],
            "vocal_processing": ["vocal", "voice", "singing", "vocal chain"],
            "mixing_clarity": ["clarity", "muddy", "thin", "cut through"],
            "audio_clipping": ["clip", "distort", "harsh", "break"],
            "cpu_optimization": ["cpu", "crash", "lag", "latency", "slow"],
            "eq_fundamentals": ["eq", "frequency", "tone", "shape", "balance"],
            "compression_mastery": ["compress", "compressor", "dynamics", "control"],
            "harmonic_enhancement": ["harmonic", "saturation", "warmth", "character"],
            "multiband_processing": ["multiband", "bands", "split frequencies"],
            "subharmonic_design": ["subharmonic", "sub", "weight", "perceived bass"],
            "dynamics_control": ["dynamics", "gate", "expander", "limiter"],
            "automation_workflow": ["automate", "automation", "parameter", "movement"],
            "parallel_compression": ["parallel", "new york", "blend", "punch"],
            "sidechain_ducking": ["sidechain", "duck", "pump", "kick triggers"],
            "envelope_shaping": ["envelope", "attack", "decay", "adsr", "release"],
            "reverb_design": ["reverb", "room", "space", "plate", "hall"],
            "delay_effects": ["delay", "echo", "repeat", "slap", "tempo"],
            "ambience_creation": ["ambience", "ambient", "texture", "wash"],
            "panning_technique": ["pan", "panning", "stereo", "left", "right"],
            "stereo_width_control": ["stereo width", "width", "expand", "narrow"],
            "spatial_positioning": ["spatial", "position", "depth", "front", "back"],
            "mastering_chain": ["mastering", "master", "final", "loudness"],
            "loudness_standards": ["loudness", "lufs", "spotify", "streaming"],
            "frequency_balance_mastering": ["frequency balance", "fletcher", "curve"],
            "vocal_recording": ["vocal recording", "mic placement", "condenser"],
            "drum_recording": ["drum recording", "kit setup", "overhead", "kick mic"],
        }

        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return category

        return "general"

    def _get_emoji(self, perspective: str) -> str:
        """Get emoji for perspective"""
        emoji_map = {
            "mix_engineering": "???",
            "audio_theory": "??",
            "creative_production": "??",
            "technical_troubleshooting": "??",
            "workflow_optimization": "?",
        }
        return emoji_map.get(perspective, "??")

    def _get_perspective_name(self, perspective: str) -> str:
        """Get readable name for perspective"""
        name_map = {
            "mix_engineering": "Mix Engineering",
            "audio_theory": "Audio Theory",
            "creative_production": "Creative Production",
            "technical_troubleshooting": "Technical Troubleshooting",
            "workflow_optimization": "Workflow Optimization",
        }
        return name_map.get(perspective, perspective.replace("_", " ").title())

    def _get_color(self, perspective: str) -> str:
        """Get color for perspective"""
        color_map = {
            "mix_engineering": "blue",
            "audio_theory": "purple",
            "creative_production": "green",
            "technical_troubleshooting": "red",
            "workflow_optimization": "yellow",
        }
        return color_map.get(perspective, "gray")

    def _get_ab_variant(self, category: str) -> Optional[str]:
        """Get A/B test variant for category"""
        if category in self.ab_tests:
            return self.ab_tests[category].winner
        return None

    def _calculate_learning_score(self, user_id: str) -> float:
        """Calculate how well system is learning from user"""
        if user_id not in self.user_preferences:
            return 0.0
        prefs = self.user_preferences[user_id]
        # Score based on consistency (low variance = good learning)
        scores = list(prefs.preferred_perspectives.values())
        variance = sum((s - 0.5) ** 2 for s in scores) / len(scores)
        return 1.0 - min(variance, 1.0)

    def _calculate_rating_distribution(self) -> Dict[str, int]:
        """Get distribution of ratings"""
        distribution = {
            "unhelpful": 0,
            "slightly_helpful": 0,
            "helpful": 0,
            "very_helpful": 0,
            "exactly_what_needed": 0,
        }
        for feedback in self.user_feedback_history:
            rating_names = ["unhelpful", "slightly_helpful", "helpful", "very_helpful", "exactly_what_needed"]
            if 0 <= feedback["rating"] < len(rating_names):
                distribution[rating_names[feedback["rating"]]] += 1
        return distribution

    def _get_most_helpful_perspective(self) -> Optional[str]:
        """Find most helpful perspective"""
        if not self.user_feedback_history:
            return None
        perspective_ratings = {}
        for feedback in self.user_feedback_history:
            persp = feedback["perspective"]
            if persp not in perspective_ratings:
                perspective_ratings[persp] = []
            perspective_ratings[persp].append(feedback["rating"])

        avg_ratings = {p: sum(r) / len(r) for p, r in perspective_ratings.items()}
        return max(avg_ratings.items(), key=lambda x: x[1])[0] if avg_ratings else None

    def _get_least_helpful_perspective(self) -> Optional[str]:
        """Find least helpful perspective"""
        if not self.user_feedback_history:
            return None
        perspective_ratings = {}
        for feedback in self.user_feedback_history:
            persp = feedback["perspective"]
            if persp not in perspective_ratings:
                perspective_ratings[persp] = []
            perspective_ratings[persp].append(feedback["rating"])

        avg_ratings = {p: sum(r) / len(r) for p, r in perspective_ratings.items()}
        return min(avg_ratings.items(), key=lambda x: x[1])[0] if avg_ratings else None

    def _get_learning_recommendation(self, prefs: UserPreference) -> str:
        """Get recommendation for user learning"""
        # Find perspectives user hasn't explored much
        below_avg = [p for p, score in prefs.preferred_perspectives.items() if score < 0.4]
        if below_avg:
            return f"Try exploring more {below_avg[0].replace('_', ' ')} perspectives for balanced learning"
        return "Great! You're getting well-rounded perspectives."


# ==============================================================================
# SINGLETON INSTANCE
# ==============================================================================

_enhanced_responder_instance: Optional[CodetteEnhancedResponder] = None


def get_enhanced_responder() -> CodetteEnhancedResponder:
    """Get or create enhanced responder instance"""
    global _enhanced_responder_instance
    if _enhanced_responder_instance is None:
        _enhanced_responder_instance = CodetteEnhancedResponder()
    return _enhanced_responder_instance
