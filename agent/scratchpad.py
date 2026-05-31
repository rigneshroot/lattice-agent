import json

class Scratchpad:
    """
    Scratchpad holds the history of thoughts, actions, and observations
    made during a single agent session.
    """
    def __init__(self):
        self.steps = []

    def add_step(self, thought: str, tool_call: dict = None):
        """Adds a new step (thought and potential action)."""
        self.steps.append({
            "step_index": len(self.steps) + 1,
            "thought": thought,
            "tool_call": tool_call,
            "tool_result": None
        })

    def add_last_result(self, result: str):
        """Appends the result of the last step's tool call."""
        if self.steps:
            self.steps[-1]["tool_result"] = result

    def get_tool_query_history(self) -> list:
        """
        Retrieves all executed tool query strings for similarity validation.
        Extracts the search query, URL, or main parameter.
        """
        history = []
        for step in self.steps:
            tool_call = step.get("tool_call")
            if tool_call:
                args = tool_call.get("arguments", {})
                if args:
                    # Extract the main query parameter if possible
                    main_arg = args.get("query") or args.get("url") or args.get("symbol") or json.dumps(args)
                    history.append(str(main_arg))
        return history

    def format_for_prompt(self) -> str:
        """Formats the scratchpad into a readable markdown string for prompt context injection."""
        if not self.steps:
            return ""

        formatted_steps = []
        for step in self.steps:
            step_str = f"### Step {step['step_index']}\n"
            step_str += f"**Thought**: {step['thought']}\n"
            
            tool_call = step.get("tool_call")
            if tool_call:
                step_str += f"**Tool Call**: ```json\n{json.dumps(tool_call, indent=2)}\n```\n"
                
                tool_result = step.get("tool_result")
                if tool_result is not None:
                    # Trim long tool outputs for context window management
                    trimmed_result = (
                        tool_result[:3000] + "\n... [TRUNCATED FOR LENGTH] ..."
                        if len(tool_result) > 3000
                        else tool_result
                    )
                    step_str += f"**Result**: {trimmed_result}\n"
                else:
                    step_str += "**Result**: [Running / Awaiting output...]\n"
            
            formatted_steps.append(step_str)

        return "\n---\n\n".join(formatted_steps)

    def format_for_terminal(self) -> str:
        """Formats the scratchpad into a highly aesthetic, colored output for terminal presentation."""
        if not self.steps:
            return "\x1b[90mNo research steps taken yet.\x1b[0m"

        formatted_steps = []
        for step in self.steps:
            step_str = f"\x1b[36;1m[Step {step['step_index']}]\x1b[0m\n"
            step_str += f"\x1b[33mThought:\x1b[0m {step['thought']}\n"
            
            tool_call = step.get("tool_call")
            if tool_call:
                step_str += f"\x1b[35mAction:\x1b[0m {tool_call.get('name')} (args: {json.dumps(tool_call.get('arguments'))})\n"
                
                tool_result = step.get("tool_result")
                if tool_result is not None:
                    preview = tool_result.split("\n")[0][:80]
                    step_str += f"\x1b[32mObservation:\x1b[0m {preview}{'...' if len(tool_result) > 80 else ''} ({len(tool_result)} chars)\n"
            
            formatted_steps.append(step_str)

        return "\n".join(formatted_steps)

    def get_steps(self) -> list:
        return self.steps
class ScratchpadStep:
    """Helper typing model representation if needed."""
    pass
