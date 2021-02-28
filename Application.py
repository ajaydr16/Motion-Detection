import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
#import mail
import time
import datetime
import smtplib


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("akash.mallareddy@gmail.com", "dhanasree")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("akash.mallareddy@gmail.com", "ajaydr25@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
cap = cv2.VideoCapture(file_path)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Intruder Detected'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    image = cv2.resize(frame1, (1280,720))
    out.write(image)
    cv2.imshow("Detecting", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d, %H:%M:%S')
send_email("INTRUDER DETECTED", "Hi!\n intruder has been detected from source at " + st + ". ""\nStay safe,\nTresspassing Detection Team")

cv2.destroyAllWindows()
cap.release()
out.release()
