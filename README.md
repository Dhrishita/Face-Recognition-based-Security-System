# Embedded Door Lock Security System

Welcome to the Security System! This repository contains the source code and documentation for a security system developed as part of a Minor Project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Components Required](#components-required)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Woking of the Project](#working-of-the-project)
- [Demo](#demo)
- [Contact](#contact)

## Introduction

This project is a face recognition based security system implemented using a Raspberry Pi. The system is capable of real time face detection and recognition, allowing access only to authorized individuals. It uses Python programming language along with OpenCV for image processing and face recognition. The system can also notify the owner via email with an OTP and a photo of any unrecognized individual attempting access.

## Features

- Real-time face detection and recognition
- Notification via email for unrecognized faces
- Access control based on face recognition
- Backup security with a 4-digit PIN code
- Easy to configure and use

## Components Required
- Raspberry Pi 4
- Web Cam
- Switch (as Door bell)
- LED indicator
- Keypad
- Breadboard
- Jumper wires
- Python programming language
- OpenCV library
- Flask framework
- Email notification using smtplib
  
## Installation
## Hardware Setup

1. Connect the camera module to the Raspberry Pi.
2. Connect the LED indicator to the GPIO pins on the Raspberry Pi.
   
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install opencv-python
    pip3 install flask
    pip3 install smtplib
    
## Usage
1. Clone this repository to your Raspberry Pi:
   
   ```bash
   git clone https://github.com/Dhrishita/face-recognition-security-system.git
   cd face-recognition-security-system
   
3. Run the Python script:
   
   ```bash
   python3 main.py

5. The system will start and wait for someone to stand in front of the camera. If the face is recognized, access will be granted. If the face is not recognized, an email with an OTP and the photo of the individual will be sent to the owner's email.

## Code Structure
- 'main.py': The main script to run the face recognition system.
- 'face_recognition.py': Contains the face recognition logic using OpenCV.
- 'email_notification.py': Handles sending email notifications for unrecognized faces.
- 'utils.py': Utility functions for the system.

## Working of the Project

1. **Startup and Initialization**:
   - The Raspberry Pi initializes the hardware, including the camera module, keypad, and LED indicator.
   - Necessary Python libraries like OpenCV, Flask, and smtplib are loaded.

2. **Face Detection**:
   - The camera continuously monitors the area in front of the door.
   - Using OpenCV’s Haar cascades or DNN-based face detection, the system detects faces in the live video feed.

3. **Face Recognition**:
   - Detected faces are compared with the system’s database of pre-stored authorized individuals using a face recognition model (e.g., HOG-based, CNN, or DLIB library).
   - If the face matches an authorized individual, the system grants access:
     - The LED indicator glows green.
     - A signal is sent to unlock the door (using a connected relay module).

4. **Handling Unrecognized Faces**:
   - If the face is not recognized, the system performs the following actions:
     - Captures a photo of the unrecognized individual.
     - Generates a One-Time Password (OTP) and sends an email to the owner using the `smtplib` library.
     - The email includes:
       - The photo of the unrecognized individual.
       - A message prompting for OTP verification.

5. **Backup PIN Access**:
   - A keypad is available as a backup method to unlock the door.
   - The owner (or authorized individuals) can enter a pre-configured 4-digit PIN code.
   - If the PIN is correct, the system grants access.

6. **Security Layer for OTP**:
   - The owner can use the OTP received via email to manually verify and grant access if needed.
   - If the OTP is entered correctly on the keypad, the system unlocks the door.

7. **Notification**:
   - The system logs all access attempts, including timestamps and face recognition results.
   - Owners can review these logs for security purposes.

8. **Flask Framework for Remote Monitoring**:
   - The system includes a web interface (using Flask) that allows the owner to remotely view live camera feeds and manage access logs.

## Demo

https://github.com/user-attachments/assets/6b759b6c-ebb1-4930-8339-d4f1130d72b4

## Contact
If you have any questions or suggestions, feel free to open an issue or contact:
Dhrishita Parve: dhrishitap18@gmail.com


