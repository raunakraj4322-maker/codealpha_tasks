"""
Desktop UI using OpenCV
Provides a professional interface for object detection and tracking
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

from ..detection.detector import Detection
from ..services.statistics import StatisticsManager
from ..config import Config

logger = logging.getLogger(__name__)


class DesktopUI:
    """
    Desktop UI using OpenCV for visualization and control
    
    Provides a professional interface with:
    - Live detection display
    - Bounding boxes with labels
    - Tracking IDs
    - Confidence scores
    - Statistics overlay
    - Interactive controls
    """
    
    # Color scheme for different classes (consistent colors per class)
    CLASS_COLORS = {
        'person': (0, 255, 0),           # Green
        'bicycle': (255, 0, 0),          # Blue
        'car': (0, 0, 255),              # Red
        'motorcycle': (255, 255, 0),     # Cyan
        'airplane': (255, 0, 255),       # Magenta
        'bus': (0, 255, 255),            # Yellow
        'train': (128, 0, 128),          # Purple
        'truck': (255, 165, 0),          # Orange
        'boat': (0, 128, 128),           # Teal
        'dog': (255, 192, 203),          # Pink
        'cat': (255, 105, 180),          # Hot Pink
    }
    
    DEFAULT_COLOR = (0, 255, 255)  # Yellow for unmapped classes
    
    def __init__(self, app):
        """
        Initialize the desktop UI
        
        Args:
            app: ObjectDetectionApp instance
        """
        self.app = app
        self.config = app.config
        self.window_name = "Object Detection & Tracking - CodeAlpha Task 4"
        
        # UI state
        self.show_labels = True
        self.show_confidence = True
        self.show_tracking_id = True
        self.show_statistics = True
        self.paused = False
        
        # Font settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.6
        self.font_thickness = 2
        self.box_thickness = 2
        
        logger.info("Desktop UI initialized")
    
    def get_class_color(self, class_name: str) -> Tuple[int, int, int]:
        """
        Get color for a class (consistent per class)
        
        Args:
            class_name: Name of the class
        
        Returns:
            RGB color tuple
        """
        if class_name in self.CLASS_COLORS:
            return self.CLASS_COLORS[class_name]
        
        # Generate consistent color based on class name hash
        hash_value = hash(class_name) % 16777215
        return (
            (hash_value >> 16) & 255,
            (hash_value >> 8) & 255,
            hash_value & 255
        )
    
    def draw_detection(
        self,
        frame: np.ndarray,
        detection: Detection
    ) -> np.ndarray:
        """
        Draw a single detection on the frame
        
        Args:
            frame: Input frame
            detection: Detection object
        
        Returns:
            Frame with detection drawn
        """
        x1, y1, x2, y2 = detection.bbox
        color = self.get_class_color(detection.class_name)
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, self.box_thickness)
        
        # Create label text
        label_parts = []
        
        if self.show_labels:
            label_parts.append(detection.class_name)
        
        if self.show_tracking_id and detection.tracking_id is not None:
            label_parts.append(f"ID:{detection.tracking_id}")
        
        if self.show_confidence:
            label_parts.append(f"{detection.confidence:.2f}")
        
        label_text = " | ".join(label_parts)
        
        # Draw label background
        if label_text:
            (label_width, label_height), baseline = cv2.getTextSize(
                label_text, self.font, self.font_scale, self.font_thickness
            )
            
            # Ensure label doesn't go outside frame
            y1_label = max(y1 - label_height - baseline - 5, 0)
            y2_label = y1_label + label_height + baseline + 5
            x2_label = min(x1 + label_width + 10, frame.shape[1])
            
            cv2.rectangle(
                frame,
                (x1, y1_label),
                (x2_label, y2_label),
                color,
                -1  # Filled
            )
            
            # Draw label text
            cv2.putText(
                frame,
                label_text,
                (x1 + 5, y1_label + label_height + baseline - 2),
                self.font,
                self.font_scale,
                (0, 0, 0),  # Black text
                self.font_thickness
            )
        
        return frame
    
    def draw_statistics(
        self,
        frame: np.ndarray,
        statistics: StatisticsManager,
        video_info: Dict
    ) -> np.ndarray:
        """
        Draw statistics overlay on the frame
        
        Args:
            frame: Input frame
            statistics: Statistics manager
            video_info: Video information dictionary
        
        Returns:
            Frame with statistics overlay
        """
        if not self.show_statistics:
            return frame
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        height, width = frame.shape[:2]
        
        # Statistics panel dimensions
        panel_width = 350
        panel_height = 200
        panel_x = 10
        panel_y = 10
        
        # Draw semi-transparent background
        cv2.rectangle(
            overlay,
            (panel_x, panel_y),
            (panel_x + panel_width, panel_y + panel_height),
            (0, 0, 0),
            -1
        )
        
        # Blend overlay
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Get statistics
        current_fps = statistics.get_current_fps()
        avg_fps = statistics.get_average_fps()
        current_detections = statistics.get_current_detection_count()
        current_trackers = statistics.get_current_tracking_count()
        class_dist = statistics.get_class_distribution()
        
        # Draw statistics text
        y_offset = 30
        line_height = 25
        
        # FPS
        cv2.putText(
            frame,
            f"FPS: {current_fps:.1f} (Avg: {avg_fps:.1f})",
            (panel_x + 10, panel_y + y_offset),
            self.font,
            self.font_scale,
            (0, 255, 0),
            self.font_thickness
        )
        y_offset += line_height
        
        # Objects
        cv2.putText(
            frame,
            f"Objects: {current_detections}",
            (panel_x + 10, panel_y + y_offset),
            self.font,
            self.font_scale,
            (0, 255, 255),
            self.font_thickness
        )
        y_offset += line_height
        
        # Trackers
        if self.config.TRACKING_ENABLED:
            cv2.putText(
                frame,
                f"Trackers: {current_trackers}",
                (panel_x + 10, panel_y + y_offset),
                self.font,
                self.font_scale,
                (255, 0, 255),
                self.font_thickness
            )
            y_offset += line_height
        
        # Source
        source_text = f"Source: {video_info.get('source_type', 'unknown')}"
        cv2.putText(
            frame,
            source_text,
            (panel_x + 10, panel_y + y_offset),
            self.font,
            self.font_scale,
            (255, 255, 255),
            self.font_thickness
        )
        y_offset += line_height
        
        # Resolution
        if 'width' in video_info and 'height' in video_info:
            res_text = f"Res: {video_info['width']}x{video_info['height']}"
            cv2.putText(
                frame,
                res_text,
                (panel_x + 10, panel_y + y_offset),
                self.font,
                self.font_scale,
                (255, 255, 255),
                self.font_thickness
            )
            y_offset += line_height
        
        # Class distribution (top 3)
        if class_dist:
            top_classes = sorted(class_dist.items(), key=lambda x: x[1], reverse=True)[:3]
            for class_name, count in top_classes:
                class_text = f"{class_name}: {count}"
                cv2.putText(
                    frame,
                    class_text,
                    (panel_x + 10, panel_y + y_offset),
                    self.font,
                    self.font_scale,
                    (200, 200, 200),
                    self.font_thickness
                )
                y_offset += line_height
        
        return frame
    
    def draw_controls_help(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw controls help on the frame
        
        Args:
            frame: Input frame
        
        Returns:
            Frame with controls help
        """
        height, width = frame.shape[:2]
        
        # Controls text
        controls = [
            "Controls:",
            "SPACE - Pause/Resume",
            "Q - Quit",
            "S - Toggle statistics",
            "L - Toggle labels",
            "C - Toggle confidence",
            "T - Toggle tracking ID"
        ]
        
        y_offset = height - 10
        line_height = 20
        
        for control in reversed(controls):
            cv2.putText(
                frame,
                control,
                (10, y_offset),
                self.font,
                0.5,
                (255, 255, 255),
                1
            )
            y_offset -= line_height
        
        return frame
    
    def process_key(self, key: int) -> bool:
        """
        Process keyboard input
        
        Args:
            key: Key code from cv2.waitKey
        
        Returns:
            True to continue, False to quit
        """
        if key == ord('q') or key == ord('Q'):
            return False
        elif key == ord(' '):  # Space
            self.paused = not self.paused
            logger.info(f"Paused: {self.paused}")
        elif key == ord('s') or key == ord('S'):
            self.show_statistics = not self.show_statistics
            logger.info(f"Statistics: {self.show_statistics}")
        elif key == ord('l') or key == ord('L'):
            self.show_labels = not self.show_labels
            logger.info(f"Labels: {self.show_labels}")
        elif key == ord('c') or key == ord('C'):
            self.show_confidence = not self.show_confidence
            logger.info(f"Confidence: {self.show_confidence}")
        elif key == ord('t') or key == ord('T'):
            self.show_tracking_id = not self.show_tracking_id
            logger.info(f"Tracking ID: {self.show_tracking_id}")
        
        return True
    
    def run_webcam(self, camera_index: Optional[int] = None) -> None:
        """
        Run application with webcam input
        
        Args:
            camera_index: Camera index to use
        """
        logger.info("Starting webcam mode")
        
        # Open webcam
        if not self.app.video_processor.open_webcam(camera_index):
            logger.error("Failed to open webcam")
            return
        
        # Start statistics
        self.app.statistics.start_session()
        
        # Create window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 1280, 720)
        
        logger.info("Webcam mode started. Press 'Q' to quit.")
        
        try:
            while True:
                if not self.paused:
                    # Read frame
                    frame = self.app.video_processor.read_frame()
                    
                    if frame is None:
                        logger.error("Failed to read frame from webcam")
                        break
                    
                    # Process frame
                    processed_frame, detections = self.app.video_processor.process_frame(
                        frame,
                        enable_tracking=self.config.TRACKING_ENABLED
                    )
                    
                    # Update statistics
                    self.app.statistics.update_frame(detections, self.app.tracker)
                    
                    # Draw detections
                    for detection in detections:
                        processed_frame = self.draw_detection(processed_frame, detection)
                    
                    # Draw statistics
                    video_info = self.app.video_processor.get_video_info()
                    processed_frame = self.draw_statistics(
                        processed_frame,
                        self.app.statistics,
                        video_info
                    )
                    
                    # Draw controls help
                    processed_frame = self.draw_controls_help(processed_frame)
                    
                    # Display frame
                    cv2.imshow(self.window_name, processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if not self.process_key(key):
                    break
        
        except Exception as e:
            logger.error(f"Error in webcam mode: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            cv2.destroyAllWindows()
            self.app.video_processor.close()
            logger.info("Webcam mode ended")
    
    def run_video(self, video_path: str) -> None:
        """
        Run application with video file input
        
        Args:
            video_path: Path to video file
        """
        logger.info(f"Starting video mode: {video_path}")
        
        # Open video
        if not self.app.video_processor.open_video(video_path):
            logger.error("Failed to open video")
            return
        
        # Start statistics
        self.app.statistics.start_session()
        
        # Create window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 1280, 720)
        
        logger.info("Video mode started. Press 'Q' to quit.")
        
        try:
            while True:
                if not self.paused:
                    # Read frame
                    frame = self.app.video_processor.read_frame()
                    
                    if frame is None:
                        logger.info("Video ended")
                        break
                    
                    # Process frame
                    processed_frame, detections = self.app.video_processor.process_frame(
                        frame,
                        enable_tracking=self.config.TRACKING_ENABLED
                    )
                    
                    # Update statistics
                    self.app.statistics.update_frame(detections, self.app.tracker)
                    
                    # Draw detections
                    for detection in detections:
                        processed_frame = self.draw_detection(processed_frame, detection)
                    
                    # Draw statistics
                    video_info = self.app.video_processor.get_video_info()
                    processed_frame = self.draw_statistics(
                        processed_frame,
                        self.app.statistics,
                        video_info
                    )
                    
                    # Draw controls help
                    processed_frame = self.draw_controls_help(processed_frame)
                    
                    # Display frame
                    cv2.imshow(self.window_name, processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if not self.process_key(key):
                    break
        
        except Exception as e:
            logger.error(f"Error in video mode: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            cv2.destroyAllWindows()
            self.app.video_processor.close()
            logger.info("Video mode ended")
    
    def run_image(self, image_path: str) -> None:
        """
        Run application with single image input
        
        Args:
            image_path: Path to image file
        """
        logger.info(f"Starting image mode: {image_path}")
        
        # Load image
        if not self.app.video_processor.load_image(image_path):
            logger.error("Failed to load image")
            return
        
        # Start statistics
        self.app.statistics.start_session()
        
        # Create window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        try:
            # Get frame
            frame = self.app.video_processor.current_frame
            
            if frame is None:
                logger.error("No frame loaded")
                return
            
            # Process frame (no tracking for single image)
            processed_frame, detections = self.app.video_processor.process_frame(
                frame,
                enable_tracking=False
            )
            
            # Update statistics
            self.app.statistics.update_frame(detections, self.app.tracker)
            
            # Draw detections
            for detection in detections:
                processed_frame = self.draw_detection(processed_frame, detection)
            
            # Draw statistics
            video_info = self.app.video_processor.get_video_info()
            processed_frame = self.draw_statistics(
                processed_frame,
                self.app.statistics,
                video_info
            )
            
            # Resize if too large
            height, width = processed_frame.shape[:2]
            if width > 1920 or height > 1080:
                scale = min(1920 / width, 1080 / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                processed_frame = cv2.resize(
                    processed_frame,
                    (new_width, new_height)
                )
            
            # Display frame
            cv2.imshow(self.window_name, processed_frame)
            
            logger.info(f"Detected {len(detections)} objects")
            logger.info("Press any key to exit...")
            
            # Wait for key
            cv2.waitKey(0)
        
        except Exception as e:
            logger.error(f"Error in image mode: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            cv2.destroyAllWindows()
            self.app.video_processor.close()
            logger.info("Image mode ended")
