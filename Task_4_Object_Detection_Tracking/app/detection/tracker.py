"""
Object Tracking Module
Provides tracking management and utilities for object tracking
"""

from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import logging

from .detector import Detection

logger = logging.getLogger(__name__)


class ObjectTracker:
    """
    Object tracking manager
    
    This class provides tracking management utilities on top of the
    built-in YOLO tracking functionality. It maintains tracking history
    and provides utilities for tracking analysis.
    
    Note: The actual tracking algorithm (ByteTrack) is implemented
    within the Ultralytics YOLO library and used via the detector's
    detect_with_tracking method. This class provides additional
    tracking management and analysis capabilities.
    """
    
    def __init__(self):
        """Initialize the object tracker"""
        self.tracking_history: Dict[int, List[Detection]] = defaultdict(list)
        self.active_trackers: Dict[int, Detection] = {}
        self.next_id: int = 1
        self.frame_count: int = 0
    
    def update(
        self,
        detections: List[Detection],
        frame_number: int
    ) -> List[Detection]:
        """
        Update tracking with new detections
        
        Args:
            detections: List of detections with tracking IDs
            frame_number: Current frame number
        
        Returns:
            Updated list of detections
        """
        self.frame_count = frame_number
        
        # Clear active trackers for this frame
        self.active_trackers.clear()
        
        # Update tracking history
        for detection in detections:
            if detection.tracking_id is not None:
                # Add to tracking history
                self.tracking_history[detection.tracking_id].append(detection)
                # Add to active trackers
                self.active_trackers[detection.tracking_id] = detection
        
        return detections
    
    def get_tracking_history(self, tracking_id: int) -> List[Detection]:
        """
        Get the tracking history for a specific tracking ID
        
        Args:
            tracking_id: The tracking ID to get history for
        
        Returns:
            List of detections for this tracking ID
        """
        return self.tracking_history.get(tracking_id, [])
    
    def get_active_trackers(self) -> Dict[int, Detection]:
        """
        Get currently active trackers
        
        Returns:
            Dictionary of tracking_id -> Detection
        """
        return self.active_trackers.copy()
    
    def get_active_tracking_ids(self) -> List[int]:
        """
        Get list of currently active tracking IDs
        
        Returns:
            List of active tracking IDs
        """
        return list(self.active_trackers.keys())
    
    def get_tracker_count(self) -> int:
        """
        Get the number of currently active trackers
        
        Returns:
            Number of active trackers
        """
        return len(self.active_trackers)
    
    def get_class_distribution(self) -> Dict[str, int]:
        """
        Get the distribution of object classes among active trackers
        
        Returns:
            Dictionary of class_name -> count
        """
        distribution = defaultdict(int)
        for detection in self.active_trackers.values():
            distribution[detection.class_name] += 1
        return dict(distribution)
    
    def get_tracker_class(self, tracking_id: int) -> Optional[str]:
        """
        Get the class name for a specific tracking ID
        
        Args:
            tracking_id: The tracking ID to query
        
        Returns:
            Class name if tracker exists, None otherwise
        """
        if tracking_id in self.active_trackers:
            return self.active_trackers[tracking_id].class_name
        return None
    
    def remove_inactive_trackers(self, max_age: int = 30) -> int:
        """
        Remove trackers that haven't been seen recently
        
        Args:
            max_age: Maximum number of frames a tracker can be inactive
        
        Returns:
            Number of trackers removed
        """
        removed_count = 0
        inactive_ids = []
        
        for tracking_id, history in self.tracking_history.items():
            if tracking_id not in self.active_trackers:
                # Check how many frames since last detection
                if len(history) > 0:
                    last_frame = history[-1]
                    # If we haven't seen this tracker in max_age frames, remove it
                    if (self.frame_count - len(history)) > max_age:
                        inactive_ids.append(tracking_id)
        
        for tracking_id in inactive_ids:
            del self.tracking_history[tracking_id]
            removed_count += 1
        
        return removed_count
    
    def reset(self) -> None:
        """Reset all tracking state"""
        self.tracking_history.clear()
        self.active_trackers.clear()
        self.frame_count = 0
        logger.info("Tracking state reset")
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get tracking statistics
        
        Returns:
            Dictionary containing tracking statistics
        """
        return {
            'frame_count': self.frame_count,
            'active_trackers': len(self.active_trackers),
            'total_unique_trackers': len(self.tracking_history),
            'class_distribution': self.get_class_distribution(),
            'active_tracking_ids': self.get_active_tracking_ids()
        }
    
    def calculate_displacement(
        self,
        tracking_id: int,
        frames_back: int = 1
    ) -> Optional[Tuple[float, float]]:
        """
        Calculate the displacement of a tracker over the last N frames
        
        Args:
            tracking_id: The tracking ID to calculate displacement for
            frames_back: Number of frames to look back
        
        Returns:
            Tuple of (dx, dy) displacement or None if not enough data
        """
        history = self.get_tracking_history(tracking_id)
        if len(history) < frames_back + 1:
            return None
        
        current = history[-1]
        previous = history[-(frames_back + 1)]
        
        current_center = current.center
        previous_center = previous.center
        
        dx = current_center[0] - previous_center[0]
        dy = current_center[1] - previous_center[1]
        
        return (dx, dy)
    
    def calculate_velocity(
        self,
        tracking_id: int,
        frames_back: int = 1,
        fps: float = 30.0
    ) -> Optional[Tuple[float, float]]:
        """
        Calculate the velocity of a tracker (pixels per second)
        
        Args:
            tracking_id: The tracking ID to calculate velocity for
            frames_back: Number of frames to look back
            fps: Frames per second of the video
        
        Returns:
            Tuple of (vx, vy) velocity or None if not enough data
        """
        displacement = self.calculate_displacement(tracking_id, frames_back)
        if displacement is None:
            return None
        
        time_delta = frames_back / fps
        vx = displacement[0] / time_delta
        vy = displacement[1] / time_delta
        
        return (vx, vy)
