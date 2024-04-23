import numpy as np
import cv2
import time
# Number of chessboard corners (inner points)
num_x = 9 # Number of inner corners along the x-axis
num_y = 6 # Number of inner corners along the y-axis

# Create a VideoCapture object
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the frame
    cv2.imshow('Chessboard', frame)

    # Check for key press
    key = cv2.waitKey(1) & 0xFF

    # If 's' is pressed, save the image
    if key == ord('s'):
        # Save the image with a unique name
        filename = f'grasping/log/calibration_image_{int(time.time())}.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image {filename} saved")

    # Break the loop if the ESC key is pressed
    elif key == 27:
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
