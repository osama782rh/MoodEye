import dlib
import cv2

predictor_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


def detect_keypoints(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    keypoints = []
    for face in faces:
        landmarks = predictor(gray, face)
        points = [(p.x, p.y) for p in landmarks.parts()]
        keypoints.append(points)
    return keypoints