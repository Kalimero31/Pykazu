import lib.yakazu_solver as YakazuSolver
import numpy as np
matrix_to_load = np.load('matrices/1.npy')

# Correction sur la lecture d'image
matrix_to_load[4][8] = 2
# print(matrix_to_load)

testSolveur = YakazuSolver.YakazuSolver(matrix_to_load)

# testSolveur.find_an_opportunity(5,6)

# print(testSolveur.find_an_opportunity(x, y))
testSolveur.resolution_loop()


# print(testSolveur.get_necessary_numbers(line))