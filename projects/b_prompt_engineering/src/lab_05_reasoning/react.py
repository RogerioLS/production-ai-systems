"""ReAct (Reasoning + Acting) autonomous agent execution engine."""

import json
import re
import time
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from projects.b_prompt_engineering.src.lab_05_reasoning.exceptions import (
    ReActExecutionError,
    ToolNotFoundError,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.types import (
    ReActResult,
    ReActStep,
    ToolDefinition,
)


class ReActEngine:
    """Production ReAct loop implementation (Yao et al., 2022).

    Orchestrates the interleaved cognitive loop:
        Thought: <internal reasoning on what to do next>
        Action: <tool_name>
        Action Input: <json/dict parameters>
        Observation: <result returned by executing tool>
        ...
        Thought: <concluding deduction>
        Final Answer: <solution to task>
    """

    def __init__(self, max_iterations: int = 6) -> None:
        self.max_iterations: int = max_iterations
        self.tools: Dict[str, ToolDefinition] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        handler: Callable[..., Any],
        parameters_schema: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Registers an executable tool into the ReAct agent's environment."""
        tool = ToolDefinition(
            name=name,
            description=description,
            handler=handler,
            parameters_schema=parameters_schema or {},
        )
        self.tools[name] = tool
        logger.debug(f"Registered tool: '{name}' ({description})")

    def build_system_prompt(self) -> str:
        """Generates instruction prompt describing available tools and ReAct syntax."""
        tools_docs = []
        for tool in self.tools.values():
            tools_docs.append(f"- {tool.name}: {tool.description}")

        tools_str = "\n".join(tools_docs)
        prompt = (
            "You are a helpful assistant equipped with the following tools:\n"
            f"{tools_str}\n\n"
            "To solve the user's task, use the following strict format:\n\n"
            "Thought: <your reasoning about what step to take next>\n"
            "Action: <the tool name, one of the registered tools above>\n"
            "Action Input: <valid JSON string containing tool arguments>\n"
            "Observation: <the result returned by the environment>\n\n"
            "... (repeat Thought/Action/Action Input/Observation N times as necessary)\n\n"
            "Thought: I know the final answer\n"
            "Final Answer: <the ultimate response to the original task>\n"
        )
        return prompt

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Executes registered tool and returns stringified observation."""
        if tool_name not in self.tools:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
            )

        tool = self.tools[tool_name]
        if not tool.handler:
            return f"Error: Tool '{tool_name}' has no registered handler."

        try:
            logger.info(f"ReAct invoking tool '{tool_name}' with args: {arguments}")
            res = tool.handler(**arguments)
            return str(res)
        except Exception as err:
            logger.warning(f"Tool '{tool_name}' raised an error: {err}")
            return f"Error executing tool '{tool_name}': {err}"

    @staticmethod
    def parse_llm_turn(text: str) -> Dict[str, Any]:
        """Parses LLM generation into Thought, Action, Action Input, or Final Answer."""
        thought_match = re.search(
            r"Thought:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)", text, re.DOTALL
        )
        action_match = re.search(r"Action:\s*([a-zA-Z0-9_-]+)", text)
        input_match = re.search(r"Action Input:\s*(.*?)(?=\nObservation:|$)", text, re.DOTALL)
        final_answer_match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL)

        thought = thought_match.group(1).strip() if thought_match else ""
        action = action_match.group(1).strip() if action_match else None
        final_answer = final_answer_match.group(1).strip() if final_answer_match else None

        action_input = {}
        if input_match:
            raw_input = input_match.group(1).strip()
            # Clean possible markdown block wraps
            raw_input = re.sub(r"^```json\s*", "", raw_input)
            raw_input = re.sub(r"\s*```$", "", raw_input)
            try:
                action_input = json.loads(raw_input)
            except Exception:
                # If not valid JSON, treat as a single query/input argument
                action_input = {"query": raw_input}

        return {
            "thought": thought,
            "action": action,
            "action_input": action_input,
            "final_answer": final_answer,
        }

    def run(
        self,
        task: str,
        llm_responder: Callable[[str], str],
    ) -> ReActResult:
        """Executes the full ReAct cognitive loop with trajectory tracking."""
        start_time = time.time()
        system_prompt = self.build_system_prompt()
        trajectory: str = f"{system_prompt}\n\nTask: {task}\n"

        steps: List[ReActStep] = []

        for step_idx in range(1, self.max_iterations + 1):
            logger.debug(f"ReAct Step {step_idx}/{self.max_iterations}")
            llm_output = llm_responder(trajectory)
            parsed = self.parse_llm_turn(llm_output)

            # Check if Final Answer reached
            if parsed["final_answer"]:
                final_thought = parsed["thought"] or "Task successfully completed."
                steps.append(
                    ReActStep(
                        step_number=step_idx,
                        thought=final_thought,
                        action_tool=None,
                        action_input=None,
                        observation=None,
                    )
                )
                duration = time.time() - start_time
                return ReActResult(
                    task=task,
                    final_answer=parsed["final_answer"],
                    steps=steps,
                    total_steps=step_idx,
                    success=True,
                    execution_time_seconds=round(duration, 3),
                )

            # Action required
            if parsed["action"]:
                tool_name = parsed["action"]
                tool_args = parsed["action_input"]

                try:
                    observation = self.execute_tool(tool_name, tool_args)
                except ToolNotFoundError as err:
                    observation = str(err)

                steps.append(
                    ReActStep(
                        step_number=step_idx,
                        thought=parsed["thought"],
                        action_tool=tool_name,
                        action_input=tool_args,
                        observation=observation,
                    )
                )

                # Update trajectory with history
                trajectory += (
                    f"Thought: {parsed['thought']}\n"
                    f"Action: {tool_name}\n"
                    f"Action Input: {json.dumps(tool_args)}\n"
                    f"Observation: {observation}\n"
                )
            else:
                # If neither action nor final answer found, break gracefully
                duration = time.time() - start_time
                return ReActResult(
                    task=task,
                    final_answer=llm_output.strip(),
                    steps=steps,
                    total_steps=step_idx,
                    success=False,
                    execution_time_seconds=round(duration, 3),
                )

        duration = time.time() - start_time
        raise ReActExecutionError(
            f"ReAct loop exceeded maximum allowable iterations ({self.max_iterations}) "
            "without terminating."
        )
