# Object Detection Criteria

## Color Detection

1. **Calibration Stage:**
   - Identify the color of the known object through a calibration process.

2. **Color Range Track Bars:**
   - Define track bars to set the color range for object detection.

3. **Image Processing:**
   - Load the image.
   - Convert the image to the HSV color space using `cv2.COLOR_BGR2HSV`.
   - Utilize HSV color space for its broader range of colors.

4. **Color Filtering:**
   - Use `cv2.inRange` to filter a specific color range.
   - Extract specific bitplanes from the image using `cv2.bitwise_and`.

## Distance Detection

1. **Successful Object Detection:**
   - Achieve accurate object detection based on color, size, and distance.

2. **Distance Measurement:**
   - Measure the distance between the detected object (known object) and the Raspberry Pi camera.

3. **Width Calculation:**
   - Measure the width of the detected object (known object).

4. **Focal Length Calculation:**
   - Calculate the focal length of the camera using the formula: `F = (P X D) / W`, where:
     - `F` is the focal length,
     - `P` is the apparent width of the object in pixels,
     - `D` is the actual distance between the object and the camera,
     - `W` is the actual width of the object.

5. **Object Distance Calculation:**
   - Utilize the calculated focal length in the triangle similarity method to determine the object's distance.

By following these steps, the system should effectively detect known objects based on their color, size, and distance, providing a comprehensive solution for object detection criteria.
