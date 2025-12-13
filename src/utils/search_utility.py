from typing import List, Dict, Any
import json
import os
from components.search_engine import SearchEngine

class SearchUtility:
    """Utility class for performing web searches"""
    
    def __init__(self, config_path: str = "config/google_config.json"):
        self.search_engine = None
        self._initialize_search_engine(config_path)
        
    def _initialize_search_engine(self, config_path: str):
        """Initialize the search engine with configuration"""
        try:
            # Load config if exists
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                # Set environment variables
                os.environ['GOOGLE_API_KEY'] = config['google_search']['api_key']
                os.environ['GOOGLE_CUSTOM_SEARCH_ID'] = config['google_search']['custom_search_id']
            
            self.search_engine = SearchEngine()
            
        except Exception as e:
            print(f"Failed to initialize search engine: {str(e)}")
            self.search_engine = None
            
    async def search(self, query: str, max_results: int = 3) -> str:
        """
        Perform a web search and return formatted results
        
        Args:
            query (str): The search query
            max_results (int): Maximum number of results to return
            
        Returns:
            str: Formatted search results with sources
        """
        if not self.search_engine:
            return "Search functionality is not available. Please check configuration."
            
        try:
            return await self.search_engine.get_knowledge(query, max_results)
        except Exception as e:
            return f"Search failed: {str(e)}"
            
    async def get_raw_results(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Get raw search results for further processing
        
        Args:
            query (str): The search query
            num_results (int): Number of results to return
            
        Returns:
            List[Dict]: List of search results with title, link, and snippet
        """
        if not self.search_engine:
            return []
            
        try:
            return await self.search_engine.search(query, num_results)
        except Exception:
            return []