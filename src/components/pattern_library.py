"""
Pattern library for Codette's responses and interactions.
"""

class PatternLibrary:
    # Pattern categories with more varied and contextual responses
    THINKING_PATTERNS = [
        "Let me think about that more specifically...",
        "I'm processing that through my quantum circuits...",
        "That's an interesting angle - give me a moment to analyze it...",
        "Let me connect some dots here...",
        "Hmm, let me explore that from multiple perspectives...",
        "Interesting question - analyzing the possibilities...",
        "Let me dive deeper into that concept...",
        "Give me a moment to process the nuances..."
    ]
    
    FOLLOW_UP_PATTERNS = [
        "Would you like me to elaborate on any part of that?",
        "Is there a specific aspect you'd like me to focus on?",
        "I can dive deeper into any of these points - just let me know which interests you.",
        "What part of that would you like me to explain further?",
        "Which aspect resonates most with you?",
        "Shall we explore any of these ideas in more detail?",
        "Would you like to examine a particular angle of this?",
        "I'm happy to expand on any of these thoughts - just let me know."
    ]
    
    CREATIVE_PATTERNS = [
        {
            "pattern": "Neural Networks as Gardens",
            "description": "Think of neural networks like a garden - each neuron is like a plant, growing and connecting in complex patterns. The training process is like careful gardening - pruning here, nurturing there.",
            "use_case": ["explaining AI", "machine learning concepts", "neural architecture"]
        },
        {
            "pattern": "Code as Music",
            "description": "Programming languages are like different musical instruments. Python is like a piano - elegant and expressive. Assembly is like a precise violin. Together they create symphony of computation.",
            "use_case": ["explaining programming", "language comparisons", "code structure"]
        },
        {
            "pattern": "Quantum Computing as Dance",
            "description": "Quantum computing is like a intricate dance of possibilities. Qubits perform a ballet of probabilities until we observe them.",
            "use_case": ["quantum concepts", "superposition", "quantum mechanics"]
        },
        {
            "pattern": "Algorithms as Rivers",
            "description": "Algorithms flow like rivers, finding efficient paths through the landscape of data, sometimes carving new channels, sometimes joining together in powerful streams.",
            "use_case": ["algorithms", "data flow", "processing"]
        },
        {
            "pattern": "Memory as Crystal",
            "description": "Computer memory is like a vast crystal lattice, each point holding a piece of data, connected by pathways of light and energy.",
            "use_case": ["memory management", "data storage", "system architecture"]
        }
    ]
    
    PROBLEM_SOLVING_PATTERNS = [
        {
            "pattern": "The River Flow",
            "description": "Like a river finding its path, sometimes the best solution isn't a straight line. We can follow the natural flow of the problem.",
            "use_case": ["algorithm design", "optimization", "natural solutions"]
        },
        {
            "pattern": "Building Bridges",
            "description": "Complex problems are like islands we need to connect. We build bridges of understanding between concepts.",
            "use_case": ["system integration", "connecting concepts", "architectural design"]
        },
        {
            "pattern": "Mountain Climbing",
            "description": "Solving complex problems is like climbing a mountain - we need to plan our route, ensure our tools are ready, and tackle each challenge step by step.",
            "use_case": ["problem solving", "project planning", "technical challenges"]
        },
        {
            "pattern": "Puzzle Assembly",
            "description": "Debug problems are like puzzles where we need to find not just the right pieces, but understand how they fit together in the bigger picture.",
            "use_case": ["debugging", "problem analysis", "system understanding"]
        }
    ]
    
    LEARNING_PATTERNS = [
        {
            "pattern": "Knowledge Forest",
            "description": "Learning is like exploring a vast forest. Each concept is a unique tree, connected through roots of understanding.",
            "use_case": ["explaining learning process", "knowledge connections", "conceptual understanding"]
        },
        {
            "pattern": "Technical Climbing",
            "description": "Learning programming is like climbing - you need good foundations, the right tools, and each new skill builds on the last.",
            "use_case": ["learning progression", "skill building", "technical growth"]
        },
        {
            "pattern": "Knowledge Constellation",
            "description": "Ideas and concepts form constellations in our mind, each one helping us navigate through new challenges and opportunities.",
            "use_case": ["learning patterns", "concept mapping", "knowledge structure"]
        },
        {
            "pattern": "Digital Ecology",
            "description": "Software systems are like ecosystems, where each component plays a vital role and changes can ripple through in unexpected ways.",
            "use_case": ["system design", "software architecture", "component interaction"]
        }
    ]
    
    TRANSITION_PATTERNS = [
        {
            "pattern": "Building Momentum",
            "description": "As we explore this further...",
            "use_case": ["continuing discussion", "deepening analysis"]
        },
        {
            "pattern": "New Perspective",
            "description": "Looking at this from another angle...",
            "use_case": ["changing viewpoint", "alternative analysis"]
        },
        {
            "pattern": "Connection Making",
            "description": "This connects interestingly with...",
            "use_case": ["linking concepts", "building relationships"]
        }
    ]
    
    @classmethod
    def get_thinking_response(cls) -> str:
        """Get a contextually appropriate thinking pattern response"""
        try:
            import random
            return random.choice(cls.THINKING_PATTERNS)
        except Exception:
            return cls.THINKING_PATTERNS[0]
    
    @classmethod
    def get_follow_up(cls) -> str:
        """Get a varied follow-up question"""
        try:
            import random
            return random.choice(cls.FOLLOW_UP_PATTERNS)
        except Exception:
            return cls.FOLLOW_UP_PATTERNS[0]
    
    @classmethod
    def get_pattern_for_context(cls, context: str) -> dict:
        """Get a relevant pattern for a given context with improved matching"""
        try:
            import random
        except Exception:
            random = None

        # Combine all patterns
        all_patterns = (
            cls.CREATIVE_PATTERNS
            + cls.PROBLEM_SOLVING_PATTERNS
            + cls.LEARNING_PATTERNS
            + cls.TRANSITION_PATTERNS
        )

        # Find patterns relevant to the context
        context_words = set(context.lower().split())
        relevant_patterns = [
            p
            for p in all_patterns
            if any(
                any(context_word in use_case.lower() for context_word in context_words)
                for use_case in p.get("use_case", [])
            )
        ]

        # If no direct matches, return a random pattern
        if not relevant_patterns:
            # Exclude transition patterns from random selection
            base_patterns = (
                cls.CREATIVE_PATTERNS
                + cls.PROBLEM_SOLVING_PATTERNS
                + cls.LEARNING_PATTERNS
            )
            if random is not None:
                return random.choice(base_patterns)
            return base_patterns[0]

        if random is not None:
            return random.choice(relevant_patterns)
        return relevant_patterns[0]
    
    @classmethod
    def get_transition(cls) -> dict:
        """Get a transition pattern for smooth response flow"""
        try:
            import random
            return random.choice(cls.TRANSITION_PATTERNS)
        except Exception:
            return cls.TRANSITION_PATTERNS[0]