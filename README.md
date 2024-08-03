# Face-Recognition-based-Security-System

Welcome to the Diabetes prediction! This repository contains the source code and documentation for a diabetes prediction developed as part of a university project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Components](#components)
- [Installation](#installation)
- [Usage](#usage)
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


To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Dhrishita/diabetes-prediction.git
   cd diabetes-prediction

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
Once the chatbot is running, you can interact with it via the command line or a web interface. Simply type your questions or statements and the chatbot will respond accordingly.

1. Prepare your dataset and place it in the data/ directory.
2. Train the model:
   ```bash
   python train_model.py
3. Evaluate the model:
   ```bash
   python evaluate_model.py
4. Use the model to make predictions:
   ```bash
   python predict.py

## Contact
If you have any questions or suggestions, feel free to open an issue or contact:
Dhrishita Parve: dhrishitap18@gmail.com


