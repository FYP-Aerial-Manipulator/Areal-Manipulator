import numpy as np
import cv2
import glob
import os

cb_width = 8
cb_height = 5
cb_square_size = 28

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) .... , (6,5,0)
cb_3D_points = np.zeros((cb_width * cb_height, 3), np.float32)
cb_3D_points[:, :2] = np.mgrid[0:cb_width, 0:cb_height].T.reshape(-1, 2) * cb_square_size

# Arrays to store object points and image points from all the images.
list_cb_3d_points = []  # 3d point in real world space
list_cb_2d_img_points = []  # 2d points in image plane.
list_images = glob.glob(os.path.join("rotation_matrix_image", '*.jpg'))

for frame_name in list_images:
    img = cv2.imread(frame_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (cb_width, cb_height), None)

    # If found, add object points, image points (after refining them)
    if ret:
        list_cb_3d_points.append(cb_3D_points)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        list_cb_2d_img_points.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (cb_width, cb_height), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Calibrate camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(list_cb_3d_points, list_cb_2d_img_points, gray.shape[::-1], None, None)

#print("Calibration Matrix: ")
#print(mtx)
#print("Distortion: ", dist)

# Find extrinsic parameters (Translation Vector, Rotation Matrix)
for i in range(len(list_cb_3d_points)):
    img_points = list_cb_2d_img_points[i]
    obj_points = list_cb_3d_points[i]
    ret, rvec, tvec = cv2.solvePnP(obj_points, img_points, mtx, dist)

    print(f"\nExtrinsic parameters for image {i+1}:")
    print("Rotation Vector:")
    print(rvec)
    print("Translation Vector:")
    print(tvec)

    # Convert rotation vector to rotation matrix
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    print("Rotation Matrix:")
    print(rotation_matrix)

    # Pose Estimation matrix (Transformation Matrix)
    pose_matrix = np.hstack((rotation_matrix, tvec))
    print("Transformation Matrix:")
    print(pose_matrix)

# Save the calibration matrix and distortion coefficients
with open('camera_cal.npy', 'wb') as f:
    np.save(f, mtx)
    np.save(f, dist)
