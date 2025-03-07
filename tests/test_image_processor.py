"""
test_histogram_generator.py

Tests for histogram_generator module.
"""

import unittest
import numpy as np
from src.camera_srv import compute_histogram

class TestHistogramGenerator(unittest.TestCase):

    def test_compute_histogram_valid(self):
        # Create a dummy grayscale image with known values
        dummy_grayscale = np.array([[0, 0, 255, 255],
                                    [128, 128, 64, 64]], dtype=np.uint8)
        hist = compute_histogram(dummy_grayscale)

        # Check histogram length
        self.assertEqual(len(hist), 256)

        # We know there are 2 zeros, 2 255s, 2 128s, 2 64s
        self.assertEqual(hist[0], 2)
        self.assertEqual(hist[64], 2)
        self.assertEqual(hist[128], 2)
        self.assertEqual(hist[255], 2)

    def test_compute_histogram_none(self):
        with self.assertRaises(ValueError):
            compute_histogram(None)

if __name__ == '__main__':
    unittest.main()
