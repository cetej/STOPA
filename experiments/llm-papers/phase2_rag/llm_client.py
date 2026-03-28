"""Unified LLM client — abstracts different backends behind one interface.

Supports:
1. OpenAI-compatible API (OpenAI, Anthropic via proxy, Ollama, vLLM, etc.)
2. Mock client for testing (deterministic responses)

Configuration via environment variables:
    LLM_BASE_URL  — API base URL (default: http://localhost:11434/v1 for Ollama)
    LLM_API_KEY   — API key (default: "ollama" for local)
    LLM_MODEL     — Model name (default: "llama3.2:3b")

Why this design?
- RAG and ReAct need a "smart" LLM for generation/reasoning
- Our Phase 1 tiny model is too small for meaningful QA or reasoning
- A thin client keeps the code backend-agnostic
- Ollama is the easiest local option (free, no API key, runs on your GPU)
"""

import json
import os
import sys
from dataclasses import dataclass, field

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


@dataclass
class LLMResponse:
    """Structured response from the LLM."""
    text: str
    model: str = ""
    usage: dict = field(default_factory=dict)  # tokens used


class LLMClient:
    """OpenAI-compatible API client.

    Works with:
    - Ollama: LLM_BASE_URL=http://localhost:11434/v1
    - OpenAI: LLM_BASE_URL=https://api.openai.com/v1 LLM_API_KEY=sk-...
    - vLLM:   LLM_BASE_URL=http://localhost:8000/v1
    - Any OpenAI-compatible endpoint
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self.base_url = (base_url or os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")).rstrip("/")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "ollama")
        self.model = model or os.getenv("LLM_MODEL", "llama3.2:3b")

    def generate(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> LLMResponse:
        """Generate text from a prompt using the chat completions API.

        Args:
            prompt: User message / prompt text
            system: Optional system message
            temperature: Sampling temperature (0 = deterministic)
            max_tokens: Max tokens to generate
            stop: Stop sequences

        Returns:
            LLMResponse with generated text
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if stop:
            payload["stop"] = stop

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()

            return LLMResponse(
                text=data["choices"][0]["message"]["content"],
                model=data.get("model", self.model),
                usage=data.get("usage", {}),
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to LLM at {self.base_url}. "
                f"Start Ollama with: ollama run {self.model}"
            )
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"LLM API error: {e.response.status_code} — {e.response.text[:200]}")


class MockLLMClient:
    """Deterministic mock client for testing.

    Returns canned responses based on prompt content — useful for
    testing RAG/ReAct logic without needing a real LLM.
    """

    def __init__(self, responses: dict[str, str] | None = None):
        self.responses = responses or {}
        self.call_log: list[str] = []

    def generate(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> LLMResponse:
        self.call_log.append(prompt)

        # Check for keyword matches in responses dict
        for keyword, response in self.responses.items():
            if keyword.lower() in prompt.lower():
                return LLMResponse(text=response, model="mock")

        # Default response
        return LLMResponse(
            text="I don't have enough information to answer that question.",
            model="mock",
        )
