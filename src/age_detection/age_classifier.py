from deepface import DeepFace

def estimate_age(face_img):
    result = DeepFace.analyze(face_img, actions=['age'], enforce_detection=False)
    age = result[0]['age'] if isinstance(result, list) else result['age']
    return age
