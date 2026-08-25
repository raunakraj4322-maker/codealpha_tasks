# Object Detection and Tracking Application

**CodeAlpha AI Internship - Task 4**

A real-time object detection and tracking application using YOLO (You Only Look Once) with professional visualization and tracking capabilities.

---

## Project Overview

This application implements real-time object detection and tracking using computer vision techniques. It uses a pre-trained YOLO11n model to detect objects in video streams and applies object tracking algorithms to maintain identity across frames. The application provides a professional desktop interface with real-time statistics and interactive controls.

### Key Features

- **Real-time Object Detection**: Detects 80 common object classes from the COCO dataset
- **Object Tracking**: Maintains tracking IDs across video frames using ByteTrack
- **Multiple Input Sources**: Webcam, video files, and single images
- **Professional UI**: Clean OpenCV-based interface with statistics overlay
- **Configurable**: Adjustable confidence thresholds and class filtering
- **Performance Optimized**: Lightweight YOLO11n model suitable for student laptops
- **CPU/GPU Support**: Automatic device detection with graceful CPU fallback

---

## Technology Stack

### Backend / Computer Vision
- **Python 3.11+**: Core programming language
- **OpenCV**: Video processing and visualization
- **Ultralytics YOLO**: Object detection model (YOLO11n)
- **NumPy**: Numerical operations
- **PyTorch**: Deep learning framework (via Ultralytics)

### Architecture
- **Modular Design**: Separated detection, tracking, and processing modules
- **Service-Oriented**: Video processor and statistics manager services
- **Configuration-Driven**: Centralized configuration management

---

## YOLO Model Explanation

### Model: YOLO11n (Nano)

**Why YOLO11n was selected:**
- **Lightweight**: Optimized for edge devices and student laptops
- **Real-time Performance**: Capable of processing 30+ FPS on modern CPUs
- **Good Accuracy**: Maintains competitive accuracy despite small size
- **Modern Architecture**: Latest version of YOLO with improved performance
- **Easy Integration**: Seamless integration via Ultralytics library

### Model Specifications
- **Model Name**: YOLO11n (yolo11n.pt)
- **Parameters**: ~2.6M parameters
- **Model Size**: ~6MB
- **Dataset**: COCO (Common Objects in Context)
- **Classes**: 80 object categories
- **Input Size**: 640x640 (default, configurable)

### Supported Classes

The model can detect 80 common object categories including:

**People & Animals:**
- Person, bicycle, car, motorcycle, airplane, bus, train, truck, boat
- Bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe

**Household Items:**
- Backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard
- Sports ball, kite, baseball bat, baseball glove, skateboard, surfboard
- Tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl

**Food:**
- Banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

**Furniture & Electronics:**
- Chair, couch, potted plant, bed, dining table, toilet, tv, laptop
- Mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator

**Other:**
- Traffic light, fire hydrant, stop sign, parking meter, bench, book, clock
- Vase, scissors, teddy bear, hair drier, toothbrush

### Model Loading

The model weights are automatically downloaded on the first run from the Ultralytics official repository. The model is cached locally in the `models/` directory for subsequent uses.

**Important**: Model weights are NOT committed to Git to avoid large file sizes. They are downloaded automatically when needed.

---

## Object Detection Explanation

Object detection is the computer vision task of identifying and locating objects within an image or video frame. This application uses YOLO (You Only Look Once), a state-of-the-art detection algorithm.

### How YOLO Works

1. **Input Processing**: The video frame is resized to the model's input size (640x640)
2. **Feature Extraction**: A convolutional neural network extracts features from the image
3. **Bounding Box Prediction**: The model predicts bounding boxes, class probabilities, and confidence scores
4. **Non-Maximum Suppression (NMS)**: Overlapping detections are merged using IoU threshold
5. **Filtering**: Detections below the confidence threshold are removed

### Detection Pipeline

```
Frame Input → YOLO Model → Bounding Boxes → Confidence Filtering → Output Detections
```

### Confidence Threshold

The confidence threshold determines which detections are displayed:
- **Default**: 0.25 (25% confidence)
- **Range**: 0.0 to 1.0
- **Effect**: Higher values = fewer but more confident detections
- **Adjustable**: Can be changed via command line or configuration

---

## Object Tracking Explanation

Object tracking maintains the identity of detected objects across consecutive video frames, allowing the system to follow objects as they move.

### Tracking Algorithm: ByteTrack

This application uses **ByteTrack**, a high-performance multi-object tracking algorithm:

**Why ByteTrack:**
- **High Accuracy**: State-of-the-art tracking performance
- **Simple Integration**: Built into Ultralytics YOLO
- **Robust**: Handles occlusions and re-identification well
- **Efficient**: Low computational overhead
- **Real-time**: Suitable for live video processing

### How ByteTrack Works

1. **Detection Association**: Associates detections in the current frame with existing tracks
2. **Motion Prediction**: Uses Kalman filtering to predict object positions
3. **Track Management**: Creates new tracks for unassociated detections
4. **Track Deletion**: Removes tracks that haven't been matched for several frames
5. **ID Assignment**: Maintains consistent tracking IDs across frames

