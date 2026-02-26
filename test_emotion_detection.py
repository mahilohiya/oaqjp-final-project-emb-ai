import unittest
from EmotionDetection import emotion_detector

class TestEmotionDetection(unittest.TestCase):

    def test_valid_input(self):
        result = emotion_detector("I am happy")
        self.assertIsNotNone(result["dominant_emotion"])

    def test_empty_input(self):
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])

if __name__ == "__main__":
    unittest.main()