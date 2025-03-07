"""
test_camera_service.py

Tests for CameraService using mock or dummy checks.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.camera_srv import CameraService

class TestCameraService(unittest.TestCase):

    @patch('cv2.VideoCapture')
    def test_camera_open_close(self, mock_videocapture):
        # Arrange
        service = CameraService(camera_index=0)
        mock_capture_instance = MagicMock()
        mock_videocapture.return_value = mock_capture_instance

        # Act
        service.open_camera()
        service.close_camera()

        # Assert
        mock_videocapture.assert_called_once_with(0)
        mock_capture_instance.release.assert_called_once()

    @patch('cv2.VideoCapture')
    def test_read_frame(self, mock_videocapture):
        service = CameraService(camera_index=0)
        mock_capture_instance = MagicMock()
        mock_videocapture.return_value = mock_capture_instance
        mock_capture_instance.isOpened.return_value = True
        mock_capture_instance.read.return_value = (True, "fake_frame")

        service.open_camera()
        success, frame = service.read_frame()
        self.assertTrue(success)
        self.assertEqual(frame, "fake_frame")
        service.close_camera()

if __name__ == '__main__':
    unittest.main()