### Tracking Pipeline

```
Detections → ByteTrack → Track Association → ID Assignment → Tracked Objects
```

### Tracking IDs

Each tracked object receives a unique ID that persists across frames:
- **Format**: Integer (e.g., 1, 2, 3, ...)
- **Persistence**: IDs remain consistent as long as the object is visible
- **Display**: Shown on bounding boxes (e.g., "Person | ID:7 | 0.91")
- **Colors**: Consistent colors per object class for visual distinction

---

## Supported Input Sources

### 1. Webcam
- **Default Camera**: Index 0 (default system webcam)
- **Custom Camera**: Specify camera index (e.g., `--webcam 1`)
- **Resolution**: Configurable (default: 1280x720)
- **FPS Limit**: Configurable (default: 30 FPS)

### 2. Video Files
- **Supported Formats**: MP4, AVI, MOV, MKV, WMV
- **File Size Limit**: 500MB (configurable)
- **Automatic Processing**: Processes entire video frame-by-frame
- **Controls**: Pause/resume during playback

### 3. Images
- **Supported Formats**: JPG, JPEG, PNG, BMP, TIFF
- **Single Frame**: Detection without tracking
- **Quick Preview**: Displays results with statistics

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd Task_4_Object_Detection_Tracking

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install PyTorch

Choose the appropriate PyTorch installation based on your system:

