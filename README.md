# Autonomous-Drone-integrating-AI-for-Object-Detection

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent drone control system that uses computer vision to autonomously detect and track a person. This project leverages the **YOLOv5** object detection model, **DroneKit** for MAVLink communication, and **OpenCV** for real-time video processing.



The drone operates using a robust state machine to handle various scenarios like searching, tracking, handling target loss, and executing safety-critical failsafes.

## ✨ Key Features

- **Autonomous Person Tracking**: Locks onto the largest detected person and controls the drone's yaw, pitch, and throttle to maintain a consistent following distance and position.
- **Robust State Machine**: Manages states like `SEARCHING`, `TRACKING`, `GRACE_PERIOD` (for target occlusion), and `PAUSED`.
- **Safety Failsafes**: Automatically triggers a **Return-to-Launch (RTL)** on low battery, after a prolonged search timeout, or via operator command.
- **Real-time Operator Feedback**: An OpenCV window displays the drone's live camera feed, current state, battery level, and target bounding box.
- **Interactive Control**: The operator can pause, resume, force an RTL, or command a new target search using simple keyboard commands.
- **Modular & Configurable**: The entire project is split into logical modules (`controller`, `vision`, etc.), with all key parameters exposed in a simple `config.py` file for easy tuning.

## 🛠️ Technology Stack

- **Python 3.9+**
- **DroneKit**: For communicating with vehicle flight controllers over MAVLink.
- **PyTorch**: The core deep learning framework.
- **YOLOv5 (Ultralytics)**: For real-time, high-performance person detection.
- **OpenCV**: For camera interaction and video feed display.
- **NumPy**: For numerical operations.

## 📂 Project Structure

The project is organized into a clean, modular structure for better readability and maintenance.
