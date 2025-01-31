import unittest
from unittest.mock import MagicMock
from gui.pages.drowsiness_page import Drowsiness

class TestDrowsiness(unittest.TestCase):
    def setUp(self):
        self.page = MagicMock()
        self.drowsiness = Drowsiness(self.page)
        self.drowsiness.main()  # Inicializar los controles necesarios

    def test_initial_state(self):
        self.assertFalse(self.drowsiness.running)
        self.assertIsNone(self.drowsiness.video_thread)
        self.assertIsNone(self.drowsiness.sketch_image_control)
        self.assertIsNotNone(self.drowsiness.original_image_control)

    def test_start_detection(self):
        self.drowsiness.start_detection(None)
        self.assertTrue(self.drowsiness.running)
        self.assertIsNotNone(self.drowsiness.video_thread)
        self.assertTrue(self.drowsiness.luz_roja.visible)
        self.assertFalse(self.drowsiness.start_button.visible)
        self.assertTrue(self.drowsiness.stop_button.visible)

    def test_stop_detection(self):
        self.drowsiness.start_detection(None)
        self.drowsiness.stop_detection(None)
        self.assertFalse(self.drowsiness.running)
        self.assertFalse(self.drowsiness.luz_roja.visible)
        self.assertTrue(self.drowsiness.start_button.visible)

if __name__ == '__main__':
    unittest.main()
