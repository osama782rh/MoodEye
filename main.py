import os
import cv2
import numpy as np
from src.preprocessing.data_loader import load_images
from src.detection.face_detection import detect_faces
from src.emotion_detection.emotion_classifier import classify_emotion


def process_images_in_folder(folder_path, grid_size=(4, 6), image_size=(150, 150)):
    images = load_images(folder_path)
    annotated_images = []

    for img_name, img in images.items():
        faces = detect_faces(img)
        if len(faces) == 0:
            print(f"Aucun visage détecté dans l'image : {img_name}")
            continue

        for (x, y, w, h) in faces:
            face_img = img[y:y + h, x:x + w]
            emotion = classify_emotion(face_img)

            # Dessiner le cadre et afficher l'émotion
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        # Redimensionner chaque image pour l'ajouter à la grille
        img_resized = cv2.resize(img, image_size)
        annotated_images.append(img_resized)

    # Construire la mosaïque d'images
    display_images_grid(annotated_images, grid_size, image_size)


def display_images_grid(images, grid_size, image_size):
    rows, cols = grid_size
    grid_img = np.zeros((rows * image_size[1], cols * image_size[0], 3), dtype=np.uint8)

    for idx, img in enumerate(images):
        if idx >= rows * cols:
            break
        row = idx // cols
        col = idx % cols
        x_offset = col * image_size[0]
        y_offset = row * image_size[1]
        grid_img[y_offset:y_offset + image_size[1], x_offset:x_offset + image_size[0]] = img

    cv2.imshow("Mosaic of Emotion Detection", grid_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    folder_path = './data/assets/face/'
    process_images_in_folder(folder_path)
