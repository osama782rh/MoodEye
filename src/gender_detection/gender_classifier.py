from deepface import DeepFace

def determine_gender(face_img):
    result = DeepFace.analyze(face_img, actions=['gender'], enforce_detection=False)
    gender = result[0]['gender'] if isinstance(result, list) else result['gender']
    return "Homme" if gender == "Man" else "Femme"
