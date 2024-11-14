import unittest
from src.preprocessing.data_loader import load_images

class TestDataLoader(unittest.TestCase):
    def test_load_images(self):
        images = load_images('./data/raw/')
        self.assertIsInstance(images, dict)
        self.assertGreater(len(images), 0, "No images loaded from the directory")

if __name__ == "__main__":
    unittest.main()
