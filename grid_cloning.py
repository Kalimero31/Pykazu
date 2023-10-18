test_image = 'grids-png/grille_1.png'
test_image = 'grids-png/grille_2.jpeg'
test_image = 'grids-png/grille_3.png'
test_image = 'grids-png/grille_4.png'

YakazuMatrix = grd.TraitementImage(test_image).grid_matrix

print(YakazuMatrix)
YakazuGame = gmk.YakazuGame(YakazuMatrix)
print(YakazuMatrix)