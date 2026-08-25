"""
Main Application Entry Point
Object Detection and Tracking Application
CodeAlpha AI Internship Task 4
"""

import sys
import logging
from pathlib import Path

from .config import Config
from .detection.detector import ObjectDetector
from .detection.tracker import ObjectTracker
from .services.video_processor import VideoProcessor
from .services.statistics import StatisticsManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class ObjectDetectionApp:
    """
    Main application class for Object Detection and Tracking
    
    Coordinates all components and provides the main application logic.
    """
    
    def __init__(self, config: Config = None):
        """Initialize the application"""
        self.config = config or Config()
        self.detector = ObjectDetector(self.config)
        self.tracker = ObjectTracker()
        self.video_processor = VideoProcessor(self.config)
        self.statistics = StatisticsManager()
        
        self.is_running = False
        
        logger.info("Object Detection Application initialized")
        logger.info(f"Model: {self.config.MODEL_NAME}")
        logger.info(f"Device: {self.config.get_device()}")
    
    def initialize(self) -> bool:
        """
        Initialize the application components
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Load detection model
            logger.info("Loading detection model...")
            if not self.detector.load_model():
                logger.error("Failed to load detection model")
                return False
            
            logger.info("Model loaded successfully")
            logger.info(f"Available classes: {len(self.detector.get_class_names())}")
            
            return True
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            return False
    
    def run_webcam(self, camera_index: int = None) -> None:
        """
        Run application with webcam input
        
        Args:
            camera_index: Camera index to use
        """
        logger.info(f"Starting webcam mode with camera index: {camera_index or self.config.WEBCAM_INDEX}")
        
        # Import UI here to avoid circular imports
        from .ui.desktop_ui import DesktopUI
        
        ui = DesktopUI(self)
        ui.run_webcam(camera_index)
    
    def run_video(self, video_path: str) -> None:
        """
        Run application with video file input
        
        Args:
            video_path: Path to video file
        """
        logger.info(f"Starting video mode with file: {video_path}")
        
        from .ui.desktop_ui import DesktopUI
        
        ui = DesktopUI(self)
        ui.run_video(video_path)
    
    def run_image(self, image_path: str) -> None:
        """
        Run application with single image input
        
        Args:
            image_path: Path to image file
        """
        logger.info(f"Starting image mode with file: {image_path}")
        
        from .ui.desktop_ui import DesktopUI
        
        ui = DesktopUI(self)
        ui.run_image(image_path)
    
    def shutdown(self) -> None:
        """Shutdown the application and release resources"""
        logger.info("Shutting down application...")
        
        self.video_processor.close()
        self.tracker.reset()
        self.statistics.reset()
        
        self.is_running = False
        logger.info("Application shutdown complete")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Object Detection and Tracking Application - CodeAlpha Task 4"
    )
    
    parser.add_argument(
        '--webcam',
        type=int,
        nargs='?',
        const=0,
        help='Use webcam (optional camera index)'
    )
    
    parser.add_argument(
        '--video',
        type=str,
        help='Path to video file'
    )
    
    parser.add_argument(
        '--image',
        type=str,
        help='Path to image file'
    )
    
    parser.add_argument(
        '--confidence',
        type=float,
        default=None,
        help='Confidence threshold (default: 0.25)'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        choices=['auto', 'cpu', 'cuda', 'mps'],
        default=None,
        help='Device to use for inference'
    )
    
    parser.add_argument(
        '--no-tracking',
        action='store_true',
        help='Disable object tracking'
    )
    
    args = parser.parse_args()
    
    # Create and initialize application
    app = ObjectDetectionApp()
    
    # Apply command line overrides
    if args.confidence is not None:
        app.config.CONFIDENCE_THRESHOLD = args.confidence
        logger.info(f"Confidence threshold set to: {args.confidence}")
    
    if args.device is not None:
        app.config.DEVICE = args.device
        logger.info(f"Device set to: {args.device}")
    
    if args.no_tracking:
        app.config.TRACKING_ENABLED = False
        logger.info("Tracking disabled")
    
    # Initialize
    if not app.initialize():
        logger.error("Failed to initialize application")
        sys.exit(1)
    
    # Run appropriate mode
    try:
        if args.webcam is not None:
            app.run_webcam(args.webcam)
        elif args.video:
            app.run_video(args.video)
        elif args.image:
            app.run_image(args.image)
        else:
            # Default to webcam
            logger.info("No input specified, defaulting to webcam")
            app.run_webcam()
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()
