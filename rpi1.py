import face_recognition
import cv2
import time
import smtplib
import random
import RPi.GPIO as GPIO
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
#from rpi_lcd import LCD
#lcd=LCD()

######################
# EXITING THE CODE
def bye():
    print("Entry denied")
    print("BYE")
    exit()


#######################

def keypad_reading():
    row_list = [18, 22, 24, 26]
    col_list = [32, 36, 38, 40]

    for pin in row_list:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    for pin in col_list:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    key_map = [["1", "2", "3", "A"],\
               ["4", "5", "6", "B"],\
               ["7", "8", "9", "C"],\
               ["*", "0", "#", "D"]]

    def Keypad4x4Read(cols, rows):
        for r in rows:
            GPIO.output(r, GPIO.LOW)

            result = [GPIO.input(cols[0]), GPIO.input(cols[1]), GPIO.input(cols[2]), GPIO.input(cols[3])]

            if min(result) == 0:
                key = key_map[int(rows.index(r))][int(result.index(0))]
                GPIO.output(r, GPIO.HIGH)  # manages key keept pressed
                return key

            GPIO.output(r, GPIO.HIGH)

    value = ""
    j = 0
    while (j < 4):
        try:
            key = Keypad4x4Read(col_list, row_list)
            if key != None:
                value = value + key
                os.system('clear')
                print("value entered is :"+ value)
                j = j + 1
                time.sleep(0.3)
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()
    os.system('clear')
    return value


#########################################
def opendoor(a):
    # video_capture.release()
    # cv2.destroyAllWindows()
    print("welcome home " + a)
    exit()


###########################################
def display (msg1,msg2):
    print(msg1)
    print("\n")
    print(msg2)
    '''lcd.backlight(turn_on=False)
    sleep(5)
    lcd.backlight(turn_on=True)

    lcd.clear()
    lcd.text(msg1,1)
    lcd.text(msg2,2)'''
    return
############################################################


def takephoto(camera_index=0, save_path="/home/dhrishita/guest_image.jpeg"):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        display("take_photo" ,"camera not opening")
        sleep(5)
        lcd.clear()
        return
    ret, frame = cap.read()
    if not ret:
        display("take_photo", "could not click a picture")
        sleep(5)
        lcd.clear()
        return
    cv2.imwrite(save_path, frame)
    cap.release()
    print("Photo saved as:", save_path)
    return


################################################################


#################################################################
def intruder():
    otp = random.randint(1000, 9999)
    sender_email = "21bec088@nirmauni.ac.in"
    sender_password = "Dhrishita0518"
    receiver_email = "dhrishitap18@gmail.com"

    # Create server object
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Login to email server
    server.login(sender_email, sender_password)

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Intruder detected."
    msg.attach(MIMEText("Your otp is: {}".format(otp)))

    # Attach the image
    image_path = "/home/dhrishita/guest_image.jpeg"  # Replace with the actual path to your image
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        image = MIMEImage(image_data, name=os.path.basename(image_path))
        msg.attach(image)

    # Send email
    server.send_message(msg)

    # Close server connection
    server.quit()

    passwd=keypad_reading()


    if (passwd == str(otp)):
        opendoor("stranger")
    else:
        bye()

    exit()


#########################################################################


########################################################################################

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Load the reference image
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
reference_image = face_recognition.load_image_file("/home/dhrishita/Dhrishita.jpeg")
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Assign a name for the reference image
reference_name = "Dhrishita"
name = "Unknown"

   
#while True:
    #if GPIO.input(15) == GPIO.HIGH:
# Initialize the webcam
video_capture = cv2.VideoCapture(0)
lst = []
t_end = time.time() + 10
while time.time() < t_end:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the face encoding with the reference encoding
        matches = face_recognition.compare_faces([reference_encoding], face_encoding)
        # If a match is found, assign the reference name
        if matches[0]:
            name = reference_name
            opendoor(name)
        # Draw a green rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display the resulting frame
    # .imshow('Video', frame)

    # Break the loop if 'q' is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    # break

# Release the webcam and close all windows
video_capture.release()
# cv2.destroyAllWindows()

if name == "Unknown":
    takephoto()
    intruder()
