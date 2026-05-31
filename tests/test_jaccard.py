import unittest
import sys
import os

# Ensure the parent directory is in path to import from 'agent'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.validation import tokenize, compute_jaccard_similarity

class TestJaccardTokenization(unittest.TestCase):
    def test_tokenization(self):
        query = "Search for latest Google Q1 earnings report!"
        tokens = tokenize(query)

        # Verify stop words are removed ('for', 'latest') and punctuation stripped
        self.assertIn("google", tokens)
        self.assertIn("q1", tokens)
        self.assertIn("earnings", tokens)
        self.assertIn("report", tokens)
        self.assertNotIn("for", tokens)
        self.assertNotIn("latest", tokens)

    def test_exact_similarity(self):
        str_a = "check Google stock price"
        str_b = "Check Google stock price!"
        similarity = compute_jaccard_similarity(str_a, str_b)

        self.assertEqual(similarity, 1.0)

    def test_partial_similarity(self):
        str_a = "Google Q1 earnings 2026"
        str_b = "Google Q2 earnings 2026"
        # Intersection: {"google", "earnings", "2026"} (size 3)
        # Union: {"google", "q1", "q2", "earnings", "2026"} (size 5)
        # Jaccard: 3/5 = 0.6
        similarity = compute_jaccard_similarity(str_a, str_b)

        self.assertEqual(similarity, 0.6)

    def test_zero_similarity(self):
        str_a = "Apple stock growth"
        str_b = "Google weather forecast"
        similarity = compute_jaccard_similarity(str_a, str_b)

        self.assertEqual(similarity, 0.0)

if __name__ == '__main__':
    unittest.main()
