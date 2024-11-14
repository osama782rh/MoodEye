import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Charger le dataset FER-2013
data_path = "data/fer2013.csv"
data = pd.read_csv(data_path)


# Prétraitement des données
def preprocess_data(data):
    X = []
    y = []
    for index, row in data.iterrows():
        pixels = np.array(row['pixels'].split(), dtype="float32")
        pixels = pixels.reshape(48, 48, 1) / 255.0  # Normalisation
        X.append(pixels)
        y.append(row['emotion'])

    X = np.array(X)
    y = to_categorical(y, num_classes=7)  # 7 classes d'émotions dans FER-2013
    return X, y


X, y = preprocess_data(data)

# Séparer en ensembles d'entraînement et de validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)


# Définir le modèle de détection d'émotions
def build_emotion_model(input_shape=(48, 48, 1), num_classes=7):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


model = build_emotion_model()

# Entraîner le modèle
epochs = 30
batch_size = 64
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)

# Sauvegarder le modèle entraîné
model.save("data/emotion_model.h5")
print("Modèle sauvegardé sous data/emotion_model.h5")
