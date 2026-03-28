"""Tool registry for ReAct agent.

Paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
       (Yao et al., 2022)

In ReAct, tools are functions that the agent can call to interact
with the environment. Each tool has:
- A name (used in Action: name(...) format)
- A description (shown to the LLM so it knows when to use it)
- A callable (the actual function)

The tool registry pattern is the foundation of modern tool-use in LLMs:
- Claude's tool_use API
- OpenAI's function calling
- LangChain's tools
All follow this same basic structure.
"""

import math
import re
from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    """A tool that the ReAct agent can use."""
    name: str
    description: str
    fn: Callable[[str], str]  # Takes string input, returns string output


class ToolRegistry:
    """Registry of available tools.

    Provides:
    - Tool registration
    - Tool listing (for the system prompt)
    - Tool execution by name
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, description: str, fn: Callable[[str], str]) -> None:
        """Register a new tool."""
        self._tools[name] = Tool(name=name, description=description, fn=fn)

    def get(self, name: str) -> Tool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def execute(self, name: str, input_str: str) -> str:
        """Execute a tool by name. Returns result or error string."""
        tool = self._tools.get(name)
        if tool is None:
            return f"Error: Unknown tool '{name}'. Available: {', '.join(self._tools.keys())}"
        try:
            return tool.fn(input_str)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def format_for_prompt(self) -> str:
        """Format all tools for inclusion in the system prompt."""
        lines = []
        for tool in self._tools.values():
            lines.append(f"- {tool.name}(input): {tool.description}")
        return "\n".join(lines)

    @property
    def names(self) -> list[str]:
        return list(self._tools.keys())


# === Built-in Tools ===

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Supports: +, -, *, /, **, sqrt, sin, cos, log, pi, e
    """
    # Allow only safe math operations
    allowed = set("0123456789+-*/.() ")
    allowed_funcs = {"sqrt", "sin", "cos", "tan", "log", "abs", "pi", "e", "pow"}

    # Clean the expression
    expr = expression.strip()

    # Replace common math words with Python equivalents
    expr = expr.replace("^", "**")

    # Validate: only allowed characters and function names
    cleaned = expr
    for func in allowed_funcs:
        cleaned = cleaned.replace(func, "")

    if not all(c in allowed for c in cleaned):
        return f"Error: Invalid characters in expression: {expr}"

    # Build safe namespace
    safe_dict = {
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
        "tan": math.tan, "log": math.log, "abs": abs,
        "pi": math.pi, "e": math.e, "pow": pow,
    }

    try:
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_default_tools() -> ToolRegistry:
    """Create a tool registry with built-in tools."""
    registry = ToolRegistry()

    registry.register(
        "calculator",
        "Evaluate mathematical expressions. Input: math expression (e.g., '2 + 3 * 4', 'sqrt(16)').",
        calculator,
    )

    return registry
