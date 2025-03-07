# Camera Image Processing

A small application that captures an image from your webcam, converts it to 8-bit grayscale, and generates a grayscale histogram.

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- Matplotlib
- Numpy
- (Optional) PyTest for running tests

Install dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run

1. Clone or download this repository:

```bash
git clone https://github.com/burakaksoy/CameraImageProcessing-Assignment.git
```

2. Move into the project directory:

```bash
cd CameraImageProcessing-Assignment
```

3. Install dependencies (as shown above).

4. Run the main application:

```bash
python src/main.py
```

## Project Structure
* src/
    * camera_srv/:
        * `camera_service.py`: Camera driver implementation that uses OpenCV to capture frames
        * `image_processor.py`: Utility functions for image conversion to grayscale
        * `histogram_generator.py`: Logic for generating a histogram from a grayscale image
    * `main.py`: Application entry point; orchestrates capturing, processing, and displaying images/histograms

* tests/:

    * `test_camera_service.py`: Basic tests for the camera service (mocking out webcam if needed)
    * `test_image_processor.py`: Tests for grayscale conversion
    * `test_histogram_generator.py`: Tests for histogram generation

## Sample Outputs
After capturing an image from the webcam, you should see:
1. A **grayscale image** window
2. A **maplotlib histogram** windows showing grayscale pixel distribution

<!-- Add image below -->
![Sample Image](.imgs/sample.png)

## Running Tests 
You can run tests using pytest. For example:
```bash
PYTHONPATH=$(pwd) pytest tests
```


## Notes/Assumptions

* Camera index is set to `0` by default. If you have multiple webcams or use a different device, you may need to change this.
* The histogram is displayed in a Matplotlib window; if you close it, the application continues running until you press `ESC` in the webcam feed window.
* This sample does not include advanced error handling or robust cross-platform testing, but it should be portable to Windows, macOS, and Linux as long as OpenCV and Matplotlib can be installed.