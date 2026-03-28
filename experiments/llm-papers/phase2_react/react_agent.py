"""ReAct Agent — Reasoning + Acting loop.

Paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
       (Yao et al., 2022 / ICLR 2023)

The ReAct pattern interleaves:
- Thought: LLM reasons about the current state and what to do next
- Action: LLM calls a tool to get new information
- Observation: Tool result is fed back to the LLM
- Repeat until Final Answer

Why ReAct works:
1. Reasoning before acting reduces errors (think before you do)
2. Observations ground the model in real data (less hallucination)
3. The trace is human-readable (interpretable decision-making)
4. Tool use extends capabilities beyond what the model "knows"

This is the foundation of:
- Claude's tool use + thinking
- OpenAI's function calling + chain-of-thought
- LangChain agents
- AutoGPT, CrewAI, etc.

The key insight: let the LLM DECIDE which tool to call and when,
rather than hardcoding a pipeline.
"""

import re
import sys
from dataclasses import dataclass, field

sys.path.insert(0, ".")

from phase2_rag.llm_client import LLMClient, LLMResponse, MockLLMClient

from .tools import ToolRegistry, get_default_tools


REACT_SYSTEM_PROMPT = """You are a helpful assistant that solves problems step by step.

You have access to the following tools:
{tools}

To use a tool, write:
Thought: [your reasoning about what to do next]
Action: tool_name(input)

After each action, you will receive an Observation with the result.

When you have the final answer, write:
Thought: [your final reasoning]
Final Answer: [your answer]

Important:
- Always think before acting
- Use tools when you need information or computation
- If a tool returns an error, try a different approach
- Be concise in your reasoning"""


@dataclass
class AgentStep:
    """One step in the ReAct loop."""
    thought: str = ""
    action: str = ""       # tool_name(input)
    observation: str = ""  # tool result


@dataclass
class AgentResult:
    """Final result of the agent execution."""
    answer: str
    steps: list[AgentStep] = field(default_factory=list)
    n_steps: int = 0
    stopped_reason: str = ""  # "answer", "max_steps", "error"

    def trace(self) -> str:
        """Format the full reasoning trace."""
        parts = []
        for i, step in enumerate(self.steps, 1):
            parts.append(f"--- Step {i} ---")
            if step.thought:
                parts.append(f"Thought: {step.thought}")
            if step.action:
                parts.append(f"Action: {step.action}")
            if step.observation:
                parts.append(f"Observation: {step.observation}")
        parts.append(f"\nFinal Answer: {self.answer}")
        return "\n".join(parts)


class ReActAgent:
    """ReAct agent that reasons and acts with tools.

    Usage:
        agent = ReActAgent(llm=LLMClient(), tools=get_default_tools())
        result = agent.run("What is the square root of 144 plus 13?")
        print(result.answer)
        print(result.trace())
    """

    def __init__(
        self,
        llm: LLMClient | MockLLMClient,
        tools: ToolRegistry | None = None,
        max_steps: int = 10,
        verbose: bool = True,
    ):
        self.llm = llm
        self.tools = tools or get_default_tools()
        self.max_steps = max_steps
        self.verbose = verbose

    def run(self, question: str) -> AgentResult:
        """Run the ReAct loop until an answer is found or max steps reached.

        The loop:
        1. Build prompt with history of thoughts/actions/observations
        2. Ask LLM to think and act
        3. Parse response for Action or Final Answer
        4. If Action: execute tool, add observation, go to 1
        5. If Final Answer: return result
        """
        system = REACT_SYSTEM_PROMPT.format(tools=self.tools.format_for_prompt())
        steps: list[AgentStep] = []
        conversation = f"Question: {question}\n"

        for i in range(self.max_steps):
            # Ask LLM
            response = self.llm.generate(
                prompt=conversation,
                system=system,
                temperature=0.3,
                stop=["Observation:"],
            )

            text = response.text.strip()

            # Parse thought
            thought = self._extract_thought(text)
            # Parse action or final answer
            action = self._extract_action(text)
            final_answer = self._extract_final_answer(text)

            step = AgentStep(thought=thought)

            if self.verbose:
                if thought:
                    print(f"  Thought: {thought}")

            if final_answer:
                if self.verbose:
                    print(f"  Final Answer: {final_answer}")
                return AgentResult(
                    answer=final_answer,
                    steps=steps,
                    n_steps=i + 1,
                    stopped_reason="answer",
                )

            if action:
                step.action = action
                # Execute the tool
                tool_name, tool_input = self._parse_action(action)
                observation = self.tools.execute(tool_name, tool_input)
                step.observation = observation

                if self.verbose:
                    print(f"  Action: {action}")
                    print(f"  Observation: {observation}")

                # Append to conversation history
                conversation += f"Thought: {thought}\n"
                conversation += f"Action: {action}\n"
                conversation += f"Observation: {observation}\n"
            else:
                # No action and no final answer — LLM is confused
                conversation += f"{text}\n"
                conversation += "Please use an Action or provide a Final Answer.\n"

            steps.append(step)

        # Max steps reached
        return AgentResult(
            answer="I was unable to find an answer within the step limit.",
            steps=steps,
            n_steps=self.max_steps,
            stopped_reason="max_steps",
        )

    @staticmethod
    def _extract_thought(text: str) -> str:
        """Extract the Thought: line from LLM output."""
        match = re.search(r"Thought:\s*(.+?)(?=\n(?:Action:|Final Answer:)|$)", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_action(text: str) -> str:
        """Extract the Action: line from LLM output."""
        match = re.search(r"Action:\s*(.+?)(?=\n|$)", text)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_final_answer(text: str) -> str:
        """Extract Final Answer from LLM output."""
        match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _parse_action(action: str) -> tuple[str, str]:
        """Parse 'tool_name(input)' into (tool_name, input).

        Examples:
            'calculator(2 + 3)' → ('calculator', '2 + 3')
            'search_docs(hamlet death)' → ('search_docs', 'hamlet death')
        """
        match = re.match(r"(\w+)\((.+)\)", action)
        if match:
            return match.group(1), match.group(2)
        # Fallback: treat entire action as tool name with no input
        return action, ""
