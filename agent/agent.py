import json
import re
from providers.router import LLMProvider
from tools.registry import ToolRegistry
from .prompts import PromptCompiler
from .scratchpad import Scratchpad
from .validation import validate_tool_query

class LatticeAgent:
    """
    LatticeAgent coordinates the core orchestrator loop, managing LLM
    reasoning, tool triggers, and active loop prevention checks.
    """
    def __init__(self, provider: LLMProvider, registry: ToolRegistry, config: dict):
        self.provider = provider
        self.registry = registry
        self.compiler = PromptCompiler(config.get("project_root", "."))
        self.max_steps = config.get("max_steps", 10)
        self.jaccard_threshold = config.get("jaccard_threshold", 0.7)

    def run(self, task: str, on_step=None) -> str:
        """
        Runs the main autonomous agent loop for a given task.
        """
        scratchpad = Scratchpad()
        current_step = 0
        loop_warning = None

        print(f"\n\x1b[36;1m[Lattice] Bootstrapping research for task:\x1b[0m \"{task}\"")
        print(f"\x1b[90mRunning with Provider: {self.provider.name} | Max Steps: {self.max_steps}\x1b[0m\n")

        while current_step < self.max_steps:
            current_step += 1
            print(f"\x1b[90m--- Starting Step {current_step}/{self.max_steps} ---\x1b[0m")

            # 1. Compile prompt context
            tools_string = self.registry.get_tools_list_string()
            system_prompt = self.compiler.compile_system_prompt(tools_string)
            user_prompt = self.compiler.compile_user_prompt(task, scratchpad.format_for_prompt(), loop_warning)

            # Reset warning for next step
            loop_warning = None

            # 2. Query active provider
            try:
                raw_response = self.provider.generate(system_prompt, user_prompt)
            except Exception as e:
                print(f"\x1b[31mLLM Generation Error during Step {current_step}:\x1b[0m {e}")
                return f"I encountered an issue generating a response with the configured LLM provider: {e}"

            # 3. Parse tool calls
            parsed_call = self._parse_tool_call(raw_response)

            if parsed_call:
                name = parsed_call.get("name")
                args = parsed_call.get("arguments", {})

                # Extract primary search query or URL to validate similarity loop triggers
                main_parameter = str(args.get("query") or args.get("url") or args.get("symbol") or json.dumps(args))

                # 4. Perform Jaccard validation
                history = scratchpad.get_tool_query_history()
                validation = validate_tool_query(main_parameter, history, self.jaccard_threshold)

                # Extract any logical thought preamble before the tool call
                thought = self._extract_thought(raw_response) or f"Executing tool {name}."

                scratchpad.add_step(thought, parsed_call)

                if validation["is_loop"]:
                    print(f"\x1b[31;1m[Loop Guard] Looping query detected! Similarity: {validation['similarity'] * 100:.1f}%\x1b[0m")
                    # Intercept execution: write warning to scratchpad and notify loop_warning prompt compiler
                    scratchpad.add_last_result(validation["warning_message"])
                    loop_warning = validation["warning_message"]
                else:
                    # Execute tool normally
                    print(f"\x1b[35m[Lattice Tool] Invoking: {name}\x1b[0m (Arguments: {json.dumps(args)})")
                    result = self.registry.execute(name, args)
                    scratchpad.add_last_result(result)

                # Trigger step callback for REPL updates
                if on_step:
                    on_step(scratchpad)
            else:
                # No tool call parsed. This represents the final response from Lattice!
                print(f"\x1b[32;1m[Lattice] Final synthesized answer ready.\x1b[0m\n")
                return raw_response

        return f"Lattice reached the maximum step limit of {self.max_steps} without resolving the task. Research context:\n\n{scratchpad.format_for_prompt()}"

    def _parse_tool_call(self, response: str) -> dict:
        """Parses the JSON tool_call blocks out of markdown tags."""
        match = re.search(r"```tool_call\s*([\s\S]+?)\s*```", response)
        if match:
            try:
                parsed = json.loads(match.group(1).strip())
                if "name" in parsed and "arguments" in parsed:
                    return parsed
            except Exception as e:
                print(f"Failed to parse tool call JSON block: {e}")
        return None

    def _extract_thought(self, response: str) -> str:
        """Extracts text reasoning block located outside of tool_call blocks."""
        return re.sub(r"```tool_call[\s\S]+?```", "", response).strip()
