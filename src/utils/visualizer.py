# src/utils/visualizer.py
import cv2

def show_image_with_emotion(image, emotion_text):
    """Affiche une image avec l'émotion en texte."""
    cv2.putText(image, f"Emotion: {emotion_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Emotion Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
