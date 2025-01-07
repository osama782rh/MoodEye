import os
import cv2


def load_images(folder_path):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Vérifie les formats d'image
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images[filename] = img
            else:
                print(f"Impossible de charger l'image : {img_path}")
    return images
