"""
test_image_processor.py

Tests for image_processor module.
"""

import unittest
import numpy as np
from src.camera_srv import to_grayscale

class TestImageProcessor(unittest.TestCase):

    def test_to_grayscale_valid(self):
        # Create a dummy color image
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Convert to grayscale
        gray = to_grayscale(dummy_image)
        # Assertions
        self.assertEqual(len(gray.shape), 2)  # Grayscale should have 2 dimensions
        self.assertEqual(gray.shape, (100, 100))

    def test_to_grayscale_none_input(self):
        with self.assertRaises(ValueError):
            to_grayscale(None)

if __name__ == '__main__':
    unittest.main()
