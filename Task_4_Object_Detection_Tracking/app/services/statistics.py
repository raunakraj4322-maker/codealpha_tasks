"""
Statistics Manager Service
Tracks and manages real-time statistics for detection and tracking
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import time
import logging

from ..detection.detector import Detection
from ..detection.tracker import ObjectTracker

logger = logging.getLogger(__name__)


class StatisticsManager:
    """
    Statistics manager for real-time detection and tracking metrics
    
    Tracks FPS, object counts, class distributions, and other
    performance metrics over time.
    """
    
    def __init__(self, history_size: int = 30):
        """
        Initialize statistics manager
        
        Args:
            history_size: Number of frames to keep in history for averaging
        """
        self.history_size = history_size
        
        # FPS tracking
        self.fps_history: deque = deque(maxlen=history_size)
        self.frame_times: deque = deque(maxlen=history_size)
        self.last_frame_time: Optional[float] = None
        
        # Detection statistics
        self.detection_count_history: deque = deque(maxlen=history_size)
        self.class_count_history: deque = deque(maxlen=history_size)
        
        # Tracking statistics
        self.tracking_count_history: deque = deque(maxlen=history_size)
        self.unique_trackers_total: int = 0
        
        # Error tracking
        self.error_count: int = 0
        self.last_error: Optional[str] = None
        
        # Performance metrics
        self.total_frames_processed: int = 0
        self.total_detections: int = 0
        self.start_time: Optional[float] = None
    
    def start_session(self) -> None:
        """Start a new statistics session"""
        self.start_time = time.time()
        self.fps_history.clear()
        self.frame_times.clear()
        self.detection_count_history.clear()
        self.class_count_history.clear()
        self.tracking_count_history.clear()
        self.unique_trackers_total = 0
        self.error_count = 0
        self.last_error = None
        self.total_frames_processed = 0
        self.total_detections = 0
        self.last_frame_time = None
        
        logger.info("Statistics session started")
    
    def update_frame(self, detections: List[Detection], tracker: ObjectTracker) -> None:
        """
        Update statistics with new frame data
        
        Args:
            detections: List of detections for current frame
            tracker: Object tracker instance
        """
        current_time = time.time()
        
        # Calculate frame time
        if self.last_frame_time is not None:
            frame_time = current_time - self.last_frame_time
            self.frame_times.append(frame_time)
            
            # Calculate FPS
            if frame_time > 0:
                fps = 1.0 / frame_time
                self.fps_history.append(fps)
        
        self.last_frame_time = current_time
        
        # Update detection statistics
        detection_count = len(detections)
        self.detection_count_history.append(detection_count)
        self.total_detections += detection_count
        
        # Update class distribution
        class_counts = defaultdict(int)
        for detection in detections:
            class_counts[detection.class_name] += 1
        self.class_count_history.append(dict(class_counts))
        
        # Update tracking statistics
        tracking_count = tracker.get_tracker_count()
        self.tracking_count_history.append(tracking_count)
        self.unique_trackers_total = len(tracker.tracking_history)
        
        # Update frame count
        self.total_frames_processed += 1
    
    def record_error(self, error_message: str) -> None:
        """
        Record an error occurrence
        
        Args:
            error_message: Error message
        """
        self.error_count += 1
        self.last_error = error_message
        logger.warning(f"Error recorded: {error_message}")
    
    def get_current_fps(self) -> float:
        """
        Get current FPS (average over history)
        
        Returns:
            Current FPS or 0 if no data
        """
        if len(self.fps_history) == 0:
            return 0.0
        return sum(self.fps_history) / len(self.fps_history)
    
    def get_average_fps(self) -> float:
        """
        Get average FPS over the entire session
        
        Returns:
            Average FPS or 0 if no data
        """
        if self.start_time is None or self.total_frames_processed == 0:
            return 0.0
        
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0.0
        
        return self.total_frames_processed / elapsed_time
    
    def get_current_detection_count(self) -> int:
        """
        Get current number of detections
        
        Returns:
            Current detection count or 0 if no data
        """
        if len(self.detection_count_history) == 0:
            return 0
        return self.detection_count_history[-1]
    
    def get_average_detection_count(self) -> float:
        """
        Get average number of detections per frame
        
        Returns:
            Average detection count or 0 if no data
        """
        if len(self.detection_count_history) == 0:
            return 0.0
        return sum(self.detection_count_history) / len(self.detection_count_history)
    
    def get_current_tracking_count(self) -> int:
        """
        Get current number of active trackers
        
        Returns:
            Current tracking count or 0 if no data
        """
        if len(self.tracking_count_history) == 0:
            return 0
        return self.tracking_count_history[-1]
    
    def get_class_distribution(self) -> Dict[str, int]:
        """
        Get current class distribution
        
        Returns:
            Dictionary of class_name -> count
        """
        if len(self.class_count_history) == 0:
            return {}
        return self.class_count_history[-1].copy()
    
    def get_average_class_distribution(self) -> Dict[str, float]:
        """
        Get average class distribution over history
        
        Returns:
            Dictionary of class_name -> average count
        """
        if len(self.class_count_history) == 0:
            return {}
        
        class_sums = defaultdict(float)
        for class_counts in self.class_count_history:
            for class_name, count in class_counts.items():
                class_sums[class_name] += count
        
        history_length = len(self.class_count_history)
        return {
            class_name: total / history_length
            for class_name, total in class_sums.items()
        }
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the current session
        
        Returns:
            Dictionary containing all statistics
        """
        elapsed_time = 0.0
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
        
        return {
            'session_info': {
                'start_time': self.start_time,
                'elapsed_time_seconds': elapsed_time,
                'total_frames_processed': self.total_frames_processed,
                'total_detections': self.total_detections,
                'error_count': self.error_count,
                'last_error': self.last_error
            },
            'performance': {
                'current_fps': self.get_current_fps(),
                'average_fps': self.get_average_fps(),
                'average_frame_time': (
                    sum(self.frame_times) / len(self.frame_times)
                    if len(self.frame_times) > 0 else 0.0
                )
            },
            'detection_stats': {
                'current_detections': self.get_current_detection_count(),
                'average_detections': self.get_average_detection_count(),
                'class_distribution': self.get_class_distribution(),
                'average_class_distribution': self.get_average_class_distribution()
            },
            'tracking_stats': {
                'current_trackers': self.get_current_tracking_count(),
                'unique_trackers_total': self.unique_trackers_total
            }
        }
    
    def get_display_string(self) -> str:
        """
        Get a formatted string for displaying statistics in UI
        
        Returns:
            Formatted statistics string
        """
        current_fps = self.get_current_fps()
        avg_fps = self.get_average_fps()
        current_detections = self.get_current_detection_count()
        current_trackers = self.get_current_tracking_count()
        class_dist = self.get_class_distribution()
        
        lines = [
            f"FPS: {current_fps:.1f} (Avg: {avg_fps:.1f})",
            f"Objects: {current_detections}",
            f"Trackers: {current_trackers}",
            f"Frames: {self.total_frames_processed}"
        ]
        
        # Add top classes
        if class_dist:
            top_classes = sorted(class_dist.items(), key=lambda x: x[1], reverse=True)[:3]
            class_lines = [f"{cls}: {count}" for cls, count in top_classes]
            lines.append("Top: " + ", ".join(class_lines))
        
        return " | ".join(lines)
    
    def reset(self) -> None:
        """Reset all statistics"""
        self.start_session()
        logger.info("Statistics reset")
