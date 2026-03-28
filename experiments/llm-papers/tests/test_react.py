"""Tests for ReAct agent components.

Tests tool registry, action parsing, and agent loop — no LLM needed.
"""

from phase2_rag.llm_client import MockLLMClient
from phase2_react.react_agent import ReActAgent
from phase2_react.tools import ToolRegistry, calculator, get_default_tools


class TestCalculatorTool:
    def test_basic_math(self):
        assert calculator("2 + 3") == "5"
        assert calculator("10 * 5") == "50"

    def test_advanced_math(self):
        assert calculator("sqrt(16)") == "4.0"
        assert calculator("2 ** 10") == "1024"

    def test_caret_as_power(self):
        assert calculator("2^10") == "1024"

    def test_invalid_expression(self):
        result = calculator("import os")
        assert "Error" in result


class TestToolRegistry:
    def test_register_and_execute(self):
        registry = ToolRegistry()
        registry.register("echo", "Echoes input", lambda x: f"Echo: {x}")
        result = registry.execute("echo", "hello")
        assert result == "Echo: hello"

    def test_unknown_tool(self):
        registry = ToolRegistry()
        result = registry.execute("nonexistent", "input")
        assert "Error" in result

    def test_format_for_prompt(self):
        registry = get_default_tools()
        prompt = registry.format_for_prompt()
        assert "calculator" in prompt


class TestReActParsing:
    def test_extract_thought(self):
        text = "Thought: I need to calculate something\nAction: calculator(2+3)"
        thought = ReActAgent._extract_thought(text)
        assert "calculate" in thought

    def test_extract_action(self):
        text = "Thought: blah\nAction: calculator(2+3)"
        action = ReActAgent._extract_action(text)
        assert action == "calculator(2+3)"

    def test_extract_final_answer(self):
        text = "Thought: I know the answer.\nFinal Answer: 42"
        answer = ReActAgent._extract_final_answer(text)
        assert answer == "42"

    def test_parse_action(self):
        name, inp = ReActAgent._parse_action("calculator(2 + 3)")
        assert name == "calculator"
        assert inp == "2 + 3"

    def test_parse_action_with_complex_input(self):
        name, inp = ReActAgent._parse_action("search_docs(hamlet death soliloquy)")
        assert name == "search_docs"
        assert "hamlet" in inp


class TestReActAgent:
    def test_immediate_answer(self):
        llm = MockLLMClient(responses={
            "6 * 7": "Thought: This is obvious.\nFinal Answer: 42"
        })
        agent = ReActAgent(llm=llm, verbose=False)
        result = agent.run("What is 6 * 7?")
        assert result.answer == "42"
        assert result.stopped_reason == "answer"

    def test_tool_use(self):
        # First call: LLM decides to use calculator
        # Second call: LLM provides final answer after seeing observation
        call_count = 0

        class SequentialMock:
            def generate(self, prompt, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    from phase2_rag.llm_client import LLMResponse
                    return LLMResponse(text="Thought: I need to calculate.\nAction: calculator(2 + 3)")
                else:
                    from phase2_rag.llm_client import LLMResponse
                    return LLMResponse(text="Thought: The calculator says 5.\nFinal Answer: 5")

        agent = ReActAgent(llm=SequentialMock(), verbose=False)
        result = agent.run("What is 2 + 3?")
        assert result.answer == "5"
        assert result.n_steps >= 1

    def test_max_steps_limit(self):
        llm = MockLLMClient(responses={
            "default": "Thought: I need to think more.\nAction: calculator(1+1)"
        })
        agent = ReActAgent(llm=llm, max_steps=3, verbose=False)
        result = agent.run("Impossible question")
        assert result.stopped_reason == "max_steps"


if __name__ == "__main__":
    import traceback

    test_classes = [TestCalculatorTool, TestToolRegistry, TestReActParsing, TestReActAgent]
    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        for method_name in sorted(dir(instance)):
            if not method_name.startswith("test_"):
                continue
            try:
                getattr(instance, method_name)()
                print(f"  PASS  {cls.__name__}.{method_name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL  {cls.__name__}.{method_name}: {e}")
                traceback.print_exc()
                failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
