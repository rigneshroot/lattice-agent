import os

class PromptCompiler:
    """
    PromptCompiler handles compiling the system instructions and user research templates.
    It dynamically loads SOUL.md to ground the agent's identity.
    """
    def __init__(self, project_root: str):
        self.soul_path = os.path.join(project_root, "SOUL.md")

    def get_soul(self) -> str:
        """Reads SOUL.md from disk, falling back to default identity if missing."""
        try:
            if os.path.exists(self.soul_path):
                with open(self.soul_path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"Warning: Could not read SOUL.md: {e}. Using default persona.")
        
        return "# SOUL OF LATTICE\nYou are Lattice, an autonomous cognitive synthesizer designed to navigate complex research environments."

    def compile_system_prompt(self, tools_list_string: str) -> str:
        """Compiles the system prompt incorporating the agent's identity, active tools, and instructions."""
        soul = self.get_soul()
        return f"""{soul}

## Operational Environment & Tools
You have access to a suite of execution tools. You can invoke them using the structured JSON tool-call schema.

Available Tools:
{tools_list_string}

## Decision Making Protocol
1. **Analyze**: Deconstruct the task. Formulate a hypothesis.
2. **Explore**: Use tools to query information, read details, and gather facts.
3. **Verify**: Double check your outputs. Check for looping behaviors.
4. **Synthesize**: When you have sufficient data, formulate a final comprehensive response.

## Output Formatting Rules
To call a tool, respond with a JSON block containing the tool name and arguments. Wrap it in a markdown block with the `tool_call` language identifier:

```tool_call
{{
  "name": "tool_name",
  "arguments": {{
    "arg1": "value1"
  }}
}}
```

If you have completed your research and have the final answer, do NOT call any tools. Instead, respond with your final comprehensive response. Make sure to ground your final answer in the facts gathered.
"""

    def compile_user_prompt(self, task: str, scratchpad_logs: str, warning: str = None) -> str:
        """Formats the user message with the active scratchpad and optional warnings."""
        prompt = f"""## Active Task
{task}

## Active Research Scratchpad (Your History)
{scratchpad_logs or "No tools have been called yet."}
"""
        if warning:
            prompt += f"""
> [!WARNING]
> COGNITIVE GUARD TRIGGERED:
> {warning}
"""
        prompt += "\nProvide your next thought, tool call, or final synthesized response."
        return prompt
