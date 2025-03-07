"""
histogram_generator.py

Module for generating and displaying histogram data from an 8-bit grayscale image.
"""

import numpy as np
import matplotlib.pyplot as plt

def compute_histogram(grayscale_img):
    """
    Compute histogram data for an 8-bit grayscale image.
    Args:
        grayscale_img (numpy.ndarray): 8-bit grayscale image.
    Returns:
        hist (numpy.ndarray): A 256-length array with pixel counts for each grayscale value.
    """
    if grayscale_img is None:
        raise ValueError("Grayscale image is None.")
    # Flatten the image array and compute histogram
    hist, _ = np.histogram(grayscale_img.ravel(), bins=256, range=(0, 256))
    return hist

def display_histogram(hist):
    """
    Display a histogram of the grayscale values using matplotlib.
    Args:
        hist (numpy.ndarray): A 256-length array with pixel counts for each grayscale value.
    """
    plt.figure("Grayscale Histogram")
    plt.title("Histogram of Grayscale Values")
    plt.xlabel("Pixel Value")
    plt.ylabel("Count")
    plt.plot(hist)  # Plot the histogram
    plt.xlim([-0.5, 255.5])
    plt.show()
