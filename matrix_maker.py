import lib.grid_maker as gmk
import lib.grid_reader as grd
import numpy as np

# test_image = 'grids-png/grille_1.png'
# test_image = 'grids-png/grille_2.jpeg'
# test_image = 'grids-png/grille_3.png'

path_imgs = 'grids-png/'
img_name = 'grille_1.png'

YakazuMatrix = grd.TraitementImage(path_imgs+img_name).grid_matrix

np.save('matrices/1', YakazuMatrix)