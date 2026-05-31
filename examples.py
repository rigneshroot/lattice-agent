import os
import sys

# Ensure the active directory is in the path to allow direct imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from providers.router import MockProvider
from tools.registry import ToolRegistry
from tools.base import BaseTool
from agent.agent import LatticeAgent

# =====================================================================
# EXAMPLE 1: Running the Agent Programmatically
# =====================================================================
def run_basic_agent_example():
    print("=== Example 1: Programmatic Agent Execution ===")
    
    # 1. Initialize our lightweight Mock Provider for local testing
    provider = MockProvider()
    
    # 2. Setup the tool registry
    registry = ToolRegistry()
    
    # 3. Create the agent with parameters
    agent = LatticeAgent(provider, registry, {
        "project_root": project_root,
        "max_steps": 5,
        "jaccard_threshold": 0.7
    })
    
    # 4. Define the task
    task = "Verify loop safety by checking Google stock prices twice."
    
    # 5. Run the agent and capture the final synthesized response
    final_response = agent.run(task)
    
    print("\n--- Programmatic Final Answer ---")
    print(final_response)
    print("---------------------------------\n")


# =====================================================================
# EXAMPLE 2: Extending Lattice with a Custom Tool
# =====================================================================

# Define a custom valuation tool by inheriting from BaseTool
class CompanyValuationTool(BaseTool):
    @property
    def name(self) -> str:
        return "company_valuation"

    @property
    def description(self) -> str:
        return "Calculates structural valuation metrics for a given corporate ticker."

    @property
    def schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "The stock ticker symbol (e.g. GOOGL)."},
                "discount_rate": {"type": "number", "description": "The discount rate percentage (e.g. 0.08)."}
            },
            "required": ["ticker"]
        }

    def execute(self, ticker: str, discount_rate: float = 0.08) -> str:
        ticker_upper = ticker.upper()
        print(f"[company_valuation] Calculating valuation metrics for {ticker_upper} using discount rate of {discount_rate*100}%...")
        
        # Static mock valuation calculations for demonstration
        if ticker_upper in ("GOOGL", "GOOG"):
            fair_value = 195.20
            current_price = 174.50
            margin_of_safety = ((fair_value - current_price) / fair_value) * 100
            
            return f"""[Valuation Results for {ticker_upper}]
- Fair Value Estimate: ${fair_value:.2f}
- Current Market Price: ${current_price:.2f}
- Margin of Safety: {margin_of_safety:.1f}%
- Recommendation: Undervalued. Strong valuation foundation."""
        
        return f"[company_valuation] Calculated generic valuation for ticker {ticker_upper} using default DCF model."


def run_custom_tool_example():
    print("=== Example 2: Registering a Custom Tool ===")
    
    # 1. Initialize registry and instantiate our custom valuation tool
    registry = ToolRegistry()
    custom_tool = CompanyValuationTool()
    
    # 2. Register the tool programmatically
    registry.register(custom_tool)
    
    print(f"Successfully registered custom tool: {custom_tool.name}")
    print(f"Tool description: {custom_tool.description}")
    
    # 3. Verify execution routing works
    args = {"ticker": "GOOGL", "discount_rate": 0.09}
    print(f"\nInvoking '{custom_tool.name}' via registry router...")
    result = registry.execute(custom_tool.name, args)
    
    print("\n--- Tool Execution Output ---")
    print(result)
    print("-----------------------------\n")


# =====================================================================
# MAIN RUNNER
# =====================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("Lattice Agent - Programmatic Developer Examples")
    print("=====================================================\n")
    
    # Run Example 1
    run_basic_agent_example()
    
    # Run Example 2
    run_custom_tool_example()
