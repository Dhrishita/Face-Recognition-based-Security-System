# Face Recognition based Security System

Welcome to the Security System! This repository contains the source code and documentation for a security system developed as part of a university project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Components](#components)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#codestructure)
- [Contact](#contact)

## Introduction

This project is a face recognition based security system implemented using a Raspberry Pi. The system is capable of real time face detection and recognition, allowing access only to authorized individuals. It uses Python programming language along with OpenCV for image processing and face recognition. The system can also notify the owner via email with an OTP and a photo of any unrecognized individual attempting access.

## Features

- Real-time face detection and recognition
- Notification via email for unrecognized faces
- Access control based on face recognition
- Backup security with a 4-digit PIN code
- Easy to configure and use

## Components
- Raspberry Pi 3 Model B
- Camera module
- LED indicator
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
   git clone https://github.com/your-username/face-recognition-security-system.git
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

## Contact
If you have any questions or suggestions, feel free to open an issue or contact:
Dhrishita Parve: dhrishitap18@gmail.com


