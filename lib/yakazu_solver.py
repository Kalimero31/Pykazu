import numpy as np
import imageio
import os
import shutil

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import lib.grid_maker as grid_maker
import lib.grid_reader as grid_reader


class YakazuSolver():
    def __init__(self, matrix):

        os.makedirs('generated_grid')

        self.matrix = matrix
        print("Shape", self.matrix.shape)
        self.initial_matrix = self.matrix.copy()
        self.matrices_hypotheses_invalides = np.empty((9, 9), dtype=object)
        for i in range(9):
            for j in range(9):
                self.matrices_hypotheses_invalides[i, j] = np.array([])

        # Matrice des cases modifiables
        self.boolmat = self.matrix==0

        # Matrice des possibilités
        self.matrice_possibilitee = self.make_matrix_possibilities()


    def make_matrix_possibilities(self):

        matrice_possibilitee = np.zeros_like(self.matrix)

        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                # On traite la case si c'est une case modifiable dans notre partie

                if self.boolmat[i][j]:
                    matrice_possibilitee[i][j] = self.get_possibilities(i, j)[1]
        return matrice_possibilitee
    
    def FindBlanksRow(self, rowNumber):
        L_indexes = []
        start_index = 0
        lenght_array = 0
        for i in range(len(self.matrix[rowNumber])):

            if self.matrix[rowNumber][i] != -1:
                if lenght_array != 0:
                    lenght_array +=1
                else:
                    start_index = i
                    lenght_array +=1
                if i == len(self.matrix[0])-1:
                    L_indexes.append((start_index, lenght_array))
            else:
                if lenght_array!=0:
                    L_indexes.append((start_index, lenght_array))
                    start_index = 0
                    lenght_array = 0
        return(L_indexes)
    
    def FindBlanksColumn(self, columnNumber):
        L_indexes = []
        start_index = 0 
        lenght_array = 0
        for i in range(self.matrix.shape[0]):

            if self.matrix[:, columnNumber][i] != -1:
                if lenght_array != 0:
                    lenght_array +=1
                else:
                    start_index = i
                    lenght_array +=1
                if i == self.matrix.shape[0]-1:
                    L_indexes.append((start_index, lenght_array))
            else:
                if lenght_array!=0:
                    L_indexes.append((start_index, lenght_array))
                    start_index = 0
                    lenght_array = 0
        return(L_indexes)
    
    def FindBlanksMatrix(self):
        return([self.FindBlanksRow(i) for i in range(len(self.matrix))],
               [self.FindBlanksColumn(i) for i in range(len(self.matrix[0]))])
    
    def get_yakazu_lines(self, x, y):
        # Retourner le array de la ligne:
        for i in self.FindBlanksRow(x):
            for j in range(i[1]):
                if y == i[0]+j:
                    row_position = (x, i[0])
                    row_array = self.matrix[x][i[0]:i[0]+i[1]]

        # Retourner le array de la colonne:  
        for i in self.FindBlanksColumn(y):
            for j in range(i[1]):
                if x == i[0]+j:
                    column_array = self.matrix[:, y][i[0]:i[0]+i[1]]
                    column_position = (i[0], y)
        return(row_array, column_array, (row_position, column_position))
    
    def get_possibilities(self, x, y):
        row_array, col_array = self.get_yakazu_lines(x, y)[0:2]

        # On calcule la valeur maximale d'une cellule grace à la longueur de sa ligne/colonne
        row_max = len(row_array)
        col_max = len(col_array)
        
        if row_max == 1:
            max_int = col_max
        elif col_max == 1:
            max_int = row_max
        else:
            max_int = min(row_max, col_max)

        # print(f'max int row: {row_max} and max int col {col_max}')

        # On lui retire les entiers déjà présents sur la ligne/colonne
        possibles_integers = np.setdiff1d(np.setdiff1d(np.array(range(1, max_int+1)), row_array), col_array)

        # possibles_integers = np.setdiff1d(possibles_integers, self.matrices_hypotheses_invalides[x][y])
        return possibles_integers, len(possibles_integers)
    
    def get_necessary_numbers(self, line):
        if len(line)>1:
            return(np.setdiff1d(np.array([range(1, len(line)+1)]), np.unique(line)))
        else:
            return(range(1,10))
    
    def find_an_opportunity(self, x, y):
        needed_numbers_row = self.get_necessary_numbers(self.get_yakazu_lines(x, y)[0])
        needed_numbers_col = self.get_necessary_numbers(self.get_yakazu_lines(x, y)[1])
        # print("Needed numbers for this row :", needed_numbers_row)
        # print("Needed numbers for this col :", needed_numbers_col)

        row, column, lines_positions = self.get_yakazu_lines(x, y)

        if len(row)>1:
            # print("for the row")

            for i in needed_numbers_row:

                possibilites_rows = []
                

                for j in range(len(row)):
                    if self.boolmat[ lines_positions[0][0]][lines_positions[0][1]+j]:
                        # print(f'For X={lines_positions[0][0]} and Y={lines_positions[0][1]+j}: {(self.get_possibilities(lines_positions[0][0], lines_positions[0][1]+j))[0]}')
        
                        if i in (self.get_possibilities(lines_positions[0][0], lines_positions[0][1]+j))[0]:
                            possibilites_rows.append((lines_positions[0][0], lines_positions[0][1]+j, i))

                # print(f'found {len(possibilites_rows)} possibilities for number {i}')

                if len(possibilites_rows) == 1:
                    return(possibilites_rows[0])
        
        if len(column)>1:
            # print("for the col")
            for i in needed_numbers_col:
            
                possibilites_cols = []
                for j in range(len(column)):
                    if self.boolmat[lines_positions[1][0]+j][lines_positions[1][1]]:
                        if i in (self.get_possibilities(lines_positions[1][0]+j, lines_positions[1][1]))[0]:
                            possibilites_cols.append((lines_positions[1][0]+j, lines_positions[1][1], i))

                # print(f'found {len(possibilites_cols)} possibilities for number {i}')
                
                if len(possibilites_cols) == 1:
                    return(possibilites_cols[0])
                
        return(None)
    
    def take_an_opportunity(self, possibility):
        # print(f"An opportunity has been taken on cell {possibility[0],possibility[1]}")

        # Mise à jour de la matrice du Yakazu
        self.matrix[possibility[0], possibility[1]] = possibility[2]

        # Mise à jour de la matrice des cases modifiables
        self.boolmat[possibility[0], possibility[1]] = False

        # Mise à jour de la matrice des possibilités
        self.matrice_possibilitee = self.make_matrix_possibilities()
        return
    
    def check_opportunities(self):
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.boolmat[i][j]:

                    opport = self.find_an_opportunity(i, j)

                    if opport!=None:
                        self.take_an_opportunity(opport)
                        return

    def resolution_loop(self):
        self.draw_grid(self.matrix, 0)
        for k in range(1, 100):
            # print(k)
            self.write_on_easy_cells()
            self.check_opportunities()
            self.draw_grid(self.matrix, k)
            if self.check_grid_complete():
                # self.make_animation()
                return
        return

    def write_on_easy_cells(self):
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.boolmat[i][j] and self.matrice_possibilitee[i][j]==1:
                    # print("seul possib:", i,j, self.get_possibilities(i, j)[0])
                    self.matrix[i][j] = self.get_possibilities(i, j)[0][0]

                    # Mise à jour de la matrice des cellules modifiables
                    self.boolmat[i][j] = False

                    # Mise à jour de la matrice des possibilités
                    self.matrice_possibilitee = self.make_matrix_possibilities()

                    return
        return

    def draw_grid(self, matrix, n):
        fig, ax = plt.subplots()
        ax.imshow(matrix, cmap='gray', vmin=-1, vmax=0)

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                val = matrix[i, j]

                # Ajouter une bordure
                rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='none')
                ax.add_patch(rect)

                if val == -1:
                    continue  # No text for -1 (black cell)
                elif val == 0:
                    ax.text(j, i, '', ha='center', va='center', fontsize=20, color='black')
                else:
                    ax.text(j, i, str(val), ha='center', va='center', fontsize=20, color='black')
        
        plt.axis('off')
        plt.savefig('generated_grid/'+str(n)+'.png')

    def check_grid_complete(self):
        return(np.all(self.boolmat == False))
    
    def make_animation(self):
        dossier = 'generated_grid'  # Remplace par le nom de ton dossier
        nom_du_gif = 'animation.gif'  # Nom du fichier GIF à créer

        images = []
        for fichier in sorted(os.listdir(dossier)):
            if fichier.endswith('.png'):
                chemin_fichier = os.path.join(dossier, fichier)
                images.append(imageio.imread(chemin_fichier))

        imageio.mimsave(nom_du_gif, images, duration=1)  # duration est en secondes
        shutil.rmtree(dossier)


