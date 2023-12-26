# Aerial Manipulator Project

## Camera Calibrations

### Step 1: Capture Chessboard Images
- Using the Raspberry Pi camera, capture a set of images of an 8x5, 28mm chessboard.
- Ensure various angles and distances are covered to achieve robust camera calibration.

### Step 2: Camera Calibration
- Use the captured images to calibrate the camera and obtain intrinsic and distortion matrices.
- Provide details of the intrinsic and distortion parameters in the README.

## Camera Calibration Parameters

### Intrinsic Matrix
The intrinsic matrix represents the internal parameters of the camera, essential for understanding the geometric properties of the image. It is defined as:
<div align="center">

| fx | 0  | cx |
|----|----|----|
| 0  | fy | cy |
| 0  | 0  | 1  |

</div>



Where:
- **fx**: Horizontal focal length
- **fy**: Vertical focal length
- **cx**: Horizontal principal point
- **cy**: Vertical principal point

### Distortion Coefficients
Distortion coefficients account for lens distortion in the camera. They are represented as a vector:
<div align="center">

| k1 | k2 | p1 | p2 | k3 |
|----|----|----|----|----|


</div>



Where:
- **k1, k2, k3**: Radial distortion coefficients
- **p1, p2**: Tangential distortion coefficients


### Step 3: ArUco Marker Detection
- Implement ArUco marker detection using the calibrated camera. 

### Step 4: Print 3D Coordinates
- Use the camera matrices to convert ArUco marker patterns into 3D coordinates.
- Display or print the details of the detected ArUco markers, including their 3D coordinates.
