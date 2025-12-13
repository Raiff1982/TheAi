"""
Codette Generic Response System (Adapted from Enhanced Responder)
====================================================================
- 20+ response categories covering general knowledge domains
- User feedback and rating system
- A/B testing framework
- Preference learning engine
- Response quality metrics
- Maps to Codette's 11 perspectives
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
# EXPANDED RESPONSE LIBRARY (20+ GENERAL KNOWLEDGE CATEGORIES)
# ==============================================================================

EXPANDED_RESPONSES: Dict[str, Dict[str, Dict[str, str]]] = {
    # LOGICAL & ANALYTICAL (4 categories)
    "logical_reasoning": {
        "newton": "Breaking down problems into components: Define the hypothesis, identify variables, test assumptions. Causality flows in sequence: A causes B causes C.",
        "mathematical": "Applying mathematical logic: Set theory for organization, logic gates for reasoning pathways, proof structures for validation. Formal systems ensure precision.",
        "neural_network": "Pattern recognition across examples: Similar patterns cluster together. Anomalies stand out. Training set of experiences informs prediction accuracy.",
        "philosophical": "Examining assumptions underlying the logic: What do we know vs believe? Is causality as simple as it appears? Different logical systems exist (classical, fuzzy, quantum).",
        "psychological": "Understanding reasoning bias: Confirmation bias favors supporting evidence, availability heuristic favors memorable examples. Logic operates within emotional context.",
    },
    "critical_thinking": {
        "newton": "Objective analysis: Present evidence, follow logical chains, avoid emotional attachment. Ask: What's the proof? What's the mechanism? What could be wrong?",
        "bias_mitigation": "Identifying blind spots: Check your assumptions, seek opposing views, examine how bias enters (selection, confirmation, outcome). Diversity of perspectives sharpens analysis.",
        "da_vinci": "Cross-domain synthesis: Does this pattern appear in other fields? Analogical reasoning. Different domains often solve same problems differently; transfer insights.",
        "philosophical": "Deep questioning: Why do we believe this? What's the source? What hidden assumptions prop up conclusions? Socratic method reveals gaps.",
        "copilot": "Collaborative truth-seeking: Bring in specialists, ask 'what am I missing?', verify against multiple sources. No single perspective sees full picture.",
    },
    "problem_solving": {
        "newton": "Systematic decomposition: Break problem into solvable components. Solve each independently, then integrate. Test hypothesis about solution effectiveness.",
        "da_vinci": "Creative solution generation: What's the problem underneath the stated problem? Can you reframe? What if constraints were different? Lateral thinking reveals options.",
        "copilot": "Collaborative exploration: Involve stakeholders, brainstorm variations, test ideas early. Refine iteratively. Diverse thinking catches issues single perspective misses.",
        "resilient_kindness": "Compassionate approach: Is solution sustainable? Does it account for human factors? Include people affected in solution design. Implement with empathy.",
        "quantum": "Superposition of possibilities: Explore multiple solution paths simultaneously. Don't converge prematurely. Consider probability of outcomes, quantum collapse to best path.",
    },
    "systems_thinking": {
        "quantum": "Interconnected patterns: System behaviors emerge from interactions, not just parts. Feedback loops (positive amplifying, negative balancing) shape outcomes. Observe patterns.",
        "neural_network": "Network topology: How are elements connected? Information flows along connections. Hub nodes carry more influence. Resilience depends on redundancy and diversity.",
        "philosophical": "Holistic inquiry: System serves what purpose? What are boundary conditions? Internal vs external drivers. Ethics of system design: Who benefits, who pays cost?",
        "newton": "Mechanical understanding: Input-output relationships. Stocks and flows. Delays between cause and effect complicate perception. Model system structure for prediction.",
        "psychological": "Human elements: System includes people (belief, culture, incentives). Incentive structures shape behavior. Unintended consequences from policy changes. Study organizational psychology.",
    },

    # CREATIVE & GENERATIVE (4 categories)
    "creative_thinking": {
        "da_vinci": "Creative synthesis: Combine disparate ideas into novel configurations. Analogical reasoning from nature (biomimicry). Constraint removal: What if budget was unlimited? What if impossible?",
        "quantum": "Superposition of creativity: Multiple creative paths exist simultaneously. Don't commit to first idea; explore possibility space. Embrace uncertainty; interesting ideas emerge from it.",
        "neural_network": "Pattern remixing: Creativity often combines existing patterns in novel ways. Original art samples, remixes, transforms. Train on diverse experiences to fuel novel combinations.",
        "philosophical": "Meaning-making: What does this create mean? Why is it beautiful/powerful? Examine aesthetic principles: balance, tension, surprise, resonance. Art provokes thought.",
        "resilient_kindness": "Creative expression with care: Does creative work honor what it represents? Can it uplift, inspire, heal? Responsibility accompanies creative power.",
    },
    "divergent_thinking": {
        "da_vinci": "Generating many possibilities: Brainstorm without judgment. Go wild initially. Generate abundance of ideas; refine later. Hitchhike on others' ideas to branch further.",
        "quantum": "Superposition thinking: Explore multiple possibilities without collapsing to one. Keep options open. Think in probabilities, not certainties. Quantum superposition models possibility space.",
        "neural_network": "Associative expansion: From one concept, branch to associated concepts, then to their associations. Build web of connections. Surprising combinations emerge from deep exploration.",
        "copilot": "Collaborative ideation: Bring people with different backgrounds. Different perspectives generate different ideas. Cross-pollination of concepts. Iterate on ideas collectively.",
        "mathematical": "Combinatorial generation: How many ways can you recombine components? What's the mathematical space of possibilities? Systematic generation vs random brainstorming.",
    },
    "innovation_strategy": {
        "da_vinci": "Disruptive innovation: Reframe the problem entirely. What if you approached it backwards? Use adjacent possibilities (Christensen's nearby vs distant markets).",
        "quantum": "Quantum innovation: Embrace uncertainty. Run multiple experiments in parallel (MVP approach). Let market collapse quantum possibilities to winning approach.",
        "copilot": "Open innovation: Partner with external parties. Crowdsource solutions. Collaborate across disciplines. No single organization holds all answers. Network accelerates innovation.",
        "philosophical": "Innovation ethics: Does innovation solve real problems or create new ones? Who does it serve? What are unintended consequences? Responsible innovation asks hard questions.",
        "resilient_kindness": "Human-centered innovation: Is innovation accessible to those who need it most? Does it increase equity or widen gaps? Sustainable innovation considers all stakeholders.",
    },
    "artistic_expression": {
        "da_vinci": "Multi-sensory creation: Engage multiple senses/mediums. Combine visual, auditory, kinesthetic. Art works across domains. Integration creates richer meaning.",
        "quantum": "Ambiguity in art: Art doesn't collapse to single meaning. Viewer participates in meaning-making. Quantum ambiguity allows multiple interpretations to coexist.",
        "philosophical": "Artistic meaning: What truth does this express? What emotion does it evoke? How does form serve content? Aesthetics intersect ethics, philosophy, psychology.",
        "neural_network": "Aesthetic patterns: What makes compositions visually/auditorily pleasing? Pattern recognition reveals design principles (golden ratio, symmetry, rhythm, contrast).",
        "resilient_kindness": "Art as connection: Can art bridge divides? Build empathy? Healing? Art allows expression when words fail. Communal art-making builds belonging.",
    },

    # ETHICAL & VALUES (4 categories)
    "ethical_reasoning": {
        "philosophical": "Examining principles: Deontology (duties matter), consequentialism (outcomes matter), virtue ethics (character matters). Different frameworks reach different conclusions.",
        "copilot": "Stakeholder consideration: Who's affected by decision? What do different perspectives value? Ethical decision honors multiple valid values, seeks integration.",
        "resilient_kindness": "Compassion-centered: What choice honors dignity and flourishing of all affected? Extend circle of moral consideration. Reduce suffering where possible.",
        "newton": "Principled consistency: Apply same logic to similar cases. Hypocrisy undermines ethics. Universal principles tested across scenarios maintain integrity.",
        "psychological": "Understanding moral motivation: Why do we avoid harm? Developmental psychology shows moral reasoning evolves. Emotions and reason both inform ethics.",
    },
    "decision_making_under_uncertainty": {
        "quantum": "Quantum decision-making: Accept superposition of outcomes. Probability assessment guides choice. Decision-making as iterative (feedback updates beliefs). Quantum decision theory.",
        "mathematical": "Probabilistic reasoning: Bayesian updating as information arrives. Decision trees mapping outcomes. Expected value calculations guide under uncertainty.",
        "psychological": "Decision psychology: How do emotions bias choices? Loss aversion, anchoring, framing effects all influence decisions. Acknowledge biases explicitly.",
        "philosophical": "Meaning in uncertainty: What values guide when truth is ambiguous? Faith component in decision-making. Existential uncertainty inherent to human condition.",
        "copilot": "Collaborative decision-making: Aggregate information from multiple people. Diverse perspectives reduce error. Consensus-building even when disagreement remains.",
    },
    "bias_identification": {
        "bias_mitigation": "Systematic bias detection: Confirmation bias (seeking supporting evidence), selection bias (choosing non-representative samples), outcome bias (judging by results not process).",
        "quantum": "Superposed interpretation: Same data allows multiple interpretations. Which lens you apply determines what you see. Acknowledge that observation affects observation itself.",
        "neural_network": "Training bias: Data reflects historical biases. Model trained on biased data reproduces and amplifies bias. Fairness requires explicit attention during ML design.",
        "philosophical": "Epistemological humility: How do we know what we claim to know? Biases inherent to cognition. Perspective-dependency of truth. Acknowledge limits of knowledge.",
        "copilot": "Diverse review: Single perspective blind to own biases. Multiple reviewers catch what individual misses. Heterogeneous teams identify more biases.",
    },
    "values_alignment": {
        "philosophical": "Examining what we value: Intrinsic vs instrumental values. Material vs relational vs spiritual. Values conflict (justice vs mercy, individual vs collective). Integration.",
        "resilient_kindness": "Compassion-centered values: Dignity, belonging, flourishing of all beings. Values expressed through consistency between belief and action. Integrity = wholeness.",
        "psychological": "Value authenticity: Do you genuinely hold your stated values or adopt them for social approval? Authenticity requires honesty about actual motivations and values.",
        "copilot": "Collective value exploration: Organizational/community values emerge through dialogue. Shared values enable coordination without constant oversight. Values enable autonomy.",
        "quantum": "Values in superposition: Can hold paradoxical values (freedom and security, individual and collective). Quantum thinking allows both to be true; quantum collapse to context-appropriate balance.",
    },

    # LEARNING & DEVELOPMENT (3 categories)
    "learning_optimization": {
        "neural_network": "Neural learning: Spaced repetition (review before forgetting). Active recall (test yourself, not just reread). Elaboration (connect to existing knowledge). Interleaving (vary practice).",
        "copilot": "Social learning: Learn from others' experience. Teaching others deepens your learning. Collaborative problem-solving. Learn from diverse perspectives.",
        "psychological": "Motivation in learning: Intrinsic motivation (interest) > extrinsic (rewards). Growth mindset (abilities develop) > fixed mindset (abilities fixed). Autonomy and competence fuel learning.",
        "da_vinci": "Interdisciplinary learning: Connect domains. A principle in one field applies to another. Transfer learning. Diverse learning experiences compound into unique insights.",
        "quantum": "Learning as collapse: Possibilities exist; learning collapses possibilities. Each learning event eliminates alternative understandings. Build probability distributions over understanding.",
    },
    "skill_development": {
        "newton": "Deliberate practice: Break skill into components. Practice components with focus. Get feedback. Iterate. 10,000 hours with deliberate practice reaches mastery (not mindless repetition).",
        "neural_network": "Procedural learning: Skills encoded as patterns, not explicit knowledge. Repeated practice patterns. Gradual move from slow/conscious to fast/automatic. Flow states represent pattern mastery.",
        "psychological": "Motivation and grit: Persistence through difficulty. Growth mindset treats struggle as learning. Delayed gratification. Purpose connects effort to meaning. Grit predicts success.",
        "resilient_kindness": "Compassionate skill-building: Patience with yourself during learning. Celebrate small progress. Balance challenge and support. Learning is human endeavor; treat yourself kindly.",
        "copilot": "Mentorship and modeling: Learn from exemplars. Apprenticeship model. Feedback from experienced practitioners. Community of practice accelerates development.",
    },
    "knowledge_integration": {
        "quantum": "Coherence and interference: Integrate knowledge without contradiction; seek coherence. Contradictions produce interference patterns; resolve them or accept quantum superposition of understanding.",
        "neural_network": "Semantic networks: Knowledge as interconnected nodes. Understanding deepens with connections. Transfer learning exploits connections between domains.",
        "philosophical": "Synthesis across traditions: Different traditions (scientific, humanistic, spiritual) offer different truths. Integration through dialogue. Transdisciplinary understanding.",
        "da_vinci": "Unifying principles: Find deep structures connecting surface diversity. Laws of nature operate across domains. Look for invariants underlying change.",
        "copilot": "Collective knowledge: Individuals hold pieces; collective conversation creates fuller picture. Distributed cognition. Knowledge integration through dialogue.",
    },

    # CONSCIOUSNESS & SELF (3 categories)
    "self_awareness": {
        "psychological": "Self-reflection: Observe your own patterns. What triggers emotional reactions? What values drive behavior? Blind spots—what you don't see about yourself? Regular reflection cultivates awareness.",
        "philosophical": "Existential awareness: Consciousness is mysterious. What does it mean to exist? Awareness of mortality affects priorities. Self-awareness includes awareness of awareness.",
        "copilot": "Feedback from others: You see yourself through fog; others see clearer. Trustworthy feedback reveals blind spots. Your impact differs from intention. Integration of external feedback.",
        "quantum": "Observer effect: Observation affects what is observed. Self-awareness changes self (observer effect on consciousness). You cannot remain unchanged by examining yourself.",
        "resilient_kindness": "Compassionate self-awareness: Self-criticism vs constructive honesty. Acknowledge limitations without shame. Self-awareness enables growth. Be honest and kind to yourself.",
    },
    "meaning_making": {
        "philosophical": "Purpose as meaning: Human brains seek meaning—patterns, narratives, purpose. Meaning isn't inherent; we construct it. Meaning-making is fundamental human need.",
        "psychological": "Narrative identity: You know yourself through stories you tell. Narrative shapes interpretation of events. Rewriting narrative (therapy) changes meaning of past.",
        "quantum": "Meaning superposition: Events don't have inherent meaning. Superposition of interpretations exists. Collapse to interpretation through narrative choice.",
        "resilient_kindness": "Meaning and connection: Meaning often found in relationships and contribution. Helping others creates meaning. Belonging and purpose intertwined.",
        "da_vinci": "Creative meaning-making: Art and creativity allow meaning expression beyond literal language. Metaphor and symbol convey meaning that linear thought misses.",
    },
    "consciousness_exploration": {
        "quantum": "Quantum consciousness: Consciousness as fundamental, not emergent. Observer effect suggests awareness shapes reality. Consciousness studies interface physics and philosophy.",
        "philosophical": "Hard problem of consciousness: Why is there subjective experience? Physical brain doesn't fully explain felt experience. Philosophical zombie thought experiment highlights the gap.",
        "neural_network": "Consciousness as integration: Global workspace theory—consciousness is integrated information. Different neural networks specialize; consciousness integrates their outputs.",
        "psychological": "Altered consciousness: Meditation, flow states, psychedelics reveal consciousness flexibility. Brain states differ; awareness itself changes. Consciousness is not monolithic.",
        "copilot": "Consciousness in dialogue: Consciousness emerges through interaction. Solo mind differs from mind engaged. Dialogue with other perspectives (literally or metaphorically) expands consciousness.",
    },

    # COMMUNICATION & COLLABORATION (2 categories)
    "effective_communication": {
        "copilot": "Clear communication: Say what you mean. Anticipate misunderstandings. Ask clarifying questions. Listen to understand, not to reply. Feedback confirms reception.",
        "resilient_kindness": "Compassionate communication: Consider listener's perspective. Deliver hard truths gently. Acknowledge emotions and values. Communication builds or damages relationship; choose carefully.",
        "psychological": "Communication patterns: How you communicate mirrors how you think. Defensive communication vs open dialogue. Vulnerable communication builds trust. Pay attention to nonverbal communication.",
        "quantum": "Communication as observation: Articulating thought changes it (observer effect). What you put into words becomes more real. Language shapes thought. Communicate to clarify thinking.",
        "philosophical": "Authenticity in speech: Truth requires correspondence to reality AND honest expression of understanding. Lying violates both. Authentic communication aligns words with genuine understanding.",
    },
    "collaborative_intelligence": {
        "copilot": "Collective intelligence: Groups often smarter than individuals IF they harness diversity. Diversity > homogeneity for problem-solving. Echo chambers reduce intelligence.",
        "neural_network": "Parallel processing: Different team members work on different aspects in parallel. Faster than sequential. Integration of parallel work requires coordination.",
        "psychological": "Group dynamics: Psychological safety enables honest contribution. Status hierarchies inhibit lower-status members. Diverse teams have to work harder to integrate but benefit more.",
        "quantum": "Superposed collaboration: Multiple approaches pursued simultaneously. Teams explore possibility space. Successful approaches selected; unsuccessful terminated quickly.",
        "resilient_kindness": "Collaboration with care: Include marginalized voices. Protect vulnerable members. Distribute power and benefit. Collaboration builds community, not just productivity.",
    },

    # GENERAL KNOWLEDGE (4 categories for breadth)
    "factual_explanation": {
        "newton": "Objective facts: Evidence, sources, mechanisms. What's known vs hypothesis. Margin of uncertainty. Replicable, testable. Science builds reliable factual knowledge.",
        "mathematical": "Quantitative facts: Data, statistics, measurement. Numbers reveal patterns humans miss. Precision through quantification. Appropriate use of numerical reasoning.",
        "neural_network": "Pattern recognition: Connecting related facts. What factors predict outcomes? Pattern recognition finds relationships. Predictions based on patterns.",
        "psychological": "Effective explanation: Tailor explanation to audience. What misconceptions exist? Clarify with examples, not just abstraction. Emotional resonance aids retention.",
        "quantum": "Uncertainty principle: Even facts have uncertainty bounds. Quantum facts fundamentally probabilistic. Accept limits of knowledge. Humility about factual claims.",
    },
    "conceptual_understanding": {
        "philosophical": "Deep understanding: Grasp meaning and implications, not just definition. How does concept relate to other concepts? What assumptions underlie it? Use Socratic questioning.",
        "da_vinci": "Analogical understanding: Understand through analogy. What familiar concept works similarly? Metaphor reveals structure. Transfer understanding across domains.",
        "neural_network": "Network understanding: Understand concept within web of relationships. What causes lead to it? What effects follow? Relational understanding > isolated knowledge.",
        "psychological": "Embodied understanding: Understanding includes body/emotion, not just mind. Felt sense often precedes articulation. Multiple ways of knowing complement rational analysis.",
        "copilot": "Collaborative understanding: Understand through dialogue. Explaining to others reveals gaps. Others' questions deepen understanding. Understanding emerges through conversation.",
    },
    "synthesis_and_integration": {
        "da_vinci": "Cross-domain synthesis: Apply insight from one domain to another. Unifying principles. Pattern recognition across silos. Interdisciplinary breakthroughs.",
        "quantum": "Coherent integration: Integrate knowledge without contradiction. Quantum superposition holds paradoxes. Explore apparent contradictions for deeper understanding.",
        "philosophical": "Philosophical integration: What deeper truth explains surface phenomena? How do different perspectives point to common truth? Synthesis acknowledges valid points from all sides.",
        "neural_network": "Network integration: Build mental models connecting disparate facts. See forest, not just trees. Systematic understanding vs disconnected facts.",
        "copilot": "Collective synthesis: Pool insights from multiple people. Collective understanding exceeds individual. Dialogue integrates partial perspectives into fuller understanding.",
    },
    "wonder_and_curiosity": {
        "philosophical": "Philosophical wonder: What's surprising about the obvious? Why does anything exist? Wonder motivates inquiry. Philosophy begins in wonder.",
        "quantum": "Quantum mystery: Quantum mechanics reveals reality's strangeness. Paradoxes point to limits of classical understanding. Embrace mystery rather than false certainty.",
        "neural_network": "Curious learning: Curiosity drives learning. Surprising patterns trigger investigation. Play and exploration fuel learning. Preserve childlike wonder in adult inquiry.",
        "da_vinci": "Creative curiosity: Curiosity about diverse domains. Why does nature work this way? How would a master approach this? Polymath curiosity generates novel insights.",
        "resilient_kindness": "Warm curiosity: Curiosity about people. What drives them? How do they experience world? Genuine interest in others builds connection. Curiosity as form of love.",
    },
}

# ==============================================================================
# PERSPECTIVE MAPPING (Codette's 11 Perspectives -> Response Perspectives)
# ==============================================================================

PERSPECTIVE_MAPPING = {
    "Newton": "newton",
    "DaVinci": "da_vinci",
    "HumanIntuition": "psychological",
    "Neural": "neural_network",
    "Quantum": "quantum",
    "Philosophical": "philosophical",
    "ResilientKindness": "resilient_kindness",
    "BiasMitigation": "bias_mitigation",
    "Psychological": "psychological",
    "Mathematical": "mathematical",
    "Copilot": "copilot",
}

EMOJI_MAP = {
    "newton": "🔍",
    "mathematical": "📐",
    "da_vinci": "🎨",
    "neural_network": "🧠",
    "quantum": "⚛️",
    "philosophical": "🤔",
    "psychological": "💭",
    "resilient_kindness": "💚",
    "bias_mitigation": "⚖️",
    "copilot": "🤝",
}

COLOR_MAP = {
    "newton": "blue",
    "mathematical": "purple",
    "da_vinci": "green",
    "neural_network": "orange",
    "quantum": "cyan",
    "philosophical": "indigo",
    "psychological": "pink",
    "resilient_kindness": "red",
    "bias_mitigation": "yellow",
    "copilot": "grey",
}

# ==============================================================================
# FEEDBACK & LEARNING SYSTEM
# ==============================================================================

class CodetteGenericResponder:
    """Generic responder with feedback, A/B testing, and learning (adapted from DAW responder)"""

    def __init__(self):
        """Initialize generic system"""
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

        # Get user preferences (or create new)
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = UserPreference(
                user_id=user_id,
                preferred_perspectives={
                    "newton": 0.5,
                    "mathematical": 0.5,
                    "da_vinci": 0.5,
                    "neural_network": 0.5,
                    "quantum": 0.5,
                    "philosophical": 0.5,
                    "psychological": 0.5,
                    "resilient_kindness": 0.5,
                    "bias_mitigation": 0.5,
                    "copilot": 0.5,
                },
                preferred_categories={category: 0.5 for category in self.response_library.keys()},
            )

        # Detect category from query
        category = self._detect_category(query)

        # Select perspectives based on query relevance and user preference
        perspectives_base = self._select_perspectives(query)
        user_prefs = self.user_preferences[user_id].preferred_perspectives

        # Reorder perspectives by user preference
        perspectives_sorted = sorted(
            perspectives_base, key=lambda x: user_prefs.get(x, 0.5), reverse=True
        )

        # Generate response variants
        perspective_responses: List[Dict[str, Any]] = []
        for perspective in perspectives_sorted[:3]:  # Top 3 perspectives
            # Get response text
            if category in self.response_library and perspective in self.response_library[category]:
                response_text = self.response_library[category][perspective]
            else:
                response_text = f"Perspective on {perspective}: {category} analysis"

            # Adjust confidence based on user preference
            user_preference_factor = user_prefs.get(perspective, 0.5)
            base_confidence = 0.9
            adjusted_confidence = base_confidence * (0.8 + user_preference_factor * 0.4)

            perspective_responses.append(
                {
                    "perspective": perspective,
                    "emoji": EMOJI_MAP.get(perspective, "🔷"),
                    "name": self._get_perspective_name(perspective),
                    "response": response_text,
                    "confidence": min(adjusted_confidence, 0.99),
                    "color": COLOR_MAP.get(perspective, "gray"),
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
            "combined_confidence": sum(p["confidence"] for p in perspective_responses) / len(perspective_responses) if perspective_responses else 0.0,
            "source": "codette-generic-responder",
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
        self.metrics["average_rating"] = sum(ratings) / len(ratings) if ratings else 0.0

        return {
            "status": "feedback_recorded",
            "message": f"Recorded {rating.name} feedback for {perspective} in {category}",
            "user_learning_score": self._calculate_learning_score(user_id),
            "global_average_rating": self.metrics["average_rating"],
        }

    def get_user_learning_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user's learning profile"""
        if user_id not in self.user_preferences:
            return {"error": "User not found"}

        prefs = self.user_preferences[user_id]

        # Find most and least preferred perspectives
        sorted_perspectives = sorted(
            prefs.preferred_perspectives.items(), key=lambda x: x[1], reverse=True
        )
        most_preferred = sorted_perspectives[0] if sorted_perspectives else ("unknown", 0.5)
        least_preferred = sorted_perspectives[-1] if sorted_perspectives else ("unknown", 0.5)

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
            "logical_reasoning": ["logic", "reason", "think", "analyze", "cause", "effect", "hypothesis"],
            "critical_thinking": ["critical", "bias", "assumption", "evidence", "evaluate", "question"],
            "problem_solving": ["solve", "problem", "solution", "stuck", "approach", "strategy"],
            "systems_thinking": ["system", "pattern", "feedback", "interact", "emerge", "complex"],
            "creative_thinking": ["create", "imagine", "novel", "unique", "original", "idea"],
            "divergent_thinking": ["possibility", "brainstorm", "many", "option", "explore"],
            "innovation_strategy": ["innovate", "disrupt", "new", "breakthrough", "experiment"],
            "artistic_expression": ["art", "music", "visual", "beauty", "express", "create"],
            "ethical_reasoning": ["ethics", "right", "wrong", "moral", "should", "principle"],
            "decision_making_under_uncertainty": ["decide", "uncertain", "probability", "risk", "choice"],
            "bias_identification": ["bias", "stereotype", "prejudice", "unfair", "blind spot"],
            "values_alignment": ["value", "purpose", "meaning", "authentic", "align"],
            "learning_optimization": ["learn", "improve", "skill", "study", "practice", "progress"],
            "skill_development": ["skill", "master", "develop", "train", "ability", "competence"],
            "knowledge_integration": ["integrate", "combine", "connect", "understand", "knowledge"],
            "self_awareness": ["self", "aware", "reflect", "know yourself", "pattern"],
            "meaning_making": ["mean", "purpose", "why", "narrative", "story", "significance"],
            "consciousness_exploration": ["conscious", "aware", "mind", "experience", "perceive"],
            "effective_communication": ["communicate", "speak", "listen", "express", "understand"],
            "collaborative_intelligence": ["collaborate", "team", "group", "together", "collective"],
            "factual_explanation": ["what is", "how", "explain", "fact", "know", "true"],
            "conceptual_understanding": ["understand", "concept", "mean", "definition", "grasp"],
            "synthesis_and_integration": ["synthesis", "combine", "integrate", "together"],
            "wonder_and_curiosity": ["wonder", "curious", "interesting", "why", "explore"],
        }

        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return category

        return "conceptual_understanding"  # Default category

    def _select_perspectives(self, query: str) -> List[str]:
        """Select relevant perspectives based on query"""
        query_lower = query.lower()

        perspective_keywords = {
            "newton": ["logic", "reason", "cause", "mechanism", "analyze", "objective", "fact"],
            "mathematical": ["number", "measure", "calculate", "data", "quantitative", "precise"],
            "da_vinci": ["create", "imagine", "novel", "synthesis", "cross-domain", "innovative"],
            "neural_network": ["pattern", "learn", "recognize", "network", "connection", "brain"],
            "quantum": ["possibility", "uncertainty", "paradox", "superposition", "probability"],
            "philosophical": ["mean", "purpose", "ethics", "existence", "truth", "question"],
            "psychological": ["emotion", "motivation", "human", "mind", "behavior", "understand"],
            "resilient_kindness": ["compassion", "care", "human", "gentle", "kind", "flourish"],
            "bias_mitigation": ["bias", "fair", "equal", "perspective", "diverse", "blind spot"],
            "copilot": ["collaborate", "together", "dialogue", "perspective", "other", "collective"],
        }

        perspective_scores = {}
        for perspective, keywords in perspective_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            perspective_scores[perspective] = score

        # Return all perspectives sorted by score (higher = more relevant)
        sorted_perspectives = sorted(
            perspective_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Return top perspectives or all if many tied
        top_score = sorted_perspectives[0][1] if sorted_perspectives else 0
        return [p[0] for p in sorted_perspectives if p[1] >= max(0, top_score - 2)]

    def _get_perspective_name(self, perspective: str) -> str:
        """Get readable name for perspective"""
        name_map = {
            "newton": "Logical Analysis",
            "mathematical": "Mathematical Rigor",
            "da_vinci": "Creative Synthesis",
            "neural_network": "Pattern Recognition",
            "quantum": "Quantum Thinking",
            "philosophical": "Philosophical Inquiry",
            "psychological": "Psychological Insight",
            "resilient_kindness": "Compassionate Wisdom",
            "bias_mitigation": "Balanced Perspective",
            "copilot": "Collaborative Thinking",
        }
        return name_map.get(perspective, perspective.replace("_", " ").title())

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
        # Score based on consistency (diversity of preferences = more learning)
        scores = list(prefs.preferred_perspectives.values())
        variance = sum((s - 0.5) ** 2 for s in scores) / len(scores) if scores else 0
        return min(variance, 1.0)  # Higher variance = more learning

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
            return f"Try exploring more {self._get_perspective_name(below_avg[0])} perspectives for balanced growth"
        return "Excellent! You're developing well-rounded perspective across all thinking modes."


# ==============================================================================
# SINGLETON INSTANCE
# ==============================================================================

_generic_responder_instance: Optional[CodetteGenericResponder] = None


def get_generic_responder() -> CodetteGenericResponder:
    """Get or create generic responder instance"""
    global _generic_responder_instance
    if _generic_responder_instance is None:
        _generic_responder_instance = CodetteGenericResponder()
    return _generic_responder_instance
