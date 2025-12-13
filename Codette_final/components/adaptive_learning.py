from typing import Dict, Any, List  
from collections import defaultdict  
import json  # For optional persistence  
  
class AdaptiveLearningEnvironment:  
    """Creates environments for real-time learning and adaptation"""  
  
    def __init__(self):  
        # Use defaultdict for simpler logic  
        self.environment_state = defaultdict(list)  
  
    def update_environment(self, user_id: int, interaction: Dict[str, Any]) -> None:  
        """  
        Update the environment based on user interactions.  
          
        Args:  
            user_id (int): The ID of the user.  
            interaction (Dict[str, Any]): Details of the user interaction.  
        """  
        if not isinstance(interaction, dict):  
            raise ValueError("Interaction must be a dictionary.")  
          
        # Append interaction to the user's state  
        self.environment_state[user_id].append(interaction)  
  
    def adapt_to_user(self, user_id: int) -> List[Dict[str, Any]]:  
        """  
        Adapt the environment to the user's preferences and interactions.  
          
        Args:  
            user_id (int): The ID of the user.  
          
        Returns:  
            List[Dict[str, Any]]: The user's interaction history.  
        """  
        return self.environment_state.get(user_id, [])  
  
    def save_state(self, file_path: str) -> None:  
        """  
        Save the environment state to a file (optional persistence).  
          
        Args:  
            file_path (str): The file path to save the state.  
        """  
        with open(file_path, 'w') as file:  
            json.dump(self.environment_state, file)  
  
    def load_state(self, file_path: str) -> None:  
        """  
        Load the environment state from a file.  
          
        Args:  
            file_path (str): The file path to load the state from.  
        """  
        try:  
            with open(file_path, 'r') as file:  
                data = json.load(file)  
                self.environment_state = defaultdict(list, data)  
        except FileNotFoundError:  
            print(f"File '{file_path}' not found. Starting with an empty state.")  
  
# Example usage  
if __name__ == "__main__":  
    ale = AdaptiveLearningEnvironment()  
  
    # Update environment with user interactions  
    ale.update_environment(1, {"action": "click", "page": "homepage"})  