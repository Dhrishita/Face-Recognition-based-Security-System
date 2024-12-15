import face_recognition
import cv2
import time
import smtplib
import random
import RPi.GPIO as GPIO
import os
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Initialize GPIO settings
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set up GPIO pins for keypad
row_list = [18, 22, 24, 26]
col_list = [32, 36, 38, 40]
for pin in row_list:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

for pin in col_list:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up GPIO for other components
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Load the reference image
reference_image = face_recognition.load_image_file("/home/dhrishita/Dhrishita.jpeg")
reference_encoding = face_recognition.face_encodings(reference_image)[0]
reference_name = "Dhrishita"

def bye():
    print("Entry denied")
    print("BYE")
    exit()

def keypad_reading():
    key_map = [["1", "2", "3", "A"],
               ["4", "5", "6", "B"],
               ["7", "8", "9", "C"],
               ["*", "0", "#", "D"]]

    value = ""
    j = 0
    while j < 4:
        for r in row_list:
            GPIO.output(r, GPIO.LOW)
            result = [GPIO.input(col) for col in col_list]

            if min(result) == 0:
                key = key_map[int(row_list.index(r))][int(result.index(0))]
                GPIO.output(r, GPIO.HIGH)  # manages key kept pressed
                value += key
                os.system('clear')
                print("Value entered is: " + value)
                j += 1
                sleep(0.3)
                break

            GPIO.output(r, GPIO.HIGH)

    os.system('clear')
    return value

def opendoor(name):
    print("Welcome Home " + name)
    exit()

def display(msg1, msg2):
    print(msg1)
    print("\n")
    print(msg2)
    return

def takephoto(camera_index=0, save_path="/home/dhrishita/guest_image.jpeg"):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        display("take_photo", "Camera not opening")
        sleep(5)
        return
    ret, frame = cap.read()
    if not ret:
        display("take_photo", "Could not click a picture")
        sleep(5)
        return
    cv2.imwrite(save_path, frame)
    cap.release()
    print("Photo saved as:", save_path)
    return

def intruder():
    otp = random.randint(1000, 9999)
    sender_email = "mahimu1853@gmail.com"
    sender_password = "cxgs qklq eflm pzhp"  
    receiver_email = "dhrishitap18@gmail.com"

    # Create server object
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Intruder detected."
    msg.attach(MIMEText("Your OTP is: {}".format(otp)))

    # Attach the image
    image_path = "/home/dhrishita/guest_image.jpeg"  
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        image = MIMEImage(image_data, name=os.path.basename(image_path))
        msg.attach(image)

    # Send email
    server.send_message(msg)
    server.quit()

    passwd = keypad_reading()

    if passwd == str(otp):
        opendoor("Stranger")
    else:
        bye()

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

while True:
    if GPIO.input(15) == GPIO.HIGH:  # Face detection starts when the button is pressed
        lst = []
        t_end = time.time() + 10
        name = "Unknown"

        while time.time() < t_end:
            ret, frame = video_capture.read()
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces([reference_encoding], face_encoding)
                if matches[0]:
                    name = reference_name
                    opendoor(name)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        video_capture.release()

        if name == "Unknown":
            takephoto()
            intruder()

# Cleanup GPIO on exit
GPIO.cleanup()