Motion Detector 🚨


a Python project for real-time motion detection using a webcam with alert functionality.
detects movement, calculates object speed, and triggers a beep alert when motion is detected.


Features

detects motion in real-time using a webcam

calculates object speed in pixels per second

alerts user with a beep sound when motion is detected

displays live video feed with bounding boxes and speed overlay


Installation

1.clone the repository:
git clone https://github.com/your-username/motion-detector.git

2.navigate to the project folder:
cd motion-detector

3.install dependencies:
pip install opencv-python numpy

⚠ Note: winsound is included in Windows by default.



Usage

run the main Python file:
python main.py
press ESC to exit the program.
the video feed window will show detected motion, object speed, and alerts when motion is detected.


Code Snippet

here’s a quick example of how motion is detected:

```python
import cv2
import time
import numpy as np
import winsound

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
last_center = None
last_time = None

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = fgbg.apply(gray)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 1000:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        center = (x + w // 2, y + h // 2)
        if last_center:
            dx, dy = center[0]-last_center[0], center[1]-last_center[1]
            speed = np.sqrt(dx**2 + dy**2)/(time.time()-last_time)
            print(f"Speed: {speed:.2f} px/s")
        last_center = center
        last_time = time.time()
        winsound.Beep(1000, 300)  # alert
```




Run the full code in [main.py](main.py)



Contributing

Ccontributions are welcome! feel free to submit pull requests or issues to improve this project.


License

this project is licensed under the MIT License.


