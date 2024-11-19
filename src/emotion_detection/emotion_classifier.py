from deepface import DeepFace


def classify_emotion(face_img):
    result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
    emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
    return emotion