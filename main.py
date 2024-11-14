import tkinter as tk
from PIL import Image, ImageTk
from src.camera.camera import launch_camera_mode
from src.gallery.gallerymode import launch_gallery_mode


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
        self.root.geometry("400x500")
        self.root.configure(bg="#6343a7")

        # Ajouter le logo
        logo_path = "./data/assets/img.png"
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((150, 150), Image.LANCZOS)
            tk_logo = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.root, image=tk_logo, bg="#6343a7")
            logo_label.image = tk_logo  # Conserver une référence pour éviter le garbage collection
            logo_label.pack(pady=10)
        except Exception as e:
            print("Erreur lors du chargement du logo:", e)

        # Titre et boutons
        title = tk.Label(self.root, text="MoodEye", font=("Helvetica", 24), bg="#6343a7", fg="white")
        title.pack(pady=20)

        btn_camera = tk.Button(self.root, text="Caméra", command=self.start_camera_mode, font=("Helvetica", 16),
                               bg="#3c2e6f", fg="white", width=15)
        btn_camera.pack(pady=10)

        btn_gallery = tk.Button(self.root, text="Galerie", command=self.start_gallery_mode, font=("Helvetica", 16),
                                bg="#3c2e6f", fg="white", width=15)
        btn_gallery.pack(pady=10)

    def start_camera_mode(self):
        """Lancer le mode caméra pour détecter les émotions en direct."""
        launch_camera_mode(self)

    def start_gallery_mode(self):
        """Lancer le mode galerie pour sélectionner et analyser des images."""
        launch_gallery_mode(self)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
