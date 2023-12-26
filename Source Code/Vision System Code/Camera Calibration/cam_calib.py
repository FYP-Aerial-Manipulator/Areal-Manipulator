import numpy as np
import cv2
import time
import os
import shutil

# Specify the folder name
images_folder = "images"

# Remove the existing "images" folder and its contents
if os.path.exists(images_folder):
    shutil.rmtree(images_folder)

# Create the "images" folder
os.makedirs(images_folder)

# Rest of the code remains unchanged
cv2.namedWindow("Image Feed")
cv2.moveWindow("Image Feed", 159, -25)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 40)

prev_frame_time = time.time()

cal_image_count = 0
frame_count = 0

while True:
    ret, frame = cap.read()

    # Processing code goes here
    frame_count += 1

    if frame_count == 30:
        image_path = os.path.join(images_folder, f"cal_image_{cal_image_count}.jpg")
        cv2.imwrite(image_path, frame)
        cal_image_count += 1
        frame_count = 0

    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, "FPS " + str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 3, (100, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Image Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
