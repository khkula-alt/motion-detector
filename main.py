import cv2  # for webcam and image processing
import time  # keeps track of the object's movement
import numpy as np # for math and distance calculations
import winsound  # for beep sound on Windows

# start video capture
cap = cv2.VideoCapture(0)                                         

# create background subtractor (to detect moving stuff)
fgbg = cv2.createBackgroundSubtractorMOG2()

# store last position and time for velocity calculation
last_center = None
last_time = None
speed_text = "Speed: 0 px/s"
alert_text = ""  # alert message

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply background subtraction
    mask = fgbg.apply(gray)

    # remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours of moving objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    alert_text = ""  # reset alert every frame
    motion_detected = False

    for cnt in contours:
        if cv2.contourArea(cnt) < 1000:  # ignore tiny movements
            continue

        motion_detected = True  # motion detected!

        # get bounding box
        (x, y, w, h) = cv2.boundingRect(cnt)
        center = (x + w // 2, y + h // 2)

        # colors (darker / royal style)
        box_color = (70, 70, 70)    # dark grey
        point_color = (90, 90, 120) # dark bluish grey

        # draw rectangle around moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
        cv2.circle(frame, center, 6, point_color, -1)

        # calculate velocity
        current_time = time.time()
        if last_center is not None and last_time is not None:
            dx = center[0] - last_center[0]
            dy = center[1] - last_center[1]
            distance = np.sqrt(dx**2 + dy**2)
            dt = current_time - last_time

            if dt > 0:
                speed = distance / dt  # pixels per second
                speed_text = f"Speed: {speed:.2f} px/s"
                # print speed in IDLE console
                print(speed_text)

        last_center = center
        last_time = current_time

    # alert if motion detected
    if motion_detected:
        alert_text = "MOTION DETECTED!"
        print(alert_text)
        # play beep sound (frequency=1000Hz, duration=300ms)
        winsound.Beep(1000, 300)

    # put speed text on video (always visible)
    cv2.putText(frame, speed_text, (20, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (150, 150, 180), 2)

    # put alert text if motion detected
    if alert_text:
        cv2.putText(frame, alert_text, (20, 80),
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 2)

    # Show windows
    cv2.imshow("Motion Detection", frame)
    cv2.imshow("Mask", mask)

    # exit on ESC key
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
