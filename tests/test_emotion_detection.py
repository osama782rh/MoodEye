import unittest
import cv2
from src.emotion_detection.emotion_classifier import classify_emotion

class TestEmotionDetection(unittest.TestCase):
    def test_classify_emotion(self):
        img = cv2.imread('./data/raw/sample_face.jpg')
        emotion = classify_emotion(img)
        self.assertIsInstance(emotion, str)
        self.assertTrue(len(emotion) > 0, "Emotion not detected")

if __name__ == "__main__":
    unittest.main()
