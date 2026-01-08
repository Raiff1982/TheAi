"""
Tool Registry and Schema Definition
Defines all available tools for Codette multimodal execution with OpenAI-style tool_use format
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Callable, Optional
from enum import Enum
import json


class ToolType(Enum):
    """Categories of available tools."""
    FILE_SYSTEM = "file_system"
    WEB_SEARCH = "web_search"
    CODE_EXECUTION = "code_execution"
    DATA_ANALYSIS = "data_analysis"
    API_CALL = "api_call"
    KNOWLEDGE_BASE = "knowledge_base"


@dataclass
class ToolParameter:
    """Defines a single parameter for a tool."""
    name: str
    type: str  # "string", "number", "integer", "boolean", "array", "object"
    description: str
    required: bool = True
    enum_values: Optional[List[str]] = None
    default: Optional[Any] = None

    def to_schema(self) -> Dict[str, Any]:
        """Convert to JSON schema format."""
        schema = {
            "type": self.type,
            "description": self.description
        }
        if self.enum_values:
            schema["enum"] = self.enum_values
        if self.default is not None:
            schema["default"] = self.default
        return schema


@dataclass
class Tool:
    """Represents a callable tool with OpenAI-style schema."""
    name: str
    description: str
    category: ToolType
    parameters: List[ToolParameter]
    handler: Optional[Callable] = None  # Runtime binding
    max_tokens: int = 4096  # Max tokens in tool response

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function schema format."""
        required_params = [p.name for p in self.parameters if p.required]
        properties = {p.name: p.to_schema() for p in self.parameters}

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params
                }
            }
        }

    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate parameters against schema.
        
        Returns:
            (is_valid, error_message)
        """
        required_names = {p.name for p in self.parameters if p.required}
        provided_names = set(params.keys())

        # Check required params
        missing = required_names - provided_names
        if missing:
            return False, f"Missing required parameters: {', '.join(missing)}"

        # Validate types (basic)
        for param in self.parameters:
            if param.name in params:
                value = params[param.name]
                expected_type = param.type

                if expected_type == "string" and not isinstance(value, str):
                    return False, f"Parameter '{param.name}' must be string, got {type(value).__name__}"
                elif expected_type == "number" and not isinstance(value, (int, float)):
                    return False, f"Parameter '{param.name}' must be number, got {type(value).__name__}"
                elif expected_type == "integer" and not isinstance(value, int):
                    return False, f"Parameter '{param.name}' must be integer, got {type(value).__name__}"
                elif expected_type == "boolean" and not isinstance(value, bool):
                    return False, f"Parameter '{param.name}' must be boolean, got {type(value).__name__}"

        return True, ""


class ToolRegistry:
    """Central registry of all available tools."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register built-in tools."""
        
        # File system tools
        self.register_tool(Tool(
            name="read_file",
            description="Read contents of a file from the filesystem",
            category=ToolType.FILE_SYSTEM,
            parameters=[
                ToolParameter("path", "string", "Absolute path to file", required=True),
                ToolParameter("start_line", "integer", "Start line (1-indexed)", required=False, default=1),
                ToolParameter("end_line", "integer", "End line (1-indexed)", required=False, default=None)
            ]
        ))

        self.register_tool(Tool(
            name="write_file",
            description="Write content to a file",
            category=ToolType.FILE_SYSTEM,
            parameters=[
                ToolParameter("path", "string", "Absolute path to file", required=True),
                ToolParameter("content", "string", "File content to write", required=True),
                ToolParameter("append", "boolean", "Append to file instead of overwrite", required=False, default=False)
            ]
        ))

        self.register_tool(Tool(
            name="list_directory",
            description="List files and directories in a path",
            category=ToolType.FILE_SYSTEM,
            parameters=[
                ToolParameter("path", "string", "Directory path", required=True),
                ToolParameter("recursive", "boolean", "List recursively", required=False, default=False)
            ]
        ))

        self.register_tool(Tool(
            name="search_files",
            description="Search for files matching a pattern",
            category=ToolType.FILE_SYSTEM,
            parameters=[
                ToolParameter("pattern", "string", "File name pattern (glob)", required=True),
                ToolParameter("directory", "string", "Search directory", required=False, default=".")
            ]
        ))

        # Code execution tools
        self.register_tool(Tool(
            name="execute_python",
            description="Execute Python code snippet safely",
            category=ToolType.CODE_EXECUTION,
            parameters=[
                ToolParameter("code", "string", "Python code to execute", required=True),
                ToolParameter("timeout", "integer", "Execution timeout in seconds", required=False, default=30)
            ],
            max_tokens=8192
        ))

        # Web search
        self.register_tool(Tool(
            name="web_search",
            description="Search the web for information",
            category=ToolType.WEB_SEARCH,
            parameters=[
                ToolParameter("query", "string", "Search query", required=True),
                ToolParameter("max_results", "integer", "Maximum results to return", required=False, default=5)
            ],
            max_tokens=4096
        ))

        # Data analysis
        self.register_tool(Tool(
            name="analyze_data",
            description="Perform statistical analysis on data",
            category=ToolType.DATA_ANALYSIS,
            parameters=[
                ToolParameter("data", "array", "Numerical data to analyze", required=True),
                ToolParameter("analysis_type", "string", 
                            "Type of analysis (summary, correlation, distribution, trend)",
                            required=True,
                            enum_values=["summary", "correlation", "distribution", "trend"])
            ],
            max_tokens=2048
        ))

        # Knowledge base query
        self.register_tool(Tool(
            name="query_knowledge_base",
            description="Query the internal knowledge base for facts and reasoning",
            category=ToolType.KNOWLEDGE_BASE,
            parameters=[
                ToolParameter("query", "string", "Knowledge query", required=True),
                ToolParameter("context", "string", "Optional context for the query", required=False)
            ],
            max_tokens=4096
        ))

        # API calls
        self.register_tool(Tool(
            name="api_call",
            description="Make HTTP API calls to external services",
            category=ToolType.API_CALL,
            parameters=[
                ToolParameter("url", "string", "API endpoint URL", required=True),
                ToolParameter("method", "string", "HTTP method (GET, POST, PUT, DELETE)",
                            required=True,
                            enum_values=["GET", "POST", "PUT", "DELETE"]),
                ToolParameter("headers", "object", "HTTP headers", required=False),
                ToolParameter("body", "string", "Request body (JSON)", required=False)
            ],
            max_tokens=4096
        ))

    def register_tool(self, tool: Tool):
        """Register a new tool."""
        if tool.name in self.tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name."""
        return self.tools.get(name)

    def get_tools_by_category(self, category: ToolType) -> List[Tool]:
        """Get all tools in a category."""
        return [t for t in self.tools.values() if t.category == category]

    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools."""
        return list(self.tools.values())

    def get_openai_schema(self) -> List[Dict[str, Any]]:
        """Get OpenAI function schema for all tools."""
        return [tool.to_openai_schema() for tool in self.get_all_tools()]

    def to_json(self) -> str:
        """Serialize all tool schemas to JSON."""
        return json.dumps(self.get_openai_schema(), indent=2)
