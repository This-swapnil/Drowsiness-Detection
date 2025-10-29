
# 💤 Drowsiness Detection using YOLOv11 & Streamlit

A real-time driver drowsiness detection system powered by YOLOv11 and Streamlit, capable of identifying driver fatigue, distractions, and unsafe behaviors such as phone usage, smoking, or yawning.
When any such behavior is detected, the system triggers an audio alert (warning.mp3) to warn the driver.


## 📘Table of Contents
    1. Overview
    2. Features
    3. Project Structure
    4. How It Works
    5. Installation
    6. Usage
    7. Results
    8. Future Improvements
    9. Author

## 🚀 Overview
This project implements drowsiness detection through deep learning-based object detection.
Using YOLOv11, the system identifies whether the driver appears drowsy, distracted, or alert, based on facial cues captured via webcam or uploaded videos/images.

It’s designed for real-time monitoring with a smooth browser interface built in Streamlit.
The integrated audio alarm system instantly alerts the driver to regain focus when drowsiness or distractions are detected.

## 🧠Features
✅ Multiple Input Sources
- 📸 Image upload
- 🎞️ Video upload
- 🎥 Live webcam detection

✅ YOLOv11-based Detection

Detects driver states such as:

- Drowsy
- Distracted (yawn, smoking, head drop, etc.)
- Phone usage
✅ Audio Alarm System

Triggers a continuous alarm sound (warning.mp3) when a risky behavior is detected.

✅ Streamlit Web UI

Interactive web interface with sidebar controls for:

- Model confidence slider
- Source selection
- Image/video upload

✅ Thread-Safe Video Streaming

Ensures smooth frame updates using OpenCV and Streamlit’s dynamic placeholders.

✅ Dynamic Alert Banner

Displays a top-screen warning (e.g., “⚠️ DROWSINESS DETECTED!”) in red for maximum visibility.

## 📁 Project Structure

```
DROWSINESS-DETECTION/
│
├── app.py                   # Main Streamlit app
├── utils.py                 # Core detection, alarm & frame logic
├── trained_model/
│   └── best.pt              # YOLOv11 trained model file
├── warning.mp3              # Audio alert file
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```
## ⚙️ How It Works

1. Model Loading
The YOLOv11 model (trained_model/best.pt) is loaded via the ultralytics package.

2. Input Handling
Users select between Image, Video, or Webcam mode in the Streamlit sidebar.

3. Detection Process
- Frames are captured and resized using OpenCV.
- YOLOv11 performs inference to detect classes like drowsy, distracted, phone, etc.
- Bounding boxes and detection labels are displayed on the video feed.

4. Alert & Alarm
- When a risky state is detected, a red banner message appears.
- The system plays a looping warning alarm (warning.mp3) using pygame.
- The alarm stops automatically when the driver returns to normal.

## Installation

1️⃣ Clone the Repository

```bash
git clone https://github.com/This-swapnil/Drowsiness-Detection.git
cd drowsiness-detection
```

2️⃣ Create Virtual Environment (Recommended)
```bash
conda create -n env_name python=3.13
conda activate env_name
```

3️⃣ Install Dependencies
``` bash
pip install -r requirements.txt
```

4️⃣ Place Model File
```bash
trained_model/best.pt
```
## ▶️ Usage/Examples
Run the Streamlit Application
```bash
streamlit run app.py
```

### In the Web Interface:

1. Select Model Confidence (e.g., 0.5).

2. Choose input source:
- Image → Upload and click “Predict.”
- Video → Upload a driving video.
- Webcam → Start live detection.

3. When drowsiness or distraction is detected:
- ⚠️ A red alert banner appears.
- 🔊 The warning.mp3 alarm plays automatically.

## 📊 Results  

| Condition      | Detection Label | System Response |
|----------------|-----------------|-----------------|
| Normal Driving | —               | No alert        |
| Eyes Closed    | Drowsy          | Alarm + Banner  |
| Yawning        | Distracted      | Alarm + Banner  |
| Phone in Hand  | Phone           | Alarm + Banner  |
| Looking Away   | Distracted      | Alarm + Banner  |

**Average FPS:** 20–25  
**Detection Accuracy:** ~90%

## 🧭 Future Improvements
- 🌐 Integrate WebRTC live streaming for browser webcam access. (code is commented, uncomment RTC_CONFIGURATION and def infer_webcam_server(confidence, model) method)
- 🧬 Use facial landmarks for more precise eye and mouth tracking.
- 🔊 Add voice alerts instead of tone alarms.
- 📱 Build mobile version using Flutter or React Native.
- ☁️ Deploy model on AWS/GCP for cloud inference.

## Authors
**Swapnil Sonawane**
- 💻 [GitHub](https://github.com/This-swapnil)
- 🔗 [LinkedIn](https://www.linkedin.com/in/swapnil-s-sonawane/)

## 🪪 License

This project is released under the MIT License.
You’re free to use, modify, and distribute it with proper attribution.