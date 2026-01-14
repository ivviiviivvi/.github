
import unittest
import json
from mouthpiece_filter import MouthpieceFilter

class TestMouthpieceFilterRegression(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.filter = MouthpieceFilter()
        self.sample_text = """
        I have a requirement. I need you to build a system that feels like a river of data flowing into the ocean.
        It should handle "UserAuthentication" and 'DataProcessing' modules.
        First, step 1: initialize the core. Then connect the database.
        The system needs to be robust. Can you help me?
        """

    def test_concepts_extraction(self):
        analysis = self.filter._analyze_text(self.sample_text)
        concepts = sorted(analysis['concepts'])
        # We expect "UserAuthentication", "DataProcessing" to be found.
        self.assertIn("UserAuthentication", concepts)
        self.assertIn("DataProcessing", concepts)
        self.assertIn("First", concepts) # Capitalized word

    def test_metaphor_extraction(self):
        analysis = self.filter._analyze_text(self.sample_text)
        metaphors = analysis['metaphors']
        # "feels like" is in the text and the metaphor list
        found = any("feels like" in m.lower() for m in metaphors)
        self.assertTrue(found, f"Metaphor 'feels like' not found in {metaphors}")

    def test_structure(self):
        structure = self.filter._extract_structure(self.sample_text, {})
        self.assertTrue(structure['has_steps'])
        self.assertTrue(structure['has_context'])

    def test_full_transform(self):
        result = self.filter.transform(self.sample_text)
        self.assertIsNotNone(result['prompt'])
        self.assertIn("UserAuthentication", result['prompt'] + str(result['analysis']))

if __name__ == '__main__':
    unittest.main()
