# Import necessary packages.
import cv2
import numpy as np
import keyboard
from tkinter import colorchooser
import time

# Define various colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255),
          (22, 22, 22), (0, 0, 0)]

penWidths = [14, 10, 6, 2]

# Select a default color
color = colors[0]

penWidth = penWidths[3]
widthIdx = 3

# Minimum allowed area for the contour
min_area = 1000

# Create videocapture object
cap = cv2.VideoCapture(0)

# Check success
if not cap.isOpened():
    raise Exception("Could not open video device")
# Set properties. Each returns === True on success (i.e. correct resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# Read picture. ret === True on success
ret, frame = cap.read()

width = int(cap.get(3))
height = int(cap.get(4))

# Create a blank canvas
canvas = np.zeros((height, width, 3), np.uint8)

# Color range for detecting green color
lower_bound = np.array([50, 80, 80])
upper_bound = np.array([80, 255, 255])

# Define a 10x10 kernel
kernel = np.ones((10, 10), np.uint8)

previous_center_point = 0

# To write or not to write

is_writing = False

while True:

    # Read each frame from webcam
    success, frame = cap.read()

    # Flip the frame
    frame = cv2.flip(frame, 1)

    # Convert the frame BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a binary segmented mask of green color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Add some dialation to increase segmented area
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find all the contours of the segmented mask
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Checking if any contour is detected then run the following statements
    if len(contours) > 0:
        # Get the biggest contour from all the detected contours
        cmax = max(contours, key=cv2.contourArea)

        # Find the area of the contour
        area = cv2.contourArea(cmax)
        # print(area)

        # Checking whether or not to write
        if keyboard.is_pressed("w"):
            time.sleep(0.08)
            is_writing = ~is_writing

        # Checking if the area of the contour is greater than a threshold
        if area > min_area:

            # Find center point of the contour
            M = cv2.moments(cmax)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Selecting the color for drawing in the canvas
            if previous_center_point == 0:
                if 12 < cX < 90:
                    # Clear all
                    if 12 < cY < 45:
                        canvas = np.zeros((height, width, 3), np.uint8)
                        # color = cv2.circle(frame, (cX, cY), 3, (255,255,255) )
                    elif 375 < cY < 407:
                        color = colors[8]

                if 19.5 < cX < 39.5:
                    if 75 < cY < 95:
                        color = colors[0]

                    elif 145 < cY < 165:
                        color = colors[2]

                    elif 215 < cY < 235:
                        color = colors[4]

                    elif 285 < cY < 305:
                        color = colors[6]

                if 42.5 < cX < 82.5:
                    if 110 < cY < 130:
                        color = colors[1]

                    elif 170 < cY < 200:
                        color = colors[3]

                    elif 250 < cY < 270:
                        color = colors[5]

                    elif 320 < cY < 340:
                        color = colors[7]

                if 14 < cY < 44:
                    if 120 < cX < 150:
                        penWidth = penWidths[0]
                        widthIdx = 0

                    elif 165 < cX < 195:
                        penWidth = penWidths[1]
                        widthIdx = 1

                    elif 210 < cX < 240:
                        penWidth = penWidths[2]
                        widthIdx = 2

                    elif 255 < cX < 285:
                        penWidth = penWidths[3]
                        widthIdx = 3

            # If drawing is started then draw a line between each frames detected contour center point
            if previous_center_point != 0 and is_writing:
                # print(previous_center_point)

                cv2.line(canvas, previous_center_point, (cX, cY), color, penWidth)

            # Update the center point
            previous_center_point = (cX, cY)

        else:
            previous_center_point = 0

    # Changing Colors using keyboard
    if keyboard.is_pressed("1"):
        color = colors[0]
    elif keyboard.is_pressed("2"):
        color = colors[1]
    elif keyboard.is_pressed("3"):
        color = colors[2]
    elif keyboard.is_pressed("4"):
        color = colors[3]
    elif keyboard.is_pressed("5"):
        color = colors[4]
    elif keyboard.is_pressed("6"):
        color = colors[5]
    elif keyboard.is_pressed("7"):
        color = colors[6]
    elif keyboard.is_pressed("8"):
        color = colors[7]
    elif keyboard.is_pressed("9"):
        color = colors[8]

    # Changing widths using keyboard

    try:
        if keyboard.is_pressed("l") and penWidth < 20:
            penWidth += 2

        elif keyboard.is_pressed("j") and penWidth > 2:
            penWidth -= 2

        elif keyboard.is_pressed("i") and widthIdx > 0:
            time.sleep(0.08)
            widthIdx -= 1
            penWidth = penWidths[widthIdx]

        elif keyboard.is_pressed("k") and widthIdx < 3:
            time.sleep(0.08)
            widthIdx += 1
            penWidth = penWidths[widthIdx]
    except:
        penWidth = penWidths[3]

    # Clear function
    if keyboard.is_pressed("c"):
        canvas = np.zeros((height, width, 3), np.uint8)

    if keyboard.is_pressed("g") and color != colors[8]:
        index = colors.index(color)
        if (index != 9):
            color = list(colorchooser.askcolor()[0])
            color[0], color[2] = color[2], color[0]
            colors[index] = color

    # Adding the canvas mask to the original frame
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, canvas_binary = cv2.threshold(canvas_gray, 20, 255, cv2.THRESH_BINARY_INV)

    canvas_binary = cv2.cvtColor(canvas_binary, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, canvas_binary)
    frame = cv2.bitwise_or(frame, canvas)

    # pannel
    cv2.rectangle(frame, pt1=(0, 0), pt2=(102, 550), color=(140, 140, 140), thickness=-1)
    cv2.rectangle(frame, pt1=(0, 0), pt2=(300, 60), color=(140, 140, 140), thickness=-1)
    cv2.polylines(frame, [np.array([[0, 0], [0, 550],
                                    [102, 550], [102, 60],
                                    [300, 60], [300, 0]],
                                   np.int32)],
                  True, (0, 0, 0), 2)

    # trying polygon
    cv2.fillPoly(frame, [np.array([[19.5, 75], [19.5, 95],
                                   [39.5, 107], [59.5, 95],
                                   [59.5, 75], [39.5, 63]],
                                  np.int32)],
                 colors[0])

    cv2.fillPoly(frame, [np.array([[42.5, 110], [42.5, 130],
                                   [62.5, 142], [82.5, 130],
                                   [82.5, 110], [62.5, 98]],
                                  np.int32)],
                 colors[1])

    cv2.fillPoly(frame, [np.array([[19.5, 145], [19.5, 165],
                                   [39.5, 177], [59.5, 165],
                                   [59.5, 145], [39.5, 133]],
                                  np.int32)],
                 colors[2])

    cv2.fillPoly(frame, [np.array([[42.5, 180], [42.5, 200],
                                   [62.5, 212], [82.5, 200],
                                   [82.5, 180], [62.5, 168]],
                                  np.int32)],
                 colors[3])

    cv2.fillPoly(frame, [np.array([[19.5, 215], [19.5, 235],
                                   [39.5, 247], [59.5, 235],
                                   [59.5, 215], [39.5, 203]],
                                  np.int32)],
                 colors[4])

    cv2.fillPoly(frame, [np.array([[42.5, 250], [42.5, 270],
                                   [62.5, 282], [82.5, 270],
                                   [82.5, 250], [62.5, 238]],
                                  np.int32)],
                 colors[5])

    cv2.fillPoly(frame, [np.array([[19.5, 285], [19.5, 305],
                                   [39.5, 317], [59.5, 305],
                                   [59.5, 285], [39.5, 273]],
                                  np.int32)],
                 colors[6])

    cv2.fillPoly(frame, [np.array([[42.5, 320], [42.5, 340],
                                   [62.5, 352], [82.5, 340],
                                   [82.5, 320], [62.5, 308]],
                                  np.int32)],
                 colors[7])

    cv2.fillPoly(frame, [np.array([[31, 493], [31, 513],
                                   [51, 525], [71, 513],
                                   [71, 493], [51, 481]],
                                  np.int32)],
                 color)

    cv2.circle(frame, [135, 29], 8, [255, 255, 255], -1)
    cv2.circle(frame, [180, 29], 6, [255, 255, 255], -1)
    cv2.circle(frame, [225, 29], 4, [255, 255, 255], -1)
    cv2.circle(frame, [270, 29], 2, [255, 255, 255], -1)
    cv2.circle(frame, [1225, 50], penWidth, color, -1)
    cv2.circle(frame, [1224, 50], penWidth, [180, 180, 180], 2)
    cv2.circle(frame, [1224, 50], penWidth - 1, [0, 0, 0], 1)

    cv2.rectangle(frame, pt1=(12, 13), pt2=(90, 45), color=(50, 50, 50), thickness=-1)
    cv2.rectangle(frame, pt1=(120, 14), pt2=(150, 44), color=(50, 50, 50), thickness=2)
    cv2.rectangle(frame, pt1=(165, 14), pt2=(195, 44), color=(50, 50, 50), thickness=2)
    cv2.rectangle(frame, pt1=(210, 14), pt2=(240, 44), color=(50, 50, 50), thickness=2)
    cv2.rectangle(frame, pt1=(255, 14), pt2=(285, 44), color=(50, 50, 50), thickness=2)
    cv2.rectangle(frame, pt1=(12, 375), pt2=(90, 407), color=(50, 50, 50), thickness=-1)
    cv2.rectangle(frame, pt1=(5, 430), pt2=(97, 470), color=(243, 245, 208), thickness=-1)

    # Adding the text buttons to the live frame for colour access
    cv2.putText(frame, "CLEAR ALL", (18, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.39, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "ERASER", (29, 395), cv2.FONT_HERSHEY_SIMPLEX, 0.39, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Current Color", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.39, (35, 35, 35), 2, cv2.LINE_AA)

    # Checking if any contour is detected then run the following statements
    if len(contours) > 0:

        # Checking if the area of the contour is greater than a threshold
        if area > min_area:

            # Drawing a circle in the center of the contour area
            if penWidth % 2 == 0:
                circRadius = penWidth / 2
            elif penWidth % 2 == 1:
                circRadius = (penWidth + 1) / 2

            cv2.circle(frame, (cX, cY), (penWidth), (0, 0, 255), 2)

    # Show the frame to a new OpenCV window
    cv2.imshow('Canvas', canvas)
    cv2.imshow("Frame", frame)
    # cv2.imshow("mask", mask)


    # Open the OpenCV window until 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
