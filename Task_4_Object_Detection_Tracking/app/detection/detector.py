"""
Object Detection Module using YOLO (Ultralytics)
Implements object detection with pre-trained YOLO11n model
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
import logging

from ..config import Config

logger = logging.getLogger(__name__)


class Detection:
    """Represents a single object detection result"""
    
    def __init__(
        self,
        bbox: Tuple[int, int, int, int],  # x1, y1, x2, y2
        class_id: int,
        class_name: str,
        confidence: float,
        tracking_id: Optional[int] = None
    ):
        self.bbox = bbox  # (x1, y1, x2, y2)
        self.class_id = class_id
        self.class_name = class_name
        self.confidence = confidence
        self.tracking_id = tracking_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert detection to dictionary"""
        return {
            'bbox': self.bbox,
            'class_id': self.class_id,
            'class_name': self.class_name,
            'confidence': self.confidence,
            'tracking_id': self.tracking_id
        }
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get center point of bounding box"""
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)
    
    @property
    def area(self) -> int:
        """Get area of bounding box"""
        x1, y1, x2, y2 = self.bbox
        return (x2 - x1) * (y2 - y1)


class ObjectDetector:
    """
    Object detector using YOLO11n model via Ultralytics
    
    Model: YOLO11n (nano version of YOLO11)
    - Lightweight model suitable for CPU/GPU on student laptops
    - Trained on COCO dataset (80 common object classes)
    - Provides real-time performance with good accuracy
    - Model weights downloaded automatically on first run
    
    Detection classes include: person, bicycle, car, motorcycle, airplane, bus,
    train, truck, boat, traffic light, fire hydrant, stop sign, parking meter,
    bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe,
    backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard,
    sports ball, kite, baseball bat, baseball glove, skateboard, surfboard,
    tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana,
    apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake,
    chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse,
    remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator,
    book, clock, vase, scissors, teddy bear, hair drier, toothbrush
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the object detector"""
        self.config = config or Config()
        self.model = None
        self.device = self.config.get_device()
        self.class_names = []
        self._initialized = False
        
    def load_model(self) -> bool:
        """
        Load the YOLO model
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            from ultralytics import YOLO
            
            model_path = self.config.get_model_path()
            
            logger.info(f"Loading YOLO model: {self.config.MODEL_NAME}")
            logger.info(f"Device: {self.device}")
            
            # Load model (will download if not present)
            self.model = YOLO(self.config.MODEL_NAME)
            
            # Store class names
            self.class_names = self.model.names
            
            logger.info(f"Model loaded successfully. Classes: {len(self.class_names)}")
            logger.info(f"Model will be cached at: {model_path}")
            
            self._initialized = True
            return True
            
        except ImportError as e:
            logger.error(f"Ultralytics package not installed: {e}")
            raise ImportError(
                "Ultralytics package is required. "
                "Install it with: pip install ultralytics"
            )
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def detect(
        self,
        frame: np.ndarray,
        conf_threshold: Optional[float] = None,
        iou_threshold: Optional[float] = None,
        max_detections: Optional[int] = None,
        filter_classes: Optional[List[str]] = None
    ) -> List[Detection]:
        """
        Perform object detection on a frame
        
        Args:
            frame: Input image as numpy array (BGR format from OpenCV)
            conf_threshold: Confidence threshold (default from config)
            iou_threshold: IoU threshold for NMS (default from config)
            max_detections: Maximum number of detections (default from config)
            filter_classes: List of class names to filter (default from config)
        
        Returns:
            List of Detection objects
        """
        if not self._initialized:
            if not self.load_model():
                return []
        
        # Use config defaults if not specified
        conf_threshold = conf_threshold or self.config.CONFIDENCE_THRESHOLD
        iou_threshold = iou_threshold or self.config.IOU_THRESHOLD
        max_detections = max_detections or self.config.MAX_DETECTIONS
        filter_classes = filter_classes or self.config.FILTER_CLASSES
        
        try:
            # Run inference
            results = self.model(
                frame,
                conf=conf_threshold,
                iou=iou_threshold,
                max_det=max_detections,
                verbose=False,
                device=self.device
            )
            
            detections = []
            
            # Process results
            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue
                
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    bbox = (int(x1), int(y1), int(x2), int(y2))
                    
                    # Get class information
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.class_names[class_id]
                    
                    # Get confidence
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    # Apply class filtering if specified
                    if filter_classes and class_name not in filter_classes:
                        continue
                    
                    # Create detection object
                    detection = Detection(
                        bbox=bbox,
                        class_id=class_id,
                        class_name=class_name,
                        confidence=confidence
                    )
                    
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []
    
    def detect_with_tracking(
        self,
        frame: np.ndarray,
        persist: bool = True,
        **kwargs
    ) -> List[Detection]:
        """
        Perform object detection with tracking
        
        Args:
            frame: Input image as numpy array
            persist: Whether to persist tracking across frames
            **kwargs: Additional arguments for detect()
        
        Returns:
            List of Detection objects with tracking IDs
        """
        if not self._initialized:
            if not self.load_model():
                return []
        
        try:
            # Run inference with tracking
            results = self.model.track(
                frame,
                persist=persist,
                conf=kwargs.get('conf_threshold', self.config.CONFIDENCE_THRESHOLD),
                iou=kwargs.get('iou_threshold', self.config.IOU_THRESHOLD),
                max_det=kwargs.get('max_detections', self.config.MAX_DETECTIONS),
                verbose=False,
                device=self.device,
                tracker=self.config.TRACKER_TYPE
            )
            
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue
                
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    bbox = (int(x1), int(y1), int(x2), int(y2))
                    
                    # Get class information
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.class_names[class_id]
                    
                    # Get confidence
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    # Get tracking ID if available
                    tracking_id = None
                    if box.id is not None:
                        tracking_id = int(box.id[0].cpu().numpy())
                    
                    # Apply class filtering if specified
                    filter_classes = kwargs.get('filter_classes', self.config.FILTER_CLASSES)
                    if filter_classes and class_name not in filter_classes:
                        continue
                    
                    detection = Detection(
                        bbox=bbox,
                        class_id=class_id,
                        class_name=class_name,
                        confidence=confidence,
                        tracking_id=tracking_id
                    )
                    
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection with tracking error: {e}")
            return []
    
    def get_class_names(self) -> List[str]:
        """Get list of all class names the model can detect"""
        if not self._initialized:
            self.load_model()
        return self.class_names
    
    def is_initialized(self) -> bool:
        """Check if model is loaded and ready"""
        return self._initialized
    
    def reset_tracking(self) -> None:
        """Reset tracking state"""
        if self.model and hasattr(self.model, 'predictor'):
            # Reset tracking by clearing any internal state
            try:
                self.model.predictor.reset_tracking()
            except:
                pass
