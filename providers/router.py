import os
import json
import urllib.request
import urllib.error

class LLMProvider:
    """Interface definition for LLM providers."""
    @property
    def name(self) -> str:
        raise NotImplementedError
        
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError

class GeminiProvider(LLMProvider):
    """GeminiProvider implements LLMProvider using the official new google-genai SDK."""
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        # Import inside class to prevent load failures if package is missing during test bootstrap
        from google import genai
        from google.genai import types
        self._name = "Gemini"
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.types = types

    @property
    def name(self) -> str:
        return self._name

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            config = self.types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.1,  # Low temperature for highly deterministic tool calling and reasoning
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            return response.text or ""
        except Exception as e:
            print(f"Error generating with Gemini Provider: {e}")
            raise e

class OpenAIProvider(LLMProvider):
    """OpenAIProvider implements LLMProvider using the official openai SDK."""
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        from openai import OpenAI
        self._name = "OpenAI"
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    @property
    def name(self) -> str:
        return self._name

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"Error generating with OpenAI Provider: {e}")
            raise e

class OllamaProvider(LLMProvider):
    """OllamaProvider implements LLMProvider for local offline models."""
    def __init__(self, host: str = "http://localhost:11434", model_name: str = "llama3"):
        self._name = "Ollama"
        self.host = host
        self.model_name = model_name

    @property
    def name(self) -> str:
        return self._name

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }
        
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode("utf-8"), 
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                if res.status != 200:
                    raise Exception(f"Ollama returned HTTP status {res.status}")
                data = json.loads(res.read().decode("utf-8"))
                return data.get("response", "")
        except urllib.error.URLError as e:
            print(f"Error connecting to Ollama: {e}")
            raise e

class MockProvider(LLMProvider):
    """MockProvider simulates an intelligent autonomous agent reasoning process without calling external APIs."""
    def __init__(self):
        self._name = "Lattice Mock Engine"
        self.step_counter = 0

    @property
    def name(self) -> str:
        return self._name

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        self.step_counter += 1
        
        # If the Jaccard loop warning was triggered in the user prompt:
        if "LOOPING BEHAVIOR DETECTED" in user_prompt:
            return """Thought: The loop guard has intervened! I recognize that I am repeatedly querying the same stock price of Google. I must immediately pivot my strategy and synthesize what I already know rather than calling another tool.

Based on my previous tool observations, the current stock price of Google (Alphabet Inc.) is $174.50, and the company has shown stellar growth in Q1 with high demand for Google Cloud.

Final Synthesized Resolution:
Google's stock is currently trading at $174.50. Alphabet Inc. has maintained robust performance in Q1 2026, driven by high adoption of custom AI infrastructure in the cloud. We successfully gathered this data and pivoted when redundant queries were detected, maintaining search efficiency."""

        # Step 1: Request tool execution
        if self.step_counter == 1:
            return """Thought: Let's begin our research. The user wants to know the stock price of Google and verify loop safety. I will query the web search tool for Google stock price.

```tool_call
{
  "name": "web_search",
  "arguments": {
    "query": "Google stock price Q1 2026"
  }
}
```"""
        
        # Step 2: Request repeated tool execution to trigger Jaccard guard
        if self.step_counter == 2:
            return """Thought: Excellent, I successfully retrieved Google's stock price of $174.50. Now I will search for the stock price of Google again to test the loop validation guard.

```tool_call
{
  "name": "web_search",
  "arguments": {
    "query": "Google stock price Q1 2026"
  }
}
```"""

        return "Thought: I have finished my research.\n\nFinal Resolution: Research complete."

def create_provider_from_env() -> LLMProvider:
    """Creates and returns the LLM provider configured in environment variables."""
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            print("Warning: OPENAI_API_KEY is empty. Attempting connection anyway...")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return OpenAIProvider(api_key, model)

    if provider == "ollama":
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3")
        return OllamaProvider(host, model)

    # Default: Google Gemini
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        print("Warning: GEMINI_API_KEY is not defined. Defaulting to Lattice Mock Engine.")
        print("This allows you to test the agent loop, Jaccard validation, and tool triggers out-of-the-box!\n")
        return MockProvider()
        
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return GeminiProvider(api_key, model)
