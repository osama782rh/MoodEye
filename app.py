import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from src.detection.face_detection import detect_faces
from src.emotion_detection.emotion_classifier import classify_emotion


class CameraApp:
    def __init__(self, root, app_instance):
        self.root = root
        self.app_instance = app_instance
        self.root.title("Emotions Detection")
        self.root.geometry("800x600")

        # Label pour afficher la vidéo
        self.video_label = Label(root)
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


def detect_emotions_webcam(app_instance):
    """Lancer l'interface de la caméra avec l'analyse des émotions."""
    camera_window = tk.Toplevel()
    CameraApp(camera_window, app_instance)


# Exemple d'utilisation dans une application principale
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MoodEye")
        self.show_menu()

    def show_menu(self):
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()

        # Interface du menu principal
        self.root.geometry("400x300")
        self.root.configure(bg="#6343a7")

        # Titre et boutons
        title = tk.Label(self.root, text="MoodEye", font=("Helvetica", 24), bg="#6343a7", fg="white")
        title.pack(pady=20)

        btn_camera = tk.Button(self.root, text="Caméra", command=self.start_camera_mode, font=("Helvetica", 16),
                               bg="#3c2e6f", fg="white", width=15)
        btn_camera.pack(pady=10)

        btn_gallery = tk.Button(self.root, text="Galerie", font=("Helvetica", 16), bg="#3c2e6f", fg="white", width=15)
        btn_gallery.pack(pady=10)

    def start_camera_mode(self):
        detect_emotions_webcam(self)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
