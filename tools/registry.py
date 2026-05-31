from .base import BaseTool
from .web_search import WebSearchTool
from .reader import WebReaderTool
from .whatsapp import WhatsAppTool

class ToolRegistry:
    """
    ToolRegistry handles registration, descriptions compilation,
    and routing of registered execution tools.
    """
    def __init__(self):
        self.tools = {}
        
        # Register default tools
        self.register(WebSearchTool())
        self.register(WebReaderTool())
        self.register(WhatsAppTool())


    def register(self, tool: BaseTool):
        """Registers a tool inside the registry dictionary."""
        self.tools[tool.name] = tool

    def get_all_tools(self) -> list:
        """Returns all registered tool objects."""
        return list(self.tools.values())

    def get_tools_list_string(self) -> str:
        """Formats details and parameters schemas of all registered tools for prompt injection."""
        blocks = []
        for tool in self.get_all_tools():
            blocks.append(tool.format_for_system_prompt())
        return "\n---\n\n".join(blocks)

    def execute(self, name: str, arguments: dict) -> str:
        """
        Executes a tool by its name with provided arguments dictionary.
        Returns the output string from execution.
        """
        tool = self.tools.get(name)
        if not tool:
            available = ", ".join(self.tools.keys())
            return f"Error: Tool \"{name}\" is not registered. Available tools are: {available}"

        try:
            # We unpack the kwargs for the execution.
            # Standard type checking can be added or handled internally by Zod-equivalents or directly in Python.
            return tool.execute(**arguments)
        except TypeError as e:
            print(f"Type error executing tool \"{name}\" with args {arguments}: {e}")
            return f"Error: Invalid arguments passed to tool \"{name}\". Error: {e}"
        except Exception as e:
            print(f"Exception during tool \"{name}\" execution: {e}")
            return f"Error executing tool \"{name}\": {e}"

    def has_tool(self, name: str) -> bool:
        """Checks if a tool name is registered."""
        return name in self.tools
