import cv2
import mediapipe as mp

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


    def detect_eye(self, frame) -> list[tuple[int]]:
        self.get_landmarks(frame)
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            for landmark in landmarks[474:478]:
                x = int(landmark.x * self.frame_w)
                y = int(landmark.y * self.frame_h)
                cv2.ellipse(frame, self.detect_pupil(frame)) # TODO
            return landmarks[474:478]


    def detect_pupil(self, frame) -> tuple[int] | None:
        if self.landmark_points:
            landmarks = self.landmark_points[0].landmark
            landmark = landmarks[473]
            x = int(landmark.x * self.frame_w)
            y = int(landmark.y * self.frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            return (x, y)
        return None


    def detect_head_movement(self) -> tuple[int]:
        if self.x is None or self.y is None:
            return None
        if self.frame_h is None or self.frame_w is None:
            raise Exception("Frame has no shape!")

        res_x = 3460 - (self.x / self.frame_w * 3460)
        res_y = self.y / self.frame_h * 1080
        return (res_x, res_y)
