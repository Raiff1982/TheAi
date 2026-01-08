"""
Tool Executor - Safely executes tool calls with sandboxing and resource limits
"""

import json
import subprocess
import logging
import asyncio
import re
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from tool_registry import Tool, ToolRegistry, ToolType

logger = logging.getLogger(__name__)


@dataclass
class ToolCallResult:
    """Result of a tool execution."""
    tool_name: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    tokens_used: int = 0


class ToolExecutor:
    """
    Safely executes tool calls with sandboxing, resource limits, and logging.
    """

    def __init__(self, registry: ToolRegistry, sandbox_dir: str = "tool_sandbox"):
        self.registry = registry
        self.sandbox_dir = Path(sandbox_dir)
        self.sandbox_dir.mkdir(exist_ok=True)
        self.execution_log = []
        self.max_execution_time = 30  # seconds
        self.max_output_chars = 50000

    async def execute(self, tool_name: str, params: Dict[str, Any]) -> ToolCallResult:
        """
        Execute a tool call asynchronously.
        
        Args:
            tool_name: Name of tool to execute
            params: Parameters for the tool
            
        Returns:
            ToolCallResult with output or error
        """
        start_time = datetime.utcnow()

        try:
            tool = self.registry.get_tool(tool_name)
            if not tool:
                return ToolCallResult(
                    tool_name=tool_name,
                    success=False,
                    output="",
                    error=f"Tool '{tool_name}' not found in registry"
                )

            # Validate parameters
            is_valid, error_msg = tool.validate_params(params)
            if not is_valid:
                return ToolCallResult(
                    tool_name=tool_name,
                    success=False,
                    output="",
                    error=f"Invalid parameters: {error_msg}"
                )

            # Route to handler based on tool type
            if tool.category == ToolType.FILE_SYSTEM:
                result = await self._execute_file_operation(tool, params)
            elif tool.category == ToolType.CODE_EXECUTION:
                result = await self._execute_code(tool, params)
            elif tool.category == ToolType.WEB_SEARCH:
                result = await self._execute_web_search(tool, params)
            elif tool.category == ToolType.DATA_ANALYSIS:
                result = await self._execute_data_analysis(tool, params)
            elif tool.category == ToolType.KNOWLEDGE_BASE:
                result = await self._execute_knowledge_query(tool, params)
            elif tool.category == ToolType.API_CALL:
                result = await self._execute_api_call(tool, params)
            else:
                result = ToolCallResult(
                    tool_name=tool_name,
                    success=False,
                    output="",
                    error=f"Unknown tool category: {tool.category}"
                )

            # Calculate execution time
            end_time = datetime.utcnow()
            result.execution_time_ms = (end_time - start_time).total_seconds() * 1000

            # Truncate output if needed
            if len(result.output) > self.max_output_chars:
                result.output = result.output[:self.max_output_chars] + "\n[... output truncated ...]"

            # Log execution
            self.execution_log.append({
                "timestamp": start_time.isoformat(),
                "tool_name": tool_name,
                "success": result.success,
                "execution_time_ms": result.execution_time_ms
            })

            logger.info(f"Tool '{tool_name}' executed: success={result.success}, time={result.execution_time_ms:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"Unexpected error executing tool '{tool_name}': {e}", exc_info=True)
            return ToolCallResult(
                tool_name=tool_name,
                success=False,
                output="",
                error=str(e)
            )

    async def _execute_file_operation(self, tool: Tool, params: Dict[str, Any]) -> ToolCallResult:
        """Execute file system operations safely."""
        try:
            operation = tool.name

            if operation == "read_file":
                path = Path(params["path"])
                if not self._safe_path(path):
                    return ToolCallResult(
                        tool_name=tool.name,
                        success=False,
                        output="",
                        error="Access denied: path outside workspace"
                    )

                if not path.exists():
                    return ToolCallResult(
                        tool_name=tool.name,
                        success=False,
                        output="",
                        error=f"File not found: {path}"
                    )

                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                return ToolCallResult(
                    tool_name=tool.name,
                    success=True,
                    output=content
                )

            elif operation == "write_file":
                path = Path(params["path"])
                if not self._safe_path(path):
                    return ToolCallResult(
                        tool_name=tool.name,
                        success=False,
                        output="",
                        error="Access denied: path outside workspace"
                    )

                path.parent.mkdir(parents=True, exist_ok=True)
                mode = 'a' if params.get("append", False) else 'w'

                with open(path, mode, encoding='utf-8') as f:
                    f.write(params["content"])

                return ToolCallResult(
                    tool_name=tool.name,
                    success=True,
                    output=f"File written successfully: {path}"
                )

            elif operation == "list_directory":
                path = Path(params["path"])
                if not self._safe_path(path):
                    return ToolCallResult(
                        tool_name=tool.name,
                        success=False,
                        output="",
                        error="Access denied: path outside workspace"
                    )

                if not path.is_dir():
                    return ToolCallResult(
                        tool_name=tool.name,
                        success=False,
                        output="",
                        error=f"Not a directory: {path}"
                    )

                if params.get("recursive", False):
                    items = [str(p.relative_to(path)) for p in path.rglob("*")]
                else:
                    items = [str(p.relative_to(path)) for p in path.iterdir()]

                return ToolCallResult(
                    tool_name=tool.name,
                    success=True,
                    output="\n".join(sorted(items))
                )

            else:
                return ToolCallResult(
                    tool_name=tool.name,
                    success=False,
                    output="",
                    error=f"Unknown file operation: {operation}"
                )

        except Exception as e:
            return ToolCallResult(
                tool_name=tool.name,
                success=False,
                output="",
                error=str(e)
            )

    async def _execute_code(self, tool: Tool, params: Dict[str, Any]) -> ToolCallResult:
        """
        Execute Python code in restricted sandbox.
        """
        try:
            code = params["code"]
            timeout = params.get("timeout", 30)

            # Create restricted globals with safe builtins
            safe_builtins = {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
            }

            restricted_globals = {
                '__builtins__': safe_builtins,
                '__name__': '__codette_sandbox__'
            }

            # Capture output
            import io
            import sys

            captured_output = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured_output

            try:
                exec(code, restricted_globals, restricted_globals)
                output = captured_output.getvalue()

                return ToolCallResult(
                    tool_name=tool.name,
                    success=True,
                    output=output if output else "(code executed, no output)"
                )

            finally:
                sys.stdout = old_stdout

        except Exception as e:
            return ToolCallResult(
                tool_name=tool.name,
                success=False,
                output="",
                error=f"Code execution error: {str(e)}"
            )

    async def _execute_web_search(self, tool: Tool, params: Dict[str, Any]) -> ToolCallResult:
        """Placeholder for web search integration."""
        # This would integrate with actual search API (Bing, Google, etc.)
        query = params["query"]
        return ToolCallResult(
            tool_name=tool.name,
            success=False,
            output="",
            error="Web search not yet integrated - requires API key"
        )

    async def _execute_data_analysis(self, tool: Tool, params: Dict[str, Any]) -> ToolCallResult:
        """Perform basic data analysis."""
        try:
            data = params["data"]
            analysis_type = params["analysis_type"]

            if not isinstance(data, list):
                return ToolCallResult(
                    tool_name=tool.name,
                    success=False,
                    output="",
                    error="Data must be an array of numbers"
                )

            # Basic statistics
            if analysis_type == "summary":
                output = f"""
Data Summary:
- Count: {len(data)}
- Min: {min(data) if data else 'N/A'}
- Max: {max(data) if data else 'N/A'}
- Mean: {sum(data) / len(data) if data else 'N/A'}
- Sum: {sum(data)}
""".strip()

                return ToolCallResult(
                    tool_name=tool.name,
                    success=True,
                    output=output
                )

            else:
                return ToolCallResult(
                    tool_name=tool.name,
                    success=False,
                    output="",
                    error=f"Analysis type '{analysis_type}' not yet implemented"
                )

        except Exception as e:
            return ToolCallResult(
                tool_name=tool.name,
                success=False,
                output="",
                error=str(e)
            )

    async def _execute_knowledge_query(self, tool: Tool, params: Dict[str, Any]) -> ToolCallResult:
        """Query knowledge base."""
        # Placeholder for knowledge base integration
        query = params["query"]
        return ToolCallResult(
            tool_name=tool.name,
            success=False,
            output="",
            error="Knowledge base query not yet implemented"
        )

    async def _execute_api_call(self, tool: Tool, params: Dict[str, Any]) -> ToolCallResult:
        """Make HTTP API calls."""
        # Placeholder - would require aiohttp
        return ToolCallResult(
            tool_name=tool.name,
            success=False,
            output="",
            error="API calls not yet integrated"
        )

    def _safe_path(self, path: Path) -> bool:
        """Check if path is within allowed workspace."""
        try:
            workspace_root = Path("j:\\TheAI").resolve()
            path_resolved = path.resolve()
            # Must be within workspace
            return str(path_resolved).startswith(str(workspace_root))
        except:
            return False

    def get_execution_log(self) -> list:
        """Get execution history."""
        return self.execution_log
