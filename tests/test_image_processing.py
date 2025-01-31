import unittest
import cv2
import base64
from gui.pages.drowsiness_page import Drowsiness
from unittest.mock import MagicMock

class TestImageProcessing(unittest.TestCase):
    def setUp(self):
        self.page = MagicMock()
        self.drowsiness = Drowsiness(self.page)

    def test_get_placeholder_image(self):
        placeholder_image = self.drowsiness.get_placeholder_image()
        self.assertIsInstance(placeholder_image, str)
        self.assertTrue(placeholder_image.startswith('/9j/'))  # Check if it's a base64 encoded JPEG

    def test_cv2_to_base64(self):
        image = cv2.imread(self.drowsiness.images.image_5)
        base64_image = self.drowsiness.cv2_to_base64(image)
        self.assertIsInstance(base64_image, str)
        self.assertTrue(base64_image.startswith('/9j/'))  # Check if it's a base64 encoded JPEG

if __name__ == '__main__':
    unittest.main()
