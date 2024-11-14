from deepface import DeepFace

def classify_emotion(face_image):
    result = DeepFace.analyze(face_image, actions=['emotion'], enforce_detection=False)
    if isinstance(result, list):
        result = result[0]
    return result.get('dominant_emotion', 'Inconnu')
