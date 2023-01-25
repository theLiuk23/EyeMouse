from eyes import Eyes
import mouse
import cv2
import time, sys


FPS = 5
MOUSE_SMOOTHNESS = FPS
webcam = cv2.VideoCapture(0)
eyes = Eyes()
my_mouse = mouse.Mouse(MOUSE_SMOOTHNESS)

  
while True:
    _, frame = webcam.read()
    l_eye = eyes.detect_left_eye(frame)
    r_eye = eyes.detect_right_eye(frame)
    l_pupil = eyes.detect_left_pupil(frame)
    r_pupil = eyes.detect_right_pupil(frame)

    if l_eye is None or r_eye is None or l_pupil is None or r_pupil is None:
        continue

    cv2.flip(frame, 0)
    # my_mouse.move_mouse(eye, pupil)    
    
    cv2.imshow("Test", frame)
    time.sleep(1/FPS)

    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()
webcam.release()
sys.exit(0)