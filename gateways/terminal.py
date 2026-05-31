import os
import sys
from agent.agent import LatticeAgent

class TerminalGateway:
    """
    TerminalGateway handles the CLI prompt REPL loop.
    """
    def __init__(self, agent: LatticeAgent):
        self.agent = agent

    def start(self):
        self.print_banner()

        while True:
            try:
                task = input("\x1b[36;1mLattice > \x1b[0m").strip()
                if not task:
                    continue

                if task.lower() in ("exit", "quit"):
                    print("\n\x1b[33mFarewell. Keep synthesizing.\x1b[0m\n")
                    sys.exit(0)

                print("\n\x1b[90mThinking...\x1b[0m")

                def step_callback(scratchpad):
                    steps = scratchpad.get_steps()
                    last_step = steps[-1]
                    print(f"\n\x1b[32m✔ Step Completed.\x1b[0m")
                    if last_step.get("tool_call"):
                        print(f"  \x1b[90mAction: {last_step['tool_call']['name']}\x1b[0m")
                    print()

                final_answer = self.agent.run(task, on_step=step_callback)

                print("\x1b[32;1m=== SYNTHESIZED RESPONSE ===\x1b[0m")
                print(final_answer)
                print("\x1b[32;1m============================\x1b[0m\n")

            except (KeyboardInterrupt, EOFError):
                print("\n\x1b[33mFarewell. Keep synthesizing.\x1b[0m\n")
                sys.exit(0)
            except Exception as e:
                print(f"\n\x1b[31;1mError executing task:\x1b[0m {e}\n")

    def print_banner(self):
        # Try to clear terminal screen
        os.system("cls" if os.name == "nt" else "clear")
        print("""
\x1b[36;1m=======================================================
   __         ______ ______ __   ______ ______ 
  / /   /\\   /_  __//_  __// /  / ____// ____/ 
 / /   /  \\   / /    / /  / /  / __/  / __/    
/ /___/ /\\ \\ / /    / /  / /__/ /___ / /___    
/____/_/  \\_\\\\_/    /_/  /____/_____//_____/    
                                               
  COGNITIVE SYNTHESIS ENGINE (Python Edition)
=======================================================\x1b[0m
Type any research question to prompt the agent.
Type \x1b[33m'exit'\x1b[0m or \x1b[33m'quit'\x1b[0m to terminate the session.
""")
