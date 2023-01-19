from eyes import Eyes
import mouse
import mediapipe
import cv2
import time, sys


webcam = cv2.VideoCapture(0)
eyes = Eyes()
my_mouse = mouse.Mouse()


def calibrate(left_or_right:str):
    print(f"Watch the {left_or_right} side of your screen")
    time.sleep(2)
    _, frame = webcam.read()
    detection = eyes.detect_pupils(frame)
    print(detection["ellipse"]["angle"], detection["confidence"])
    if detection["confidence"] < 0.70:
        calibrate(left_or_right)
    return detection["ellipse"]["angle"]


# left_angle = calibrate("left")
# right_angle = calibrate("right")


while True:
    _, frame = webcam.read()
    result = eyes.get_pupils_position(frame)

    if not result:
        continue

    x, y = result[0]
    my_mouse.move_mouse(x, y)
        
    # cv2.imshow("Test", frame)
    # time.sleep(1/20)

    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()
webcam.release()
sys.exit(0)