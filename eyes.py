import cv2
import mediapipe as mp
import math

class Eyes:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.frame_h, self.frame_w, _ = None, None, None
        self.landmark_points = None


    def get_landmarks(self, frame):
        self.frame_h, self.frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = self.face_mesh.process(rgb_frame)
        self.landmark_points = output.multi_face_landmarks


    def detect_left_eye(self, frame) -> list[tuple[float]] | None:
        self.get_landmarks(frame)
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            for landmark in [landmarks[463], landmarks[466], landmarks[258], landmarks[253]]: # [landmarks[463], landmarks[466], landmarks[385], landmarks[253]]: # [landmarks[463], landmarks[466], landmarks[444]]: # 450:469 # [landmarks[463], landmarks[466], landmarks[385], landmarks[253]]
                x = int(landmark.x * self.frame_w)
                y = int(landmark.y * self.frame_h)
                cv2.circle(frame, (x, y), 1, (255, 0, 0))
            return [landmarks[463], landmarks[466], landmarks[258], landmarks[253]]
        return None

    
    def detect_right_eye(self, frame) -> list[tuple[float]] | None:
        self.get_landmarks(frame)
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            for landmark in [landmarks[173], landmarks[226], landmarks[27], landmarks[23]]: # [landmarks[463], landmarks[466], landmarks[444]]: # 450:469 # [landmarks[463], landmarks[466], landmarks[385], landmarks[253]]
                x = int(landmark.x * self.frame_w)
                y = int(landmark.y * self.frame_h)
                cv2.circle(frame, (x, y), 1, (255, 0, 0))
            return [landmarks[173], landmarks[223], landmarks[27], landmarks[23]]
        return None


    def detect_left_pupil(self, frame) -> tuple[float] | None:
        self.get_landmarks(frame)
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            pupil = landmarks[473]
            x = int(pupil.x * self.frame_w)
            y = int(pupil.y * self.frame_h)
            cv2.circle(frame, (x, y), 1, (0, 255, 0))
            return (pupil.x, pupil.y)
        return None


    def detect_right_pupil(self, frame) -> tuple[float] | None:
        self.get_landmarks(frame)
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            pupil = landmarks[468]
            x = int(pupil.x * self.frame_w)
            y = int(pupil.y * self.frame_h)
            cv2.circle(frame, (x, y), 1, (0, 255, 0))
            return (pupil.x, pupil.y)
        return None


    def detect_nose(self, frame) -> tuple[int] | None:
        self.get_landmarks(frame)
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            nose = landmarks[195]
            x = int(nose.x * self.frame_w)
            y = int(nose.y * self.frame_h)
            cv2.circle(frame, (x, y), 1, (0, 255, 0))
            return (nose.x, nose.y)
        return None





    def get_pupils_position(self, frame) -> tuple(float) | None:
        pupil1, pupil2 = self.detect_left_pupil(frame), self.detect_right_pupil(frame)
        eye1, eye2 = self.detect_left_eye(frame), self.detect_right_eye(frame)
        if None in [pupil1, pupil2, eye1, eye2]: return None

        return (0, 0)



    def get_eyes_distance(self, frame) -> int | None:
        l_pupil = self.detect_left_pupil(frame)
        r_pupil = self.detect_right_pupil(frame)
        nose = self.detect_nose(frame)

        if None in [nose, l_pupil, r_pupil]:
            return None

        is_right = abs(r_pupil[0] - nose[0]) < abs(l_pupil[0] - nose[0])
        distance = math.sqrt((r_pupil[0] - l_pupil[0])**2 + (r_pupil[1] - l_pupil[1])**2)

        if is_right:
            return 1/distance
        else:
            return -1/distance