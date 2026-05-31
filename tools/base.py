import json

class BaseTool:
    """
    BaseTool represents the abstract interface for all tools registered
    within the Python Lattice Agent framework.
    """
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        raise NotImplementedError

    @property
    def schema(self) -> dict:
        """
        Returns a dict describing the arguments schema in JSON-schema format.
        Example:
        {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
        """
        raise NotImplementedError

    def execute(self, **kwargs) -> str:
        raise NotImplementedError

    def format_for_system_prompt(self) -> str:
        """Helper to format tool properties as a clean block for system prompt injection."""
        return f"""### Tool: `{self.name}`
Description: {self.description}
Parameters Schema:
```json
{json.dumps(self.schema, indent=2)}
```
"""
