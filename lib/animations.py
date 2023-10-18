import imageio
import os
import shutil

dossier = 'generated_grid'  # Remplace par le nom de ton dossier
nom_du_gif = 'animation.gif'  # Nom du fichier GIF à créer

images = []
for fichier in sorted(os.listdir(dossier)):
    if fichier.endswith('.png'):
        chemin_fichier = os.path.join(dossier, fichier)
        images.append(imageio.imread(chemin_fichier))

imageio.mimsave(nom_du_gif, images, duration=1)  # duration est en secondes
shutil.rmtree(dossier)
