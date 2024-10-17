import dwt_compression as dwt
import aes as aes
import matplotlib.pyplot as plt
from tkinter import *
from PIL import ImageTk,Image
import tkinter.filedialog as tf
import warnings
import cv2
import numpy as np
import os
warnings.filterwarnings('ignore')

def get_image():
        file = tf.askopenfilename(title="Choose Images", filetypes=(
        ("jpeg files", "*.jpg"), ("png files", "*.png")))
        img = ImageTk.PhotoImage(Image.open(file,'r'))
        image_label.config(image=img)
        image_label.image = img
        img_var.set(file)


def encrypt_image():
        compressed_image = dwt.compress(img_var.get())
        encrypted_image = aes.encrypt(compressed_image)
        img = ImageTk.PhotoImage(Image.open(encrypted_image,'r'))
        image_label.config(image=img)
        image_label.image = img
        img_var.set(encrypted_image)




def decrypt_image():
        decrypted_image = aes.decrypt(img_var.get())
        decompressed_image = dwt.decompress(decrypted_image)
        img = ImageTk.PhotoImage(Image.open(decompressed_image,'r'))
        image_label.config(image=img)
        image_label.image = img
        img_var.set(decompressed_image)

def afficher_histogramme():
    # Convertir l'image en niveaux de gris
    image1 = Image.open(img_var.get())
    image_gris = image1.convert("L")

    #changer nom fenetre de histogramme
    plt.figure("l'histogramme")
    
    # Calculer l'histogramme
    histogramme = np.histogram(image_gris, bins=256, range=[0, 256])[0]

    # Afficher l'histogramme
    plt.bar(range(256), histogramme)
    plt.show()

# Fonction appelée lors du clic sur le bouton "Mesurqualite"
def Mesurqualite():
    os.system('python Mesurqualite.py')
    #----------------------------------------------------------------------------------------------------------
root=Tk()
root.title("mini-projet")
 # Chargement de l'image de fond
backround = Image.open("C://Users//aitichou//Desktop//securitev1//background1.png")
background_image = ImageTk.PhotoImage(backround)

# Création d'un Label pour afficher l'image de fond
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# Récupérer les dimensions de l'écran
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()
largeur=700
hauteur=750
# Calculer les coordonnées de la fenêtre centrée
x = (largeur_ecran - largeur) // 2
y = (hauteur_ecran - hauteur) // 2

# Définir la géométrie de la fenêtre
root.geometry(f"{largeur}x{hauteur}+{x}+{y}")
img_data = ImageTk.PhotoImage(Image.open("C://Users//aitichou//Desktop//securitev1//logo.png",'r').resize((500,500)))
# variable to hold the image path
img_var = StringVar()
image_label = Label(root,image=img_data,width=500,height=500)
image_label.pack()
select = Button(root,text="Sélectionner une image",command=get_image,width=25,background='orange',font=('Arial',14,'bold')).pack(padx=20,pady=20)
frame = Frame(root)
frame.pack()
encrypt=Button(frame,text="cryptage",command=encrypt_image,width=25,background='orange',font=('Arial',12,'bold')).grid(row=0,column=0,padx=5,pady=5,sticky='sw')

decrypt=Button(frame,text="Decryptage",command=decrypt_image,width=25,background='orange',font=('Arial',12,'bold')).grid(row=0,column=1,padx=5,pady=5,sticky='se')
affichagehisto=Button(frame,text="Afficher l'histogramme",command=afficher_histogramme,width=25,background='orange',font=('Arial',12,'bold')).grid(row=1,column=0,padx=5,pady=5,sticky='se')
Mesure=Button(frame,text="mesure la qualité d'image",command=Mesurqualite,width=25,background='orange',font=('Arial',12,'bold')).grid(row=1,column=1,padx=5,pady=5,sticky='se')

root.mainloop()