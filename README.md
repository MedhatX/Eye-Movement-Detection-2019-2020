# Eye-Movement-Detection-(2019-2020)
This project demonstrates eye movement detection and eye blinking using Python and OpenCV. By leveraging computer vision techniques, we can detect the direction of eye movement and blinking. The primary goal of this code is to enable control of automated systems, such as wheelchairs, through eye movement, paving the way for hands-free control in various applications.

## Acknowledgements
This code is inspired by the tutorials and resources available on PySource: https://pysource.com/

## Features
- Detects faces using Dlib's pre-trained facial landmark detector.
- Tracks eye movements and processes images of the eyes.
- Adjusts brightness and contrast dynamically using trackbars.
- Determines eye position (Left, Right, Center) based on detected movement.
- Counts blink events to toggle between motion detection and a stop state.
  
## Requirements
1. pyhton > 3.0
2. python libraries
- cv2
- Numpy
- dlib
- math
3. shape_predictor_68_face_landmarks.dat file from (https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat)
4. a webcam to start capturing

## How to use it
1. Start moving your eyes left and right, and you will see the detected direction displayed on the screen.
2. Blink your eyes for about 2 seconds. The program will stop detecting eye movements during this time.
3. Re-blink your eyes for another 2 seconds to resume detection. 

## How It Works
1. Captures a video feed from the webcam.
2. Detects the face using Dlib's face detector.
3. Extracts eye regions and applies contrast/brightness adjustments.
4. Processes the eye region to determine pupil position.
5. Uses blinking patterns to toggle motion detection.
6. Displays the direction of the gaze and detects when blinking stops the motion.

## Output:
- The main window will display the video feed with detected eyes and movement directions.
- Another window will show the processed eye image and thresholded binary image for better visualization.


