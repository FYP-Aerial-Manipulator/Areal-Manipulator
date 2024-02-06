import numpy as np
import cv2
import cv2.aruco as aruco

marker_size = 25 #30

# Load camera calibration parameters
with open('camera_cal.npy', 'rb') as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

cap = cv2.VideoCapture(0)

camera_width = 640 #1280 #640
camera_height = 480 #720 #480
camera_frame_rate = 60

cap.set(3, camera_width)  # Set width
cap.set(4, camera_height)  # Set height
cap.set(5, camera_frame_rate)  # Set frame rate

while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners)  # Draw a box around all the detected markers
        rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

        rvec = rvec_list_all[0][0]
        tvec = tvec_list_all[0][0]

        aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 100)

        # Print X, Y, Z coordinates at the edges with unit (mm)
        tvec_str = "x=%4.0f mm y=%4.0f mm z=%4.0f mm" % (tvec[0], tvec[1], tvec[2])
        #cv2.putText(frame, tvec_str, (20, 460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

        # Print X, Y, Z coordinates at the edges with unit (mm)
        font_size = 1.5
        #x_str = "X: %4.0f mm" % tvec[0]
        #y_str = "Y: %4.0f mm" % tvec[1]
        #z_str = "Z: %4.0f mm" % tvec[2]
        x_str = "X: %4.1f cm" % (tvec[0] / 10)
        y_str = "Y: %4.1f cm" % (tvec[1] / 10)
        z_str = "Z: %4.1f cm" % (tvec[2] / 10)

        cv2.putText(frame, x_str, (20, 40), cv2.FONT_HERSHEY_PLAIN, font_size, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, y_str, (20, 80), cv2.FONT_HERSHEY_PLAIN, font_size, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, z_str, (20, 120), cv2.FONT_HERSHEY_PLAIN, font_size, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
