import tkinter as tk
from tkinter import filedialog
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity
from skimage.io import imread
import os
from PIL import ImageTk,Image
class App:
    def __init__(self, master):
        self.master = master
        master.title("Mesure de qualité d'image")

        # Créer les étiquettes
        self.mse_label = tk.Label(master, text="MSE : ", font=("Arial", 16))
        self.psnr_label = tk.Label(master, text="PSNR : ", font=("Arial", 16))
        self.ssim_label = tk.Label(master, text="SSIM : ", font=("Arial", 16))
        self.button = tk.Button(master,text="Calculer",command=self.calculer,width=25,background='orange',font=('Arial',14,'bold'))
       

        # Placer les étiquettes et le bouton dans la fenêtre
        self.mse_label.place(x=150, y=50)
        self.psnr_label.place(x=150, y=100)
        self.ssim_label.place(x=150, y=150)
        self.button.place(x=50,y=230)

         # Créer le bouton
       # self.button = tk.Button(master,text="Calculer",command=self.calculer,width=25,background='orange',font=('Arial',14,'bold')).pack(padx=20,pady=20)
        
    def calculer(self):
        # Demander à l'utilisateur de sélectionner les fichiers d'images
        img1_filename = 'img_original.jpg'
        img2_filename = 'restored.jpg'

        # Vérifier si les fichiers existent
        if not os.path.exists(img1_filename):
            print(f"Le fichier {img1_filename} n'existe pas.")
            return
        if not os.path.exists(img2_filename):
            print(f"Le fichier {img2_filename} n'existe pas.")
            return

        # Charger les images
        img1 = imread(img1_filename)
        img2 = imread(img2_filename)

        # Calculer le MSE
        mse = mean_squared_error(img1, img2)

        # Calculer le PSNR
        psnr = peak_signal_noise_ratio(img1, img2)

        # Calculer le SSIM avec une taille de fenêtre de 3x3
        ssim_value = structural_similarity(img1, img2, win_size=3, multichannel=True)

        # Afficher les résultats dans les étiquettes
        self.mse_label.config(text=f"MSE : {mse:.2f}")
        self.psnr_label.config(text=f"PSNR : {psnr:.2f}")
        self.ssim_label.config(text=f"SSIM : {ssim_value:.2f}")

# Créer la fenêtre Tkinter
root = tk.Tk()
largeur=400
hauteur=400
 # Chargement de l'image de fond
backround = Image.open("background1.png")
background_image = ImageTk.PhotoImage(backround)

# Création d'un Label pour afficher l'image de fond
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# Récupérer les dimensions de l'écran
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()
# Calculer les coordonnées de la fenêtre centrée
x = (largeur_ecran - largeur) // 2
y = (hauteur_ecran - hauteur) // 2

# Définir la géométrie de la fenêtre
root.geometry(f"{largeur}x{hauteur}+{x}+{y}")
# Créer l'application
app = App(root)

# Lancer la boucle principale Tkinter
root.mainloop()