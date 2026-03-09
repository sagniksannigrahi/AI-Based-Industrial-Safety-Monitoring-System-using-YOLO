
# AI-Based Industrial Safety Monitoring System using YOLO

An **AI-powered real-time industrial safety monitoring system** that detects safety violations such as **workers without helmets and fire hazards** using **YOLOv8 object detection**, logs incidents into a database, and sends **instant email alerts** to safety officers.

This project helps improve **workplace safety, accident prevention, and real-time monitoring in industrial environments.**

---

# Project Overview

Industrial environments require constant monitoring to ensure workers follow safety protocols. Manual monitoring is inefficient and prone to human error.

This system uses **computer vision and AI** to automatically detect:

* Workers
* Safety helmets
* Fire hazards

The system provides:

* Real-time camera monitoring
* Automatic violation detection
* Safety event logging
* Email alert notifications
* Web dashboard for monitoring logs

---

# System Architecture

```
Camera Feed
     │
     ▼
YOLOv8 Object Detection
     │
     ▼
Safety Analysis
(Workers vs Helmets / Fire Detection)
     │
     ├── Email Alert System
     │
     ├── Database Logging
     │
     ▼
Web Dashboard (Flask)
```

---

# Features

### Real-Time Worker Detection

Detects workers using YOLOv8 model.

### Helmet Safety Detection

Checks whether workers are wearing safety helmets.

### Fire Hazard Detection

Identifies potential fire hazards.

### Automatic Email Alerts

Sends instant alert emails when violations occur.

Example Alert:

```
Helmet Violation Detected

Workers: 1
Helmets: 0
Time: 2026-02-12 19:14
```

### Database Logging

All events are stored in a **SQLite database**.

Logged Data:

| Field       | Description                    |
| ----------- | ------------------------------ |
| ID          | Log ID                         |
| Date        | Timestamp                      |
| Workers     | Number of workers detected     |
| Helmets     | Number of helmets detected     |
| Fire Status | YES / NO                       |
| Violation   | SAFE / HELMET VIOLATION / FIRE |

### Monitoring Dashboard

A Flask-based web dashboard to view logs.

Displays:

* Worker count
* Helmet count
* Fire detection status
* Violation logs

---

# Technologies Used

| Technology           | Purpose                   |
| -------------------- | ------------------------- |
| Python               | Core programming language |
| YOLOv8 (Ultralytics) | Object detection          |
| OpenCV               | Camera feed processing    |
| Flask                | Web dashboard             |
| SQLite               | Database storage          |
| SMTP                 | Email alert system        |

---

# Project Structure

```
Industrial_Safety_YOLO
│
├── app.py                     # Flask web dashboard
├── database.py                # Database creation
├── safety_detect.py           # YOLO detection
├── safety_detect_and_save.py  # Detection + logging + alerts
│
├── templates
│    └── index.html            # Dashboard UI
│
├── safety.db                  # SQLite database
├── yolov8n.pt                 # YOLO model
│
└── README.md
```

---

# Installation

Clone the repository

```
git clone https://github.com/yourusername/Industrial-Safety-YOLO.git
cd Industrial-Safety-YOLO
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Install dependencies

```
pip install ultralytics opencv-python flask
```

---

# Run the Project

### Step 1 — Create Database

```
python database.py
```

### Step 2 — Run Detection System

```
python safety_detect_and_save.py
```

Press **S** to save logs.

---

### Step 3 — Launch Dashboard

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# Example Outputs

### Detection Window

* Worker detection
* Helmet count
* Fire status

### Email Alert

Instant alert sent to safety officer.

### Database Logs

| ID | Date       | Workers | Helmets | Fire | Violation        |
| -- | ---------- | ------- | ------- | ---- | ---------------- |
| 1  | 2026-02-12 | 1       | 0       | NO   | HELMET VIOLATION |

---

# Future Improvements

* WhatsApp alert system
* Real industrial dataset training
* Fire and smoke detection models
* Safety analytics dashboard
* Multi-camera monitoring
* Deployment on edge devices

---

# Applications

* Manufacturing industries
* Construction sites
* Oil and gas plants
* Mining industries
* Smart factories

---

# Author

**Sagnik Sannigrahi**
CSE Student
SRM Institute of Science and Technology
