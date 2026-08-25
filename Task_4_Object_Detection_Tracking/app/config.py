"""
Configuration module for Object Detection and Tracking application
"""

import os
from pathlib import Path
from typing import List, Optional


class Config:
    """Application configuration settings"""
    
    # Model settings
    MODEL_NAME: str = "yolo11n.pt"  # YOLO11 nano model
    CONFIDENCE_THRESHOLD: float = 0.25
    IOU_THRESHOLD: float = 0.45
    MAX_DETECTIONS: int = 300
    
    # Device settings
    DEVICE: str = "auto"  # Options: "auto", "cpu", "cuda", "mps"
    
    # Tracking settings
    TRACKING_ENABLED: bool = True
    TRACKER_TYPE: str = "bytetrack"  # Options: "bytetrack", "botsort"
    
    # Video settings
    WEBCAM_INDEX: int = 0
    VIDEO_WIDTH: int = 1280
    VIDEO_HEIGHT: int = 720
    FPS_LIMIT: int = 30
    
    # UI settings
    DISPLAY_FPS: bool = True
    DISPLAY_STATISTICS: bool = True
    SHOW_TRACKING_ID: bool = True
    SHOW_CONFIDENCE: bool = True
    
    # Filtering
    FILTER_CLASSES: Optional[List[str]] = None  # None = detect all classes
    
    # File paths
    BASE_DIR: Path = Path(__file__).parent.parent
    MODEL_DIR: Path = BASE_DIR / "models"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    # Supported video formats
    SUPPORTED_VIDEO_FORMATS: List[str] = [".mp4", ".avi", ".mov", ".mkv", ".wmv"]
    SUPPORTED_IMAGE_FORMATS: List[str] = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    
    # Security
    MAX_FILE_SIZE_MB: int = 500
    
    @classmethod
    def setup_directories(cls) -> None:
        """Create necessary directories if they don't exist"""
        cls.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_model_path(cls) -> Path:
        """Get the full path to the model file"""
        return cls.MODEL_DIR / cls.MODEL_NAME
    
    @classmethod
    def get_device(cls) -> str:
        """Determine the best available device"""
        if cls.DEVICE != "auto":
            return cls.DEVICE
        
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
        except ImportError:
            pass
        
        return "cpu"
    
    @classmethod
    def is_video_file(cls, filepath: str) -> bool:
        """Check if file is a supported video format"""
        return Path(filepath).suffix.lower() in cls.SUPPORTED_VIDEO_FORMATS
    
    @classmethod
    def is_image_file(cls, filepath: str) -> bool:
        """Check if file is a supported image format"""
        return Path(filepath).suffix.lower() in cls.SUPPORTED_IMAGE_FORMATS


# Initialize directories on import
Config.setup_directories()
