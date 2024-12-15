import face_recognition
import cv2
import time
import smtplib
import random
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import numpy as np
import dlib

######################
# EXITING THE CODE
def bye():
    print("Entry denied")
    time.sleep(1)
    print("BYE! See you next time.")
    exit()

#########################################
def opendoor(a):
    print("Welcome home, " + a + ".")
    print(".")
    time.sleep(0.3)
    print(".")
    print("How was your day?")
    exit()

###########################################
def display(msg1, msg2):
    print(msg1)
    print("\n")
    print(msg2)

##########################
# INCREASE IMAGE BRIGHTNESS
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img_bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img_bright

############################################################
def takephoto(camera_index=0, save_path="guest_image", brightness_value=30):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        display("take_photo", "Oops! Camera not opening")
        sleep(5)
        return
    ret, frame = cap.read()
    if not ret:
        display("take_photo", "Could not click a picture")
        sleep(5)
        return

    frame = increase_brightness(frame, brightness_value)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_filename = f"{save_path}_{timestamp}.jpeg"
    cv2.imshow("Preview", frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    cv2.imwrite(image_filename, frame)
    cap.release()
    print("Photo saved as:", image_filename)
    return image_filename

################################################################ 
def send_email(image_path, otp):
    sender_email = "mahimu1853@gmail.com"
    sender_password = "ezbe vetg gltj qupy"
    receiver_email = "dhrishitap18@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender_email, sender_password)
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Intruder detected."
        msg.attach(MIMEText("Your OTP is: {}".format(otp)))

        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()
            image = MIMEImage(image_data, name=os.path.basename(image_path))
            msg.attach(image)

        server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
    finally:
        server.quit()

def intruder():
    otp = random.randint(1000, 9999)
    image_filename = takephoto()
    send_email(image_filename, otp)

    passwd = input("Enter the OTP to open the door: ")
    if passwd == str(otp):
        opendoor("Stranger")
    else:
        bye()

###########################################
#Points 1–17: Jawline
#Points 18–27: Eyebrows
#Points 28–36: Nose
#Points 37–48: Eyes
#Left Eye: Points 36–41
#Right Eye: Points 42–47
#Points 49–68: Mouth
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def check_liveliness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    EAR_THRESHOLD = 0.25
    CONSECUTIVE_FRAMES = 3
    blink_counter = 0

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
        right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        if left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD:
            blink_counter += 1
        else:
            if blink_counter >= CONSECUTIVE_FRAMES:
                return True
            blink_counter = 0

    return False

def alert_photo_detection():
    print("Don't fool me, you fool!")

def check_if_photo_shown(frame):
    # If liveliness check fails, this is a photo
    if not check_liveliness(frame):
        alert_photo_detection()
        return True
    return False

###########################################

# Load reference images and encodings
reference_image_dhrishita = face_recognition.load_image_file("d.jpg")
reference_encoding_dhrishita = face_recognition.face_encodings(reference_image_dhrishita)[0]
reference_names = ["Dhrishita"]
reference_encodings = [reference_encoding_dhrishita]

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

name = "Unknown"

video_capture = cv2.VideoCapture(0)
t_end = time.time() + 10

while time.time() < t_end:
    ret, frame = video_capture.read()
    if not ret:
        continue

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(reference_encodings, face_encoding)
        if True in matches:
            match_index = matches.index(True)
            name = reference_names[match_index]

            if check_liveliness(frame):
                opendoor(name)
            else:
                print("Liveliness check failed. Intruder detected!")
                intruder()

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Video', frame)

    # If a photo is shown (no liveliness detected), print message
    if check_if_photo_shown(frame):
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

if name == "Unknown":
    intruder()
