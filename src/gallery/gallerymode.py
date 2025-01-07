import os
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from src.detection.face_detection import detect_faces
from src.emotion_detection.emotion_classifier import classify_emotion


class GalleryApp:
    def __init__(self, root, app_instance):
        self.root = root
        self.app_instance = app_instance
        self.root.title("Galerie d'Images")
        self.root.geometry("800x700")
        self.root.configure(bg="#6343a7")

        # Label pour afficher l'image
        self.image_label = tk.Label(root, bg="#6343a7")
        self.image_label.pack(pady=20)

        # Dossier des images
        self.images_folder = "./data/assets/face"
        self.image_list = [f for f in os.listdir(self.images_folder) if f.endswith(('jpg', 'png'))]
        self.current_image_index = 0

        # Boutons de navigation et d'analyse
        self.controls_frame = tk.Frame(root, bg="#6343a7")
        self.controls_frame.pack(pady=10)

        btn_prev = tk.Button(self.controls_frame, text="Image Précédente", command=self.show_prev_image,
                             font=("Helvetica", 10), bg="#3c2e6f", fg="white", width=15)
        btn_prev.grid(row=0, column=0, padx=10)

        self.analyze_button = tk.Button(self.controls_frame, text="Analyser l'Image", command=self.analyze_image,
                                        font=("Helvetica", 12), bg="#3c2e6f", fg="white", width=15)
        self.analyze_button.grid(row=0, column=1, padx=10)

        btn_next = tk.Button(self.controls_frame, text="Image Suivante", command=self.show_next_image,
                             font=("Helvetica", 10), bg="#3c2e6f", fg="white", width=15)
        btn_next.grid(row=0, column=2, padx=10)

        btn_quit = tk.Button(root, text="Retour au menu", command=self.stop_gallery, font=("Helvetica", 12),
                             bg="#3c2e6f", fg="white", width=15)
        btn_quit.pack(pady=10)

        # Label pour afficher le résultat de l'analyse
        self.result_label = tk.Label(root, font=("Helvetica", 12), bg="#6343a7", fg="white", text="")
        self.result_label.pack(pady=20)

        self.show_image()

    def show_image(self):
        """Affiche l'image courante dans le label."""
        img_path = os.path.join(self.images_folder, self.image_list[self.current_image_index])
        img = Image.open(img_path)
        img = img.resize((400, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        self.image_label.imgtk = img_tk
        self.image_label.configure(image=img_tk)
        self.result_label.config(text="")  # Réinitialiser le texte du résultat

    def show_next_image(self):
        """Affiche l'image suivante dans la liste."""
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.show_image()

    def show_prev_image(self):
        """Affiche l'image précédente dans la liste."""
        self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
        self.show_image()

    def analyze_image(self):
        """Analyse l'émotion de l'image courante."""
        img_path = os.path.join(self.images_folder, self.image_list[self.current_image_index])
        img = Image.open(img_path)
        img = img.resize((150, 150))
        img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        faces = detect_faces(img_array)
        if len(faces) > 0:  # Correction pour vérifier s'il y a au moins un visage détecté
            x, y, w, h = faces[0]
            face_img = img_array[y:y + h, x:x + w]
            emotion = classify_emotion(face_img)
            result_text = f"Émotion : {emotion}"
        else:
            result_text = "Aucun visage détecté"

        # Afficher le résultat de l'analyse dans le label
        self.result_label.config(text=result_text)

    def stop_gallery(self):
        """Ferme la galerie et retourne au menu principal."""
        self.root.destroy()
        self.app_instance.show_menu()


def launch_gallery_mode(app_instance):
    """Lance le mode galerie dans une nouvelle fenêtre."""
    gallery_window = tk.Toplevel()
    GalleryApp(gallery_window, app_instance)
