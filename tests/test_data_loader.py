from pathlib import Path
import os
import cv2
import numpy as np

def load_dataset(dataset_path):
    """
    Charge les images et les labels depuis le dossier dataset_path.
    La structure attendue est :
        dataset_path/
            train/
                class_1/
                class_2/
                ...
            test/
                class_1/
                class_2/
                ...
    """
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Le chemin {dataset_path.resolve()} est introuvable.")

    data = []
    labels = []

    for split in ['train', 'test']:
        split_path = dataset_path / split
        if not split_path.exists():
            raise FileNotFoundError(f"Le chemin {split_path.resolve()} est introuvable.")

        for label in os.listdir(split_path):
            label_path = split_path / label
            if label_path.is_dir():
                for img_file in os.listdir(label_path):
                    img_path = label_path / img_file
                    try:
                        # Charger l'image en niveaux de gris
                        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            img_resized = cv2.resize(img, (48, 48))  # Redimensionner à 48x48
                            data.append(img_resized)
                            labels.append(label)
                    except Exception as e:
                        print(f"Erreur lors du chargement de l'image {img_path}: {e}")

    return np.array(data), np.array(labels)

def preprocess_data(data, labels):
    """
    Prétraite les données : normalisation et encodage des labels.
    """
    from sklearn.preprocessing import LabelEncoder
    from tensorflow.keras.utils import to_categorical

    # Normaliser les pixels entre 0 et 1
    data = data / 255.0

    # Encodage des labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)
    labels = to_categorical(labels)

    return data, labels, label_encoder

if __name__ == "__main__":
    dataset_path = "../data/fer-2013"  # Chemin vers le dataset
    try:
        # Charger les données
        data, labels = load_dataset(dataset_path)
        print(f"Données chargées avec succès : {len(data)} images.")
        print(f"Labels disponibles : {np.unique(labels)}")

        # Prétraiter les données
        data, labels, label_encoder = preprocess_data(data, labels)
        print("Prétraitement terminé.")
        print(f"Dimensions des données : {data.shape}")
        print(f"Classes des labels : {label_encoder.classes_}")
    except FileNotFoundError as e:
        print(e)