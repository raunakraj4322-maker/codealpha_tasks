"""
Video Processor Service
Handles video/webcam input and processes frames with detection and tracking
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List, Callable, Dict, Any
from pathlib import Path
import logging
import time

from ..config import Config
from ..detection.detector import ObjectDetector, Detection
from ..detection.tracker import ObjectTracker

logger = logging.getLogger(__name__)


class VideoProcessor:
    """
    Video processor for handling webcam and video file input
    
    Manages video capture, frame processing, and coordinates
    detection and tracking operations.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the video processor"""
        self.config = config or Config()
        self.detector = ObjectDetector(self.config)
        self.tracker = ObjectTracker()
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.source_type: str = "none"  # "webcam", "video", "image", "none"
        self.source_path: Optional[str] = None
        
        self.frame_count: int = 0
        self.fps: float = 0.0
        self.last_frame_time: float = 0.0
        self.is_processing: bool = False
        
        self.current_frame: Optional[np.ndarray] = None
        self.current_detections: List[Detection] = []
        
        self.callbacks: Dict[str, List[Callable]] = {
            'on_frame': [],
            'on_detection': [],
            'on_error': []
        }
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register a callback for specific events
        
        Args:
            event: Event name ('on_frame', 'on_detection', 'on_error')
            callback: Callback function
        """
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, *args, **kwargs) -> None:
        """Trigger all callbacks for an event"""
        for callback in self.callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Callback error for {event}: {e}")
    
    def open_webcam(self, camera_index: Optional[int] = None) -> bool:
        """
        Open webcam for video capture
        
        Args:
            camera_index: Camera index (default from config)
        
        Returns:
            bool: True if webcam opened successfully
        """
        if self.cap is not None:
            self.close()
        
        camera_index = camera_index or self.config.WEBCAM_INDEX
        
        try:
            self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open webcam at index {camera_index}")
                self._trigger_callbacks('on_error', "Failed to open webcam")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.VIDEO_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.VIDEO_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, self.config.FPS_LIMIT)
            
            self.source_type = "webcam"
            self.source_path = f"webcam:{camera_index}"
            self.frame_count = 0
            self.is_processing = True
            
            logger.info(f"Webcam opened successfully at index {camera_index}")
            return True
            
        except Exception as e:
            logger.error(f"Error opening webcam: {e}")
            self._trigger_callbacks('on_error', f"Webcam error: {str(e)}")
            return False
    
    def open_video(self, video_path: str) -> bool:
        """
        Open video file for processing
        
        Args:
            video_path: Path to video file
        
        Returns:
            bool: True if video opened successfully
        """
        if self.cap is not None:
            self.close()
        
        video_path = Path(video_path)
        
        if not video_path.exists():
            logger.error(f"Video file not found: {video_path}")
            self._trigger_callbacks('on_error', f"Video file not found: {video_path}")
            return False
        
        if not self.config.is_video_file(str(video_path)):
            logger.error(f"Unsupported video format: {video_path.suffix}")
            self._trigger_callbacks('on_error', f"Unsupported video format: {video_path.suffix}")
            return False
        
        # Check file size
        file_size_mb = video_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.config.MAX_FILE_SIZE_MB:
            logger.error(f"Video file too large: {file_size_mb:.2f}MB")
            self._trigger_callbacks('on_error', f"Video file too large: {file_size_mb:.2f}MB")
            return False
        
        try:
            self.cap = cv2.VideoCapture(str(video_path))
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open video file: {video_path}")
                self._trigger_callbacks('on_error', f"Failed to open video file: {video_path}")
                return False
            
            self.source_type = "video"
            self.source_path = str(video_path)
            self.frame_count = 0
            self.is_processing = True
            
            # Get video properties
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Video opened: {video_path}")
            logger.info(f"Resolution: {width}x{height}, FPS: {self.fps:.2f}, Frames: {total_frames}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error opening video: {e}")
            self._trigger_callbacks('on_error', f"Video error: {str(e)}")
            return False
    
    def load_image(self, image_path: str) -> bool:
        """
        Load a single image for detection (no tracking)
        
        Args:
            image_path: Path to image file
        
        Returns:
            bool: True if image loaded successfully
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            logger.error(f"Image file not found: {image_path}")
            self._trigger_callbacks('on_error', f"Image file not found: {image_path}")
            return False
        
        if not self.config.is_image_file(str(image_path)):
            logger.error(f"Unsupported image format: {image_path.suffix}")
            self._trigger_callbacks('on_error', f"Unsupported image format: {image_path.suffix}")
            return False
        
        try:
            self.current_frame = cv2.imread(str(image_path))
            
            if self.current_frame is None:
                logger.error(f"Failed to load image: {image_path}")
                self._trigger_callbacks('on_error', f"Failed to load image: {image_path}")
                return False
            
            self.source_type = "image"
            self.source_path = str(image_path)
            self.frame_count = 0
            self.is_processing = False
            
            logger.info(f"Image loaded: {image_path}")
            logger.info(f"Resolution: {self.current_frame.shape[1]}x{self.current_frame.shape[0]}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            self._trigger_callbacks('on_error', f"Image error: {str(e)}")
            return False
    
    def read_frame(self) -> Optional[np.ndarray]:
        """
        Read a frame from the current source
        
        Returns:
            Frame as numpy array or None if no frame available
        """
        if self.cap is None or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        
        if not ret or frame is None:
            logger.info("End of video stream")
            return None
        
        self.current_frame = frame
        self.frame_count += 1
        
        # Calculate FPS
        current_time = time.time()
        if self.last_frame_time > 0:
            time_delta = current_time - self.last_frame_time
            if time_delta > 0:
                self.fps = 1.0 / time_delta
        self.last_frame_time = current_time
        
        self._trigger_callbacks('on_frame', frame, self.frame_count)
        
        return frame
    
    def process_frame(
        self,
        frame: Optional[np.ndarray] = None,
        enable_tracking: bool = True,
        **detection_kwargs
    ) -> Tuple[np.ndarray, List[Detection]]:
        """
        Process a frame with detection and tracking
        
        Args:
            frame: Input frame (uses current frame if None)
            enable_tracking: Whether to enable tracking
            **detection_kwargs: Additional arguments for detection
        
        Returns:
            Tuple of (processed_frame, detections)
        """
        if frame is None:
            frame = self.current_frame
        
        if frame is None:
            return np.array([]), []
        
        # Perform detection
        if enable_tracking and self.config.TRACKING_ENABLED:
            detections = self.detector.detect_with_tracking(frame, **detection_kwargs)
            # Update tracker
            self.tracker.update(detections, self.frame_count)
        else:
            detections = self.detector.detect(frame, **detection_kwargs)
        
        self.current_detections = detections
        
        self._trigger_callbacks('on_detection', detections, frame)
        
        return frame, detections
    
    def close(self) -> None:
        """Close video capture and release resources"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        self.source_type = "none"
        self.source_path = None
        self.is_processing = False
        self.tracker.reset()
        
        logger.info("Video processor closed")
    
    def is_opened(self) -> bool:
        """Check if video source is open"""
        return self.cap is not None and self.cap.isOpened()
    
    def get_video_info(self) -> Dict[str, Any]:
        """
        Get information about the current video source
        
        Returns:
            Dictionary with video information
        """
        info = {
            'source_type': self.source_type,
            'source_path': self.source_path,
            'is_opened': self.is_opened(),
            'frame_count': self.frame_count,
            'fps': self.fps,
            'is_processing': self.is_processing
        }
        
        if self.cap is not None and self.cap.isOpened():
            info['width'] = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            info['height'] = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            info['total_frames'] = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        elif self.current_frame is not None:
            info['width'] = self.current_frame.shape[1]
            info['height'] = self.current_frame.shape[0]
        
        return info
    
    def reset(self) -> None:
        """Reset processor state"""
        self.frame_count = 0
        self.fps = 0.0
        self.last_frame_time = 0.0
        self.current_detections = []
        self.tracker.reset()
        
        # Reset video position if video file
        if self.source_type == "video" and self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
