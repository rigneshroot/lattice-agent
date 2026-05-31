import unittest
import sys
import os

# Ensure the parent directory is in path to import from 'agent'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.whatsapp import WhatsAppTool
from tools.registry import ToolRegistry
from gateways.whatsapp import WhatsAppGateway
from providers.router import MockProvider
from agent.agent import LatticeAgent

class TestWhatsAppIntegration(unittest.TestCase):
    def test_whatsapp_tool_metadata(self):
        tool = WhatsAppTool()
        self.assertEqual(tool.name, "send_whatsapp_message")
        self.assertIn("WhatsApp", tool.description)
        
        # Verify JSON Schema is defined correctly
        schema = tool.schema
        self.assertEqual(schema["type"], "object")
        self.assertIn("recipient", schema["properties"])
        self.assertIn("message", schema["properties"])
        self.assertIn("recipient", schema["required"])

    def test_tool_registry_registration(self):
        registry = ToolRegistry()
        self.assertTrue(registry.has_tool("send_whatsapp_message"))
        
        tool = registry.tools["send_whatsapp_message"]
        self.assertIsInstance(tool, WhatsAppTool)

    def test_whatsapp_tool_fallback_execution(self):
        # Explicitly clear environment variable fields to ensure mock fallback triggers
        os.environ.pop("TWILIO_ACCOUNT_SID", None)
        os.environ.pop("TWILIO_AUTH_TOKEN", None)
        
        tool = WhatsAppTool()
        result = tool.execute(recipient="+14155238886", message="Lattice verification alert.")
        
        self.assertIn("WhatsApp Simulator Dispatch Results", result)
        self.assertIn("recipient number: +14155238886", result.lower())
        self.assertIn("lattice verification alert.", result.lower())
        self.assertIn("Simulated Send SUCCESS", result)

    def test_whatsapp_gateway_handler(self):
        provider = MockProvider()
        registry = ToolRegistry()
        agent = LatticeAgent(provider, registry, {
            "project_root": os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            "max_steps": 2,
            "jaccard_threshold": 0.7
        })
        
        gateway = WhatsAppGateway(agent)
        response = gateway.handle_incoming_message(
            sender_number="whatsapp:+14155238886",
            message_text="Simulated user inbound request."
        )
        
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

if __name__ == '__main__':
    unittest.main()
