import os
import sys
from dotenv import load_dotenv

# Resolve project path to allow imports from subdirectories
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Load environment configuration variables
load_dotenv()

from providers.router import create_provider_from_env
from tools.registry import ToolRegistry
from agent.agent import LatticeAgent

def main():
    print("\x1b[90mBootstrapping Lattice Agent Systems (Python)...\x1b[0m")

    # Double check that we have Gemini API Key if Gemini is selected as the provider
    provider_name = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider_name == "gemini" and not os.getenv("GEMINI_API_KEY"):
        print("\x1b[33mWarning: GEMINI_API_KEY is not defined in your environmental variables.\x1b[0m")
        print("\x1b[33mThe agent will default to intelligent mock fallbacks during execution.\x1b[0m\n")

    # 1. Initialize Provider Router
    try:
        provider = create_provider_from_env()
    except Exception as e:
        print(f"\x1b[31;1mFailed to initialize active LLM Provider Router:\x1b[0m {e}")
        print("\x1b[90mEnsure you have required dependencies installed via 'pip install -r requirements.txt'\x1b[0m")
        sys.exit(1)

    # 2. Initialize Tool Registry
    registry = ToolRegistry()

    # 3. Setup Agent configuration parameters
    max_steps = int(os.getenv("MAX_STEPS", "10"))
    jaccard_threshold = float(os.getenv("JACCARD_THRESHOLD", "0.7"))

    # 4. Construct Agent
    agent = LatticeAgent(provider, registry, {
        "project_root": project_root,
        "max_steps": max_steps,
        "jaccard_threshold": jaccard_threshold
    })

    # 5. Boot Gateway Interface
    gateway_type = os.getenv("GATEWAY", "terminal").lower()
    if gateway_type == "whatsapp":
        from gateways.whatsapp import WhatsAppGateway
        gateway = WhatsAppGateway(agent)
    else:
        from gateways.terminal import TerminalGateway
        gateway = TerminalGateway(agent)

    gateway.start()

if __name__ == "__main__":
    main()