**CPU-only (most compatible):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**CUDA 11.8 (NVIDIA GPU):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**CUDA 12.1 (NVIDIA GPU):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import cv2; import torch; import ultralytics; print('Installation successful!')"
```

---

## How to Run

### Basic Usage

**Run with default webcam:**
```bash
python -m app.main
```

**Run with specific camera:**
```bash
python -m app.main --webcam 1
```

**Run with video file:**
```bash
python -m app.main --video path/to/video.mp4
```

**Run with image:**
```bash
python -m app.main --image path/to/image.jpg
```

### Advanced Options

**Set confidence threshold:**
```bash
python -m app.main --confidence 0.5
```

**Specify device:**
```bash
python -m app.main --device cuda  # Use GPU
python -m app.main --device cpu   # Force CPU
```

**Disable tracking:**
```bash
python -m app.main --no-tracking
```

**Combined options:**
```bash
python -m app.main --webcam --confidence 0.3 --device cuda
```

---

## Configuration

Configuration is managed through the `Config` class in `app/config.py`. Key settings:

### Model Settings
```python
MODEL_NAME = "yolo11n.pt"              # Model to use
CONFIDENCE_THRESHOLD = 0.25           # Detection confidence threshold
IOU_THRESHOLD = 0.45                   # NMS IoU threshold
MAX_DETECTIONS = 300                   # Maximum detections per frame
```

### Device Settings
```python
DEVICE = "auto"                        # "auto", "cpu", "cuda", "mps"
```

### Tracking Settings
```python
TRACKING_ENABLED = True                # Enable/disable tracking
TRACKER_TYPE = "bytetrack"             # "bytetrack" or "botsort"
```

### Video Settings
```python
WEBCAM_INDEX = 0                       # Default webcam index
VIDEO_WIDTH = 1280                     # Video width
VIDEO_HEIGHT = 720                     # Video height
FPS_LIMIT = 30                         # FPS limit
```

### UI Settings
```python
DISPLAY_FPS = True                     # Show FPS
DISPLAY_STATISTICS = True              # Show statistics
SHOW_TRACKING_ID = True                # Show tracking IDs
SHOW_CONFIDENCE = True                 # Show confidence scores
```

---

## CPU/GPU Usage

### Automatic Device Detection

The application automatically detects and uses the best available device:

1. **CUDA**: If NVIDIA GPU with CUDA is available
2. **MPS**: If Apple Silicon GPU is available (macOS)
3. **CPU**: If no GPU is available

### Check Device in Use

The device being used is displayed in the console logs on startup:
```
INFO - Device: cuda  # Using GPU
INFO - Device: cpu   # Using CPU
```

### Force Specific Device

Override automatic detection:
```bash
python -m app.main --device cpu   # Force CPU
python -m app.main --device cuda  # Force GPU
```

### Performance Notes

- **GPU**: 30-60 FPS typical with modern NVIDIA GPU
- **CPU**: 5-15 FPS typical on modern CPU (varies by hardware)
- **Optimization**: Lower resolution for better CPU performance

---

## Project Structure

```
Task_4_Object_Detection_Tracking/
│
├── app/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── main.py                      # Application entry point
│   │
│   ├── detection/
│   │   ├── __init__.py
│   │   ├── detector.py              # YOLO object detection
│   │   └── tracker.py               # Object tracking management
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── video_processor.py       # Video/webcam handling
│   │   └── statistics.py            # Statistics tracking
│   │
│   └── ui/
│       ├── __init__.py
│       └── desktop_ui.py            # OpenCV desktop interface
│
├── tests/                           # Test files
│
├── models/                          # Model weights (auto-downloaded)
├── output/                          # Generated output files
├── temp/                            # Temporary files
│
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── AUDIT_REPORT.md                  # Audit and testing report
├── .gitignore                       # Git ignore rules
│
└── .env.example                     # Environment variables template
```

---

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

The test suite includes:
- Model loading tests
- Detection inference tests
- Tracking functionality tests
- Video processing tests
- Error handling tests
- Configuration tests

---

## Security Considerations

### File Upload Security
- **File Type Validation**: Only supported video/image formats accepted
- **File Size Limits**: Maximum 500MB for video files
- **Path Traversal Protection**: Safe file path handling
- **No Remote Downloads**: Does not accept arbitrary URLs

### Dependency Security
- **Pinned Versions**: Dependencies specify minimum versions
- **Reputable Sources**: All packages from PyPI or official repositories
- **Regular Updates**: Keep dependencies updated

### Data Privacy
- **No Data Collection**: Does not collect or transmit personal data
- **Local Processing**: All processing occurs locally
- **No API Keys**: No external API keys required
- **No Logging**: Sensitive information is not logged

### Model Weights
- **Safe Download**: Model weights from official Ultralytics repository
- **Checksum Verification**: Integrity verification during download
- **No Custom Models**: Uses only official pre-trained models

---

## Performance Considerations

### Optimization Tips

1. **Use GPU**: CUDA provides 3-5x speedup over CPU
2. **Lower Resolution**: Reduce video resolution for better FPS
3. **Adjust Confidence**: Higher threshold = faster processing
4. **Filter Classes**: Reduce detected classes for speed
5. **Disable Tracking**: Slight performance improvement without tracking

### Performance Benchmarks

**Typical Performance (YOLO11n):**
- **NVIDIA RTX 3060**: 45-60 FPS
- **NVIDIA GTX 1650**: 25-35 FPS
- **Modern CPU (i7/Ryzen 7)**: 8-15 FPS
- **Older CPU (i5/Ryzen 5)**: 5-10 FPS

**Memory Usage:**
- **GPU VRAM**: ~1-2GB
- **System RAM**: ~2-4GB
- **Disk Space**: ~100MB (excluding model cache)

---

## Limitations

### Known Limitations

1. **CPU Performance**: Real-time performance requires GPU on higher resolutions
2. **Lighting Conditions**: Detection accuracy decreases in poor lighting
3. **Small Objects**: May miss very small objects (< 32x32 pixels)
4. **Occlusion**: Tracking may fail with heavy occlusion
5. **Model Classes**: Limited to 80 COCO classes
6. **Webcam Access**: Requires compatible webcam and proper permissions

### Environment Limitations

- **Python Version**: Requires Python 3.11+
- **Operating System**: Tested on Windows, macOS, Linux
- **GPU**: NVIDIA GPU with CUDA required for GPU acceleration
- **Memory**: Minimum 4GB RAM recommended

---

## Future Improvements

### Potential Enhancements

1. **Additional Models**: Support for other YOLO variants (YOLO11s, YOLO11m)
2. **Custom Classes**: Support for custom-trained models
3. **Web Interface**: Browser-based UI with streaming
4. **Recording**: Save processed video with annotations
5. **Export Data**: Export detection/tracking data to CSV/JSON
6. **Multi-camera**: Support for multiple simultaneous cameras
7. **Alert System**: Custom alerts for specific objects
8. **Mobile Support**: Android/iOS application
9. **Edge Deployment**: Optimized for edge devices
10. **Batch Processing**: Process multiple videos automatically

---

## Controls

### Keyboard Shortcuts

- **SPACE**: Pause/Resume video
- **Q**: Quit application
- **S**: Toggle statistics display
- **L**: Toggle labels
- **C**: Toggle confidence scores
- **T**: Toggle tracking IDs

---

## Troubleshooting

### Common Issues

**Issue**: "Failed to open webcam"
- **Solution**: Check webcam permissions, try different camera index

**Issue**: "CUDA out of memory"
- **Solution**: Use CPU mode or reduce video resolution

**Issue**: "Model loading failed"
- **Solution**: Check internet connection (first run), reinstall dependencies

**Issue**: "Low FPS on CPU"
- **Solution**: Reduce video resolution, use GPU if available

**Issue**: "No detections visible"
- **Solution**: Lower confidence threshold, check lighting conditions

---

## License

This project is developed as part of the CodeAlpha AI Internship program.

**Model License**: The YOLO11n model is provided by Ultralytics under the AGPL-3.0 license.

**Code License**: This project code is provided for educational purposes.

---

## Acknowledgments

- **Ultralytics**: For the YOLO implementation and model
- **COCO Dataset**: For the training dataset
- **OpenCV**: For computer vision utilities
- **PyTorch**: For deep learning framework
- **CodeAlpha**: For the internship opportunity

---

## Contact

For questions or issues related to this CodeAlpha task, please refer to the internship guidelines or contact your CodeAlpha mentor.

---

**Project Status**: ✅ Complete  
**Last Updated**: August 2026  
**Version**: 1.0.0
