"""
AI-Driven Creativity Component for Codette
Handles creative generation and novel idea synthesis
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import random

logger = logging.getLogger(__name__)

try:
    import numpy as np
except Exception:
    np = None

class AIDrivenCreativity:
    """Manages AI-driven creative processes for Codette"""
    
    def __init__(self,
                 creativity_threshold: float = 0.7,
                 novelty_weight: float = 0.6,
                 memory_depth: int = 100):
        """Initialize the creativity engine"""
        self.creativity_threshold = creativity_threshold
        self.novelty_weight = novelty_weight
        self.memory_depth = memory_depth
        
        # Initialize state
        self.creative_memory = []
        self.idea_patterns = {}
        self.current_state = {
            "creativity_level": 1.0,
            "exploration_phase": "divergent",
            "pattern_recognition": {},
            "active_concepts": set()
        }
        
        logger.info("AI-Driven Creativity engine initialized")
        
    def generate_creative_response(self,
                                 input_data: Dict[str, Any],
                                 context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a creative response to input"""
        try:
            # Process input
            processed_input = self._process_input(input_data)
            
            # Generate ideas
            ideas = self._generate_ideas(processed_input, context)
            
            # Evaluate and select best ideas
            evaluated_ideas = self._evaluate_ideas(ideas)
            
            # Synthesize final response
            response = self._synthesize_response(evaluated_ideas)
            
            # Update memory and patterns
            self._update_memory(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating creative response: {e}")
            return {"error": str(e)}
            
    def _process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and analyze input for creative potential"""
        try:
            # Extract key concepts
            concepts = self._extract_concepts(input_data)
            
            # Analyze patterns
            patterns = self._analyze_patterns(concepts)
            
            # Calculate creative potential
            creative_potential = self._calculate_creative_potential(concepts, patterns)
            
            return {
                "concepts": concepts,
                "patterns": patterns,
                "creative_potential": creative_potential,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return {}
            
    def _generate_ideas(self,
                       processed_input: Dict[str, Any],
                       context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Generate multiple creative ideas"""
        ideas = []
        try:
            concepts = processed_input.get("concepts", [])
            patterns = processed_input.get("patterns", {})
            
            # Generate through different methods
            ideas.extend(self._generate_by_combination(concepts))
            ideas.extend(self._generate_by_analogy(concepts, patterns))
            ideas.extend(self._generate_by_mutation(concepts))
            
            if context:
                ideas.extend(self._generate_contextual_ideas(concepts, context))
                
        except Exception as e:
            logger.error(f"Error generating ideas: {e}")
            
        return ideas
        
    def _evaluate_ideas(self,
                       ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluate and rank generated ideas"""
        try:
            evaluated_ideas = []
            for idea in ideas:
                # Calculate metrics
                novelty = self._calculate_novelty(idea)
                usefulness = self._calculate_usefulness(idea)
                coherence = self._calculate_coherence(idea)
                
                # Combine scores
                total_score = (
                    novelty * self.novelty_weight +
                    usefulness * 0.3 +
                    coherence * 0.1
                )
                
                evaluated_ideas.append({
                    "idea": idea,
                    "scores": {
                        "novelty": novelty,
                        "usefulness": usefulness,
                        "coherence": coherence,
                        "total": total_score
                    }
                })
                
            # Sort by total score
            return sorted(evaluated_ideas,
                        key=lambda x: x["scores"]["total"],
                        reverse=True)
                        
        except Exception as e:
            logger.error(f"Error evaluating ideas: {e}")
            return []
            
    def _synthesize_response(self,
                           evaluated_ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize final creative response"""
        try:
            if not evaluated_ideas:
                return {
                    "status": "error",
                    "message": "No valid ideas generated"
                }
                
            # Select top ideas
            top_ideas = evaluated_ideas[:3]
            
            # Combine elements from top ideas
            synthesized = self._combine_ideas(top_ideas)
            
            return {
                "status": "success",
                "creative_response": synthesized,
                "supporting_ideas": top_ideas,
                "creativity_metrics": {
                    "novelty": float(np.mean([i["scores"]["novelty"] for i in top_ideas])) if np is not None else float(sum(i["scores"]["novelty"] for i in top_ideas)/len(top_ideas)),
                    "usefulness": float(np.mean([i["scores"]["usefulness"] for i in top_ideas])) if np is not None else float(sum(i["scores"]["usefulness"] for i in top_ideas)/len(top_ideas)),
                    "coherence": float(np.mean([i["scores"]["coherence"] for i in top_ideas])) if np is not None else float(sum(i["scores"]["coherence"] for i in top_ideas)/len(top_ideas))
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error synthesizing response: {e}")
            return {"status": "error", "message": str(e)}
            
    def _extract_concepts(self, data: Dict[str, Any]) -> List[str]:
        """Extract key concepts from input data"""
        concepts = set()
        try:
            # Extract from different data types
            if isinstance(data, dict):
                for key, value in data.items():
                    concepts.add(str(key))
                    if isinstance(value, (str, int, float)):
                        concepts.add(str(value))
                    elif isinstance(value, (list, dict)):
                        concepts.update(self._extract_concepts({"item": value}))
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, (str, int, float)):
                        concepts.add(str(item))
                    elif isinstance(item, (list, dict)):
                        concepts.update(self._extract_concepts({"item": item}))
                        
        except Exception as e:
            logger.error(f"Error extracting concepts: {e}")
            
        return list(concepts)
        
    def _analyze_patterns(self, concepts: List[str]) -> Dict[str, Any]:
        """Analyze patterns in concepts"""
        patterns = {}
        try:
            # Frequency analysis
            pattern_freq = {}
            for concept in concepts:
                for stored_pattern in self.idea_patterns:
                    if concept in stored_pattern:
                        pattern_freq[stored_pattern] = pattern_freq.get(stored_pattern, 0) + 1
                        
            # Find associations
            associations = {}
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    pair = (concept1, concept2)
                    if pair in self.idea_patterns:
                        associations[pair] = self.idea_patterns[pair]
                        
            patterns = {
                "frequencies": pattern_freq,
                "associations": associations,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing patterns: {e}")
            
        return patterns
        
    def _calculate_creative_potential(self,
                                    concepts: List[str],
                                    patterns: Dict[str, Any]) -> float:
        """Calculate creative potential of input"""
        try:
            if not concepts:
                return 0.0
                
            # Factor calculations
            novelty = len(set(concepts) - set(self.current_state["active_concepts"]))
            pattern_richness = len(patterns.get("associations", {}))
            concept_diversity = len(set(concepts))
            
            # Combine factors
            potential = (
                0.4 * (novelty / max(1, len(concepts))) +
                0.3 * (pattern_richness / max(1, len(concepts) * (len(concepts) - 1) / 2)) +
                0.3 * (concept_diversity / max(1, len(concepts)))
            )
            
            return min(1.0, max(0.0, potential))
            
        except Exception as e:
            logger.error(f"Error calculating creative potential: {e}")
            return 0.0
            
    def _generate_by_combination(self, concepts: List[str]) -> List[Dict[str, Any]]:
        """Generate ideas by combining concepts"""
        ideas = []
        try:
            # Generate random combinations
            for _ in range(min(len(concepts) * 2, 10)):
                if len(concepts) >= 2:
                    selected = random.sample(concepts, 2)
                    ideas.append({
                        "type": "combination",
                        "elements": selected,
                        "description": f"Fusion of {selected[0]} and {selected[1]}",
                        "timestamp": datetime.now().isoformat()
                    })
                    
        except Exception as e:
            logger.error(f"Error in combination generation: {e}")
            
        return ideas
        
    def _generate_by_analogy(self,
                           concepts: List[str],
                           patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate ideas through analogical thinking"""
        ideas = []
        try:
            associations = patterns.get("associations", {})
            
            for concept in concepts:
                # Find related concepts from patterns
                related = [
                    pair[1] for pair in associations.keys()
                    if pair[0] == concept
                ]
                
                if related:
                    analogy = random.choice(related)
                    ideas.append({
                        "type": "analogy",
                        "source": concept,
                        "target": analogy,
                        "description": f"Analogical mapping from {concept} to {analogy}",
                        "timestamp": datetime.now().isoformat()
                    })
                    
        except Exception as e:
            logger.error(f"Error in analogy generation: {e}")
            
        return ideas
        
    def _generate_by_mutation(self, concepts: List[str]) -> List[Dict[str, Any]]:
        """Generate ideas by mutating existing concepts"""
        ideas = []
        try:
            for concept in concepts:
                # Simple character mutation
                if len(concept) > 3:
                    mutated = list(concept)
                    pos = random.randint(0, len(mutated) - 1)
                    mutated[pos] = chr(ord(mutated[pos]) + 1)
                    ideas.append({
                        "type": "mutation",
                        "original": concept,
                        "mutated": "".join(mutated),
                        "description": f"Mutation of {concept}",
                        "timestamp": datetime.now().isoformat()
                    })
                    
        except Exception as e:
            logger.error(f"Error in mutation generation: {e}")
            
        return ideas
        
    def _generate_contextual_ideas(self,
                                 concepts: List[str],
                                 context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate ideas based on context"""
        ideas = []
        try:
            context_concepts = self._extract_concepts(context)
            
            # Find intersections between context and current concepts
            common = set(concepts) & set(context_concepts)
            
            for concept in common:
                ideas.append({
                    "type": "contextual",
                    "concept": concept,
                    "context": str(context),
                    "description": f"Contextual application of {concept}",
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"Error in contextual generation: {e}")
            
        return ideas
        
    def _calculate_novelty(self, idea: Dict[str, Any]) -> float:
        """Calculate novelty of an idea"""
        try:
            # Compare with memory
            similar_ideas = [
                mem for mem in self.creative_memory
                if self._calculate_similarity(idea, mem) > 0.8
            ]
            
            return 1.0 - (len(similar_ideas) / max(1, len(self.creative_memory)))
            
        except Exception as e:
            logger.error(f"Error calculating novelty: {e}")
            return 0.0
            
    def _calculate_usefulness(self, idea: Dict[str, Any]) -> float:
        """Calculate potential usefulness of an idea"""
        try:
            # Basic heuristics for usefulness
            type_scores = {
                "combination": 0.8,  # Combinations often useful
                "analogy": 0.7,     # Analogies can provide insights
                "mutation": 0.5,     # Mutations are less predictable
                "contextual": 0.9    # Contextual ideas highly useful
            }
            
            base_score = type_scores.get(idea.get("type", ""), 0.5)
            
            # Adjust based on description length (proxy for complexity)
            description = idea.get("description", "")
            length_factor = min(1.0, len(description) / 100)  # Normalize
            
            return (base_score + length_factor) / 2
            
        except Exception as e:
            logger.error(f"Error calculating usefulness: {e}")
            return 0.0
            
    def _calculate_coherence(self, idea: Dict[str, Any]) -> float:
        """Calculate internal coherence of an idea"""
        try:
            # Check if all required fields are present
            required_fields = ["type", "description", "timestamp"]
            completeness = sum(1 for field in required_fields if field in idea) / len(required_fields)
            
            # Check for internal consistency
            consistency = 1.0
            if idea.get("type") == "combination" and "elements" not in idea:
                consistency *= 0.5
            elif idea.get("type") == "analogy" and ("source" not in idea or "target" not in idea):
                consistency *= 0.5
            elif idea.get("type") == "mutation" and ("original" not in idea or "mutated" not in idea):
                consistency *= 0.5
                
            return (completeness + consistency) / 2
            
        except Exception as e:
            logger.error(f"Error calculating coherence: {e}")
            return 0.0
            
    def _calculate_similarity(self, idea1: Dict[str, Any], idea2: Dict[str, Any]) -> float:
        """Calculate similarity between two ideas"""
        try:
            # Compare types
            type_similarity = 1.0 if idea1.get("type") == idea2.get("type") else 0.0
            
            # Compare descriptions
            desc1 = idea1.get("description", "").lower()
            desc2 = idea2.get("description", "").lower()
            words1 = set(desc1.split())
            words2 = set(desc2.split())
            
            if not words1 or not words2:
                desc_similarity = 0.0
            else:
                common_words = words1 & words2
                desc_similarity = len(common_words) / len(words1 | words2)
                
            return (type_similarity + desc_similarity) / 2
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
            
    def _combine_ideas(self, ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine multiple ideas into a cohesive response"""
        try:
            if not ideas:
                return {}
                
            # Extract best elements
            elements = []
            descriptions = []
            for idea in ideas:
                idea_data = idea.get("idea", {})
                if "elements" in idea_data:
                    elements.extend(idea_data["elements"])
                if "description" in idea_data:
                    descriptions.append(idea_data["description"])
                    
            # Combine into new idea
            combined = {
                "type": "synthesis",
                "elements": list(set(elements)),
                "description": " | ".join(descriptions[:2]),  # Limit description length
                "component_ideas": len(ideas),
                "timestamp": datetime.now().isoformat()
            }
            
            return combined
            
        except Exception as e:
            logger.error(f"Error combining ideas: {e}")
            return {}
            
    def _update_memory(self, response: Dict[str, Any]):
        """Update creative memory and patterns"""
        try:
            # Add to memory
            self.creative_memory.append(response)
            
            # Trim memory if needed
            if len(self.creative_memory) > self.memory_depth:
                self.creative_memory = self.creative_memory[-self.memory_depth:]
                
            # Update patterns
            if "creative_response" in response:
                elements = response["creative_response"].get("elements", [])
                for i, elem1 in enumerate(elements):
                    for elem2 in elements[i+1:]:
                        self.idea_patterns[(elem1, elem2)] = datetime.now().isoformat()
                        
            # Update current state
            self.current_state["creativity_level"] = np.mean([
                response.get("creativity_metrics", {}).get("novelty", 0.5),
                response.get("creativity_metrics", {}).get("usefulness", 0.5)
            ]) if np is not None else float(sum([
                response.get("creativity_metrics", {}).get("novelty", 0.5),
                response.get("creativity_metrics", {}).get("usefulness", 0.5)
            ]) / 2)
            
            # Update active concepts
            if "creative_response" in response:
                self.current_state["active_concepts"].update(
                    response["creative_response"].get("elements", [])
                )
                
        except Exception as e:
            logger.error(f"Error updating memory: {e}")
            
    def get_state(self) -> Dict[str, Any]:
        """Get current state of the creativity engine"""
        return self.current_state.copy()
        
    def get_memory(self) -> List[Dict[str, Any]]:
        """Get creative memory"""
        return self.creative_memory.copy()
        
    def get_patterns(self) -> Dict[str, Any]:
        """Get identified idea patterns"""
        return self.idea_patterns.copy()