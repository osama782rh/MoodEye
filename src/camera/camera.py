import cv2
from src.detection.face_detection import detect_faces
from src.emotion_detection.emotion_classifier import classify_emotion
import tkinter as tk
from PIL import Image, ImageTk


class CameraApp:
    def __init__(self, root, app_instance):
        self.root = root
        self.app_instance = app_instance
        self.root.title("Emotions Detection")
        self.root.geometry("800x600")

        # Label pour afficher la vidéo
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Bouton pour quitter la caméra et revenir au menu
        self.quit_button = tk.Button(root, text="Retour au menu", command=self.stop_camera)
        self.quit_button.pack(pady=10)

        # Initialiser la caméra
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erreur : Impossible d'accéder à la caméra.")
            self.stop_camera()
            return

        self.update_frame()

    def update_frame(self):
        """Capture une image de la caméra et l'affiche dans le label."""
        ret, frame = self.cap.read()
        if not ret:
            self.stop_camera()
            return

        # Détecter les visages et les émotions
        faces = detect_faces(frame)
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            emotion = classify_emotion(face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        # Convertir l'image en format compatible avec tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        # Afficher l'image dans le label
        self.video_label.imgtk = img_tk
        self.video_label.configure(image=img_tk)

        # Rafraîchir l'image après 10 ms
        self.root.after(10, self.update_frame)

    def stop_camera(self):
        """Ferme la caméra et retourne au menu principal."""
        self.cap.release()
        self.root.destroy()
        self.app_instance.show_menu()


def launch_camera_mode(app_instance):
    """Lance le mode caméra dans une nouvelle fenêtre."""
    camera_window = tk.Toplevel()
    CameraApp(camera_window, app_instance)
