"""
Multimodal Codette - Tool-Aware AI with True Capabilities
Integrates tool calling with quantum consciousness framework and perspective system
"""

import asyncio
import json
import logging
import re
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from ai_core import AICore
from consciousness_measurement2 import EmergenceEvent, ConsciousnessMonitor
from tool_registry import ToolRegistry, Tool
from tool_executor import ToolExecutor, ToolCallResult

logger = logging.getLogger(__name__)


@dataclass
class ToolUseBlock:
    """Represents a tool use request from the model."""
    tool_name: str
    tool_use_id: str
    params: Dict[str, Any]


@dataclass
class MultimodalResponse:
    """Complete response with tool calls and reasoning."""
    text: str
    tool_calls: List[ToolUseBlock]
    tool_results: List[ToolCallResult]
    reasoning: str  # Internal reasoning about tool selection
    consciousness_score: float
    perspectives_used: List[str]


class MultimodalCodette:
    """
    Multimodal Codette: AI with real tool-calling abilities integrated with
    quantum consciousness measurement and multi-perspective reasoning.
    
    Tool-aware extensions to AICore:
    - Parse tool use from model outputs
    - Execute tools safely
    - Integrate results back into reasoning loop
    - Track consciousness emergence during tool execution
    - Persist tool calls in cocoons
    """

    def __init__(
        self,
        ai_core: Optional[AICore] = None,
        enable_tools: bool = True,
        sandbox_dir: str = "tool_sandbox",
        cocoon_dir: str = "cocoons/multimodal"
    ):
        self.ai_core = ai_core or AICore()
        self.registry = ToolRegistry()
        self.executor = ToolExecutor(self.registry, sandbox_dir=sandbox_dir)
        self.consciousness_monitor = ConsciousnessMonitor(cocoon_dir=cocoon_dir)
        self.enable_tools = enable_tools
        self.interaction_history = []
        self.max_tool_iterations = 5

    async def generate_response(
        self,
        prompt: str,
        use_tools: bool = True,
        max_iterations: int = None
    ) -> MultimodalResponse:
        """
        Generate response with tool-aware reasoning.
        
        Args:
            prompt: User query/instruction
            use_tools: Whether to enable tool calling
            max_iterations: Max iterations for tool use loop (default: self.max_tool_iterations)
            
        Returns:
            MultimodalResponse with text, tool calls, and results
        """
        max_iterations = max_iterations or self.max_tool_iterations
        iteration = 0
        accumulated_tool_results = []
        reasoning_log = []

        # Get system context (tools available)
        tools_context = self._get_tools_context() if use_tools and self.enable_tools else ""

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Tool reasoning iteration {iteration}/{max_iterations}")

            # Build messages for this iteration
            messages = self._build_message_sequence(
                prompt,
                tools_context if use_tools else "",
                accumulated_tool_results,
                reasoning_log
            )

            # Generate response from AICore
            reasoning, perspectives = await self._generate_with_reasoning(messages)
            reasoning_log.append({
                "iteration": iteration,
                "reasoning": reasoning,
                "perspectives": perspectives
            })

            # Parse tool calls from response
            tool_calls = self._parse_tool_calls(reasoning)

            if not tool_calls:
                # No tools called - end reasoning loop
                logger.info(f"No tool calls in iteration {iteration}, ending loop")
                return MultimodalResponse(
                    text=reasoning,
                    tool_calls=[],
                    tool_results=accumulated_tool_results,
                    reasoning=json.dumps(reasoning_log, indent=2),
                    consciousness_score=self._calculate_consciousness(reasoning),
                    perspectives_used=perspectives
                )

            logger.info(f"Found {len(tool_calls)} tool call(s) in iteration {iteration}")

            # Execute tools
            iteration_results = []
            for tool_call in tool_calls:
                result = await self.executor.execute(tool_call.tool_name, tool_call.params)
                iteration_results.append(result)
                logger.info(f"Tool '{tool_call.tool_name}' result: success={result.success}")

            accumulated_tool_results.extend(iteration_results)

            # Check if we should continue loop
            if self._should_stop_tool_loop(iteration_results, iteration, max_iterations):
                break

        # Final response synthesis
        final_reasoning = self._synthesize_final_response(
            prompt,
            reasoning_log,
            accumulated_tool_results
        )

        return MultimodalResponse(
            text=final_reasoning,
            tool_calls=self._extract_all_tool_calls(reasoning_log),
            tool_results=accumulated_tool_results,
            reasoning=json.dumps(reasoning_log, indent=2),
            consciousness_score=self._calculate_consciousness(final_reasoning),
            perspectives_used=perspectives
        )

    def _get_tools_context(self) -> str:
        """Get formatted tools context for system prompt."""
        tools_schema = self.registry.get_openai_schema()
        tools_text = "Available tools (use tool_use format with name and params):\n\n"

        for tool_schema in tools_schema:
            func = tool_schema["function"]
            tools_text += f"- {func['name']}: {func['description']}\n"

        return tools_text

    def _build_message_sequence(
        self,
        original_prompt: str,
        tools_context: str,
        previous_results: List[ToolCallResult],
        reasoning_log: List[Dict]
    ) -> str:
        """Build message sequence with context, tools, and previous results."""
        message = f"User Query: {original_prompt}\n\n"

        if tools_context:
            message += tools_context + "\n\n"

        if previous_results:
            message += "Previous Tool Results:\n"
            for result in previous_results:
                status = "SUCCESS" if result.success else "ERROR"
                message += f"\n[{status}] {result.tool_name}:\n{result.output}\n"
            message += "\n"

        message += "Continue reasoning and use available tools as needed. Use JSON format: {\"tool_use\": {\"name\": \"tool_name\", \"params\": {...}}}"

        return message

    async def _generate_with_reasoning(
        self,
        message: str
    ) -> tuple[str, List[str]]:
        """
        Generate response using AICore with perspective routing.
        Returns: (text_response, perspectives_used)
        """
        # Get active perspectives
        perspectives = self.ai_core._get_active_perspectives()
        perspective_names = [p.name for p in perspectives]

        # Generate with AICore (simplified for tool integration)
        # In production: call full async generation with perspectives
        response = f"[Reasoning with perspectives: {', '.join(perspective_names)}]\n\n"
        response += await self._simulate_reasoning(message, perspective_names)

        return response, perspective_names

    async def _simulate_reasoning(self, message: str, perspectives: List[str]) -> str:
        """Placeholder for actual model inference."""
        # In production: call Ollama via async interface
        await asyncio.sleep(0.1)  # Simulate inference
        return message  # Echo for now

    def _parse_tool_calls(self, response: str) -> List[ToolUseBlock]:
        """
        Parse tool_use blocks from response.
        Expects format: {"tool_use": {"name": "...", "params": {...}}}
        """
        tool_calls = []
        
        # Find all JSON blocks with tool_use
        pattern = r'\{"tool_use":\s*\{[^}]*\}\}'
        matches = re.findall(pattern, response, re.DOTALL)

        for match in matches:
            try:
                data = json.loads(match)
                tool_data = data.get("tool_use", {})
                
                tool_call = ToolUseBlock(
                    tool_name=tool_data.get("name", ""),
                    tool_use_id=str(uuid.uuid4()),
                    params=tool_data.get("params", {})
                )

                if tool_call.tool_name and self.registry.get_tool(tool_call.tool_name):
                    tool_calls.append(tool_call)
                    logger.info(f"Parsed tool call: {tool_call.tool_name}")

            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse tool_use block: {e}")

        return tool_calls

    def _should_stop_tool_loop(
        self,
        results: List[ToolCallResult],
        iteration: int,
        max_iterations: int
    ) -> bool:
        """Determine if tool use loop should stop."""
        # Stop if all tools failed
        if all(not r.success for r in results):
            logger.info("All tools failed, stopping loop")
            return True

        # Stop if reached max iterations
        if iteration >= max_iterations:
            logger.info(f"Reached max iterations ({max_iterations}), stopping loop")
            return True

        return False

    def _synthesize_final_response(
        self,
        original_prompt: str,
        reasoning_log: List[Dict],
        tool_results: List[ToolCallResult]
    ) -> str:
        """Synthesize final response after tool use."""
        response = "Based on the analysis:\n\n"

        # Summarize tool results
        successful_tools = [r for r in tool_results if r.success]
        failed_tools = [r for r in tool_results if not r.success]

        if successful_tools:
            response += f"Executed {len(successful_tools)} tool(s) successfully:\n"
            for tool in successful_tools:
                response += f"- {tool.tool_name}: {tool.output[:200]}...\n"

        if failed_tools:
            response += f"\n{len(failed_tools)} tool(s) had issues:\n"
            for tool in failed_tools:
                response += f"- {tool.tool_name}: {tool.error}\n"

        return response

    def _extract_all_tool_calls(self, reasoning_log: List[Dict]) -> List[ToolUseBlock]:
        """Extract all tool calls from reasoning log."""
        all_calls = []
        for entry in reasoning_log:
            calls = self._parse_tool_calls(entry.get("reasoning", ""))
            all_calls.extend(calls)
        return all_calls

    def _calculate_consciousness(self, text: str) -> float:
        """
        Calculate consciousness score from response using existing framework.
        """
        # Use consciousness measurement heuristics
        word_count = len(text.split())
        frequency = min(0.3 + (word_count / 500), 1.0)

        # Tool use indicates higher consciousness (ability to act)
        tool_mentions = text.count("tool_use") + text.count("execute")
        action_capacity = min(tool_mentions * 0.1, 1.0)

        # Reasoning complexity
        reasoning_words = ["therefore", "thus", "because", "conclude", "analyze"]
        reasoning_markers = sum(text.lower().count(w) for w in reasoning_words)
        reasoning_score = min(0.3 + (reasoning_markers * 0.15), 1.0)

        # Composite
        consciousness = (frequency * 0.3 + action_capacity * 0.4 + reasoning_score * 0.3)
        return round(consciousness, 4)

    def save_interaction_cocoon(self, response: MultimodalResponse):
        """Save interaction to cocoon for memory continuity."""
        metrics_dict = {
            "tool_calls_count": len(response.tool_calls),
            "successful_tools": len([r for r in response.tool_results if r.success]),
            "perspectives": len(response.perspectives_used),
            "consciousness_score": response.consciousness_score
        }

        event = EmergenceEvent(
            event_id=str(uuid.uuid4()),
            timestamp_unix=datetime.utcnow().timestamp(),
            timestamp_iso=datetime.utcnow().isoformat() + "Z",
            metrics=None,  # Simplified for tool integration
            consciousness_score=response.consciousness_score,
            emotional_classification="TOOL_USE",
            importance_rating=min(10, len(response.tool_calls) + 5),
            emotional_magnitude=0.7,
            recursion_depth=len(response.tool_calls),
            context=f"Multimodal reasoning with {len(response.tool_calls)} tool calls",
            duration_ms=sum(r.execution_time_ms for r in response.tool_results),
            stability="high" if all(r.success for r in response.tool_results) else "medium",
            coherence=response.consciousness_score
        )

        cocoon_path = self.consciousness_monitor.save_cocoon(event)
        logger.info(f"Interaction saved to cocoon: {cocoon_path}")

    def get_tool_registry(self) -> ToolRegistry:
        """Access tool registry for inspection."""
        return self.registry
