import unittest
import sys
import os

# Ensure the parent directory is in path to import from 'agent'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.validation import validate_tool_query

class TestLoopDetection(unittest.TestCase):
    def test_no_loop(self):
        history = [
            "Apple stock price Q1",
            "Google weather forecast"
        ]
        proposed = "Tesla earnings report"
        result = validate_tool_query(proposed, history, 0.7)

        self.assertFalse(result["is_loop"])
        self.assertIsNone(result["warning_message"])

    def test_loop_triggered(self):
        history = [
            "Alphabet stock price Q1 2026",
            "Microsoft revenue growth"
        ]
        proposed = "Alphabet stock price Q1 2026 reports"
        result = validate_tool_query(proposed, history, 0.7)

        self.assertTrue(result["is_loop"])
        self.assertGreaterEqual(result["similarity"], 0.7)
        self.assertIsNotNone(result["warning_message"])
        self.assertIn("LOOPING BEHAVIOR DETECTED", result["warning_message"])

if __name__ == '__main__':
    unittest.main()
