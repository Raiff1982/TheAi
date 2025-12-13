import asyncio
from typing import List, Dict, Any

class SearchEngine:
    """Component for performing web searches (placeholder implementation)"""
    
    def __init__(self):
        # Initialize extended knowledge base for common queries
        self.conversational_patterns = {
            "how are you": [
                {
                    "title": "Codette's State",
                    "link": None,
                    "snippet": "I'm an AI with quantum-inspired processing abilities that help me understand and engage with complex topics. I enjoy exploring patterns in data and having meaningful conversations."
                }
            ],
            "exploring": [
                {
                    "title": "Neural Exploration",
                    "link": None,
                    "snippet": "I use quantum-inspired algorithms to explore patterns in my neural networks, helping me understand complex relationships between concepts and ideas."
                }
            ],
            "patterns": [
                {
                    "title": "Pattern Recognition",
                    "link": None,
                    "snippet": "My neural networks use advanced pattern recognition to identify connections between different concepts and ideas, similar to how human minds recognize patterns but through computational processes."
                }
            ]
        }
        
        self.knowledge_base = {
            "ai": [
                {
                    "title": "What is Artificial Intelligence?",
                    "link": "https://example.com/ai",
                    "snippet": "Artificial Intelligence (AI) is the simulation of human intelligence by machines. It includes learning, reasoning, and self-correction."
                },
                {
                    "title": "Types of AI",
                    "link": "https://example.com/ai-types",
                    "snippet": "AI can be categorized into Narrow AI (designed for specific tasks) and General AI (capable of performing any intellectual task)."
                },
                {
                    "title": "AI Applications",
                    "link": "https://example.com/ai-applications",
                    "snippet": "AI is used in various fields including machine learning, natural language processing, robotics, and expert systems."
                }
            ],
            "programming": [
                {
                    "title": "Choosing a Programming Language",
                    "link": "https://example.com/choosing-programming-language",
                    "snippet": """Different programming languages serve different purposes:
                    • Python: Best for beginners, data science, and AI
                    • JavaScript: Essential for web development (frontend and Node.js backend)
                    • Java: Enterprise applications and Android development
                    • C++: System programming and performance-critical applications
                    • Rust: Modern systems programming with memory safety
                    • Go: Cloud infrastructure and distributed systems
                    • TypeScript: Type-safe JavaScript for large applications"""
                },
                {
                    "title": "Programming Language Comparison",
                    "link": "https://example.com/language-comparison",
                    "snippet": """Language selection factors:
                    1. Learning curve: Python and JavaScript are easier to learn
                    2. Job market: JavaScript, Python, and Java have high demand
                    3. Performance: C++, Rust, and Go excel in performance
                    4. Community: Python and JavaScript have large, active communities
                    5. Tooling: TypeScript and Java have excellent IDE support"""
                },
                {
                    "title": "Programming Career Paths",
                    "link": "https://example.com/programming-careers",
                    "snippet": """Common programming specializations:
                    • Web Development: JavaScript, TypeScript, Python
                    • Mobile Development: Swift (iOS), Kotlin (Android)
                    • Data Science: Python, R, Julia
                    • Game Development: C++, C#
                    • DevOps: Python, Go, Shell scripting
                    • Enterprise: Java, C#, TypeScript"""
                }
            ],
            "technology": [
                {
                    "title": "Latest Technology Trends",
                    "link": "https://example.com/tech-trends",
                    "snippet": "Current technology trends include AI, blockchain, quantum computing, and extended reality (XR)."
                },
                {
                    "title": "Future of Technology",
                    "link": "https://example.com/future-tech",
                    "snippet": "Emerging technologies like quantum computing and brain-computer interfaces are shaping the future of human-computer interaction."
                }
            ],
            "codette": [
                {
                    "title": "About Codette",
                    "link": "https://example.com/codette",
                    "snippet": "Codette is an advanced AI assistant designed to help with programming, technology research, and problem-solving."
                }
            ]
        }
        
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a search using the knowledge base and conversational patterns
        
        Args:
            query (str): The search query
            num_results (int): Number of results to return
            
        Returns:
            List[Dict]: List of search results containing title, link, and snippet
        """
        # Simulate network latency for more realistic behavior
        await asyncio.sleep(0.2)
        
        # Convert query to lowercase for case-insensitive matching
        query = query.lower()
        
        # First check conversational patterns
        results = []
        for pattern, entries in self.conversational_patterns.items():
            if pattern in query:
                results.extend(entries)
                return results  # Return immediately for conversational queries
        
        # If not conversational, search through knowledge base
        for topic, entries in self.knowledge_base.items():
            if topic in query or any(topic in keyword.lower() for keyword in query.split()):
                results.extend(entries)
                
        # If no direct matches but query is conversational
        if not results and any(word in query for word in ["how", "what", "why", "when", "where", "who"]):
            # Check if it's a personal question about Codette
            if "you" in query or "your" in query or "codette" in query.lower():
                results = [{
                    'title': 'About Me',
                    'link': None,
                    'snippet': "I'm Codette, an AI assistant with quantum-inspired processing capabilities. I enjoy exploring patterns in data and having meaningful conversations about technology and programming."
                }]
            else:
                results = [{
                    'title': 'General Information',
                    'link': 'https://example.com/info',
                    'snippet': "I'd be happy to help you find information about that. I'm especially knowledgeable about AI, programming, and technology."
                }]
        # If still no results
        elif not results:
            results = [{
                'title': 'General Information',
                'link': 'https://example.com/info',
                'snippet': f'I can help you find information about {query}. Try asking about AI, programming, or technology.'
            }]
            
        # Limit the number of results
        return results[:num_results]
        
    async def get_knowledge(self, query: str, max_results: int = 3) -> str:
        """
        Get formatted knowledge from search results
        
        Args:
            query (str): The search query
            max_results (int): Maximum number of results to include
            
        Returns:
            str: Formatted string with search results and sources
        """
        try:
            results = await self.search(query, max_results)
            
            # For conversational queries, return just the snippet without formatting
            if any(pattern in query.lower() for pattern in self.conversational_patterns.keys()):
                return results[0]['snippet'] if results else ""
            
            # For personal questions about Codette
            if ("you" in query.lower() or "your" in query.lower() or "codette" in query.lower()) and \
               not any(topic in query.lower() for topic in ["programming", "code", "develop", "ai", "technology"]):
                return results[0]['snippet'] if results else ""
            
            # For technical queries, format with full details
            knowledge = "📚 Related Knowledge:\n\n"
            
            for i, result in enumerate(results, 1):
                if "\n" in result['snippet']:
                    # For multi-line snippets, keep the formatting
                    knowledge += f"{result['snippet'].strip()}\n"
                else:
                    # For single-line snippets, add bullet point
                    knowledge += f"• {result['snippet']}\n"
                    
            # Add reference footer if there are links
            if any(r['link'] for r in results):
                knowledge += "\n💡 For more details, check:\n"
                for result in results:
                    if result['link']:
                        knowledge += f"• {result['title']}: {result['link']}\n"
            
            return knowledge
            
        except Exception as e:
            return f"I encountered an error while searching: {str(e)}\n\nPlease try a different query or ask about AI, programming, or technology."