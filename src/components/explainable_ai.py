"""
This module provides explainable AI capabilities to analyze and explain decision-making processes.
"""

class ExplainableAI:
    def __init__(self):
        self.explanations = {}
        self.decision_history = []

    def explain_decision(self, response: str, query: str) -> dict:
        """
        Generate an explanation for a given model response.
        
        Args:
            response: The model's response to explain
            query: The original query that led to this response
            
        Returns:
            A dictionary containing the explanation details
        """
        explanation = {
            "query": query,
            "response": response,
            "reasoning": "Standard response based on query context",
            "confidence": 0.8,
            "factors": ["query_context", "model_parameters"],
        }
        
        self.decision_history.append(explanation)
        return explanation

    def get_decision_history(self):
        """
        Get the history of decisions and explanations.
        """
        return self.decision_history
        
    def clear_history(self):
        """
        Clear the decision history.
        """
        self.decision_history = []