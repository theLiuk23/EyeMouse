import cv2
import numpy

class Eyes:
    def __init__(self):
        self.gray = None
        self.mini_gray = None
        self.mini_frame = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.eyes = None
        

    def detect_pupils_center(self, frame):
        self.eyes = self.get_eyes(frame)
        result = []

        for eye in self.eyes:
            x, y, w, h = eye
            center = int(abs(x + w / 2)), int(abs(y + h / 2))
            radius = int(abs(w / 6))
            cv2.circle(self.mini_frame, center, radius, (255, 0, 0))
            result.append((w, h))

        return result


    def detect_eyes_rect(self, frame):
        self.eyes = self.get_eyes(frame)
        
        result = []
        for eye in self.eyes:
            ex,ey,ew,eh = eye
            cv2.rectangle(self.mini_frame, (ex, ey), (ex+ew,ey+eh), (0,225,255), 2)
            result.append((ew, eh))
        
        return result


    def get_eyes(self, frame):
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        
        result = []
        for (x, y, w, h) in faces:
            self.mini_gray = self.gray[y:y+w, x:x+w]
            self.mini_frame = frame[y:y+h, x:x+w]
            result.append(self.eye_cascade.detectMultiScale(self.mini_gray, 1.3, 5))
        
        return result[0] if len(result) != 0 else []


    def get_pupils_position(self, frame):
        eyes = self.detect_eyes_rect(frame)
        pupils = self.detect_pupils_center(frame)

        if len(eyes) != 2 or len(pupils) != 2:
            return

        rel_points = []
        for i in range(2):
            x = pupils[i][0] / eyes[i][0]
            y = pupils[i][1] / eyes[i][1]
            if x > 1 or y > 1:
                continue
            rel_points.append((x, y))

        return rel_points