"""Phase 2B: ReAct Agent (Reasoning + Acting).

Paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
       (Yao et al., 2022 / ICLR 2023)

ReAct interleaves reasoning traces with tool-use actions:
  Thought: I need to find X...
  Action: search_docs("X")
  Observation: [results from tool]
  Thought: Based on the results, the answer is...
  Final Answer: ...

This is the foundation of modern agentic systems (AutoGPT, Claude tools, etc.)
"""
