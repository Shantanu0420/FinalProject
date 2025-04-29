# Gesture Controlled Virtual Mouse  

[![](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/) [![platform](https://img.shields.io/badge/platform-windows-green.svg)](https://github.com/xenon-19/Gesture_Controller)  

Gesture Controlled Virtual Mouse enables intuitive human-computer interaction using hand gestures and voice commands, minimizing direct physical contact. This solution leverages advanced Machine Learning and Computer Vision algorithms to recognize gestures and voice inputs without requiring additional hardware. It utilizes MediaPipe's CNN models for hand detection and offers two modes: direct hand detection and colored glove detection (currently Windows-only).

📹 [Video Demonstration](https://www.youtube.com/watch?v=ufm6tfgo-OA&ab_channel=Proton)  
⚠️ Note: Use Python 3.8.5 for compatibility

## Key Features

### ✋ Gesture Recognition
- **Neutral Gesture**: Stops current gesture execution (open palm)  
- **Cursor Movement**: Controlled by index/middle fingertip midpoint  
- **Mouse Controls**:  
  - Left/Right click  
  - Double click  
  - Drag & drop  
  - Multi-item selection  
- **Scrolling**: Vertical/horizontal with speed control  
- **System Controls**:  
  - Volume adjustment  
  - Screen brightness  

### 🎙️ Voice Assistant (Proton)
- **Gesture System Control**:  
  - "Proton Launch/Stop Gesture Recognition"  
- **Web Operations**:  
  - Google searches  
  - Maps navigation  
- **File Management**:  
  - Directory navigation  
  - File opening  
- **Utilities**:  
  - Date/time queries  
  - Copy/paste functionality  
- **Assistant Control**:  
  - Sleep/wake commands  
  - System exit  

## Installation Guide

### Prerequisites
- Python 3.6-3.8.5  
- [Anaconda Distribution](https://www.anaconda.com/products/individual)

### Setup Instructions
1. Clone repository:
```bash
git clone https://github.com/xenon-19/Gesture-Controlled-Virtual-Mouse.git
```

2. Create conda environment:
```bash
conda create --name gest python=3.8.5
conda activate gest
```

3. Install dependencies:
```bash
pip install -r requirements.txt
conda install PyAudio pywin32
```

4. Navigate to src folder:
```bash
cd Gesture-Controlled-Virtual-Mouse/src
```

### Launch Options
**Voice Assistant Mode**:
```bash
python Proton.py
```
(Enable gestures with "Proton Launch Gesture Recognition" voice command)

**Gesture-Only Mode**:
1. Uncomment last 2 lines in `Gesture_Controller.py`
2. Run:
```bash
python Gesture_Controller.py
```
