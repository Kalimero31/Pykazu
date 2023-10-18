import os
import cv2
import numpy as np
import pytesseract

from sklearn.cluster import KMeans


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Ajuste le chemin si nécessaire

save_path = 'cells_images'

if not os.path.exists(save_path):
    os.makedirs(save_path)

class TraitementImage():
    def __init__(self, image_path) -> None:
        self.image_path = image_path
        self.image = cv2.imread(self.image_path, 0)
        self.image_dimensions = self.image.shape
        self.image_black_and_white = cv2.threshold(self.image, 200, 255, cv2.THRESH_BINARY)[1]

        self.color_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        self.FindCells(self.image_black_and_white)
        contour_image = cv2.drawContours(self.color_image.copy(), self.contours, -1, (255,0,0), 2)

        self.grid_dimension = self.FindMax()
        self.columns = self.classify_lines(self.cells_X, int(self.grid_dimension))
        self.rows = self.classify_lines(self.cells_Y, int(self.grid_dimension))

        self.grid_matrix = np.full((self.grid_dimension, self.grid_dimension), -1)

        for i in range(len(self.cells)):
            self.grid_matrix[self.rows[i]][self.columns[i]] = 0

        self.check_cells_color()
        self.read_cells_tesseract()

        # cv2.imshow('Grey Scaled', contour_image)
        # cv2.waitKey(0)

    def FindCells(self, image):
        self.contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        self.cells = []
        self.cell_images = []

        for cnt in self.contours:
            x, y, w, h = cv2.boundingRect(cnt)

            aspect_ratio = w/h

            area = cv2.contourArea(cnt)

            if 0.9 <= aspect_ratio <=1.1 and area>100 and w < self.image_dimensions[0]/3:
                self.cells.append(cnt)

        # Creation des images et enregistrement

        for idx, contour in enumerate(self.cells):
            x, y, w, h = cv2.boundingRect(contour)
            cell = image[y:y+h, x:x+w]
            self.cell_images.append(cell)
            
            # Sauvegarde de l'image de la cellule
        #     cv2.imwrite(os.path.join(save_path, f'cell_{idx}.png'), cell)
        # print('len cells : ', len(self.cells))

        return self.contours
    
    def GetNumberOnSameLine(self, x, L, seuil):
        SameLineElements = []

        for i in range(len(L)):

            if ((L[i] - seuil < x) and (L[i] + seuil > x)):
                SameLineElements.append(i)

        return(len(SameLineElements))
    
    def FindMax(self):
        self.cells_X = [float(cv2.boundingRect(i)[0]) for i in self.cells]
        self.cells_Y = [float(cv2.boundingRect(i)[1]) for i in self.cells]

        line_lenghts = []

        for cell in self.cells:
            x = cv2.boundingRect(cell)[0]
            y = cv2.boundingRect(cell)[1]
            line_lenghts.append(self.GetNumberOnSameLine(x, self.cells_X, 15))
            line_lenghts.append(self.GetNumberOnSameLine(y, self.cells_Y, 15))
        
        return(max(line_lenghts))
    
    def classify_lines(self, x_coords, n_clusters):
        x_coords = np.array(x_coords).reshape(-1, 1)
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        kmeans.fit(x_coords)
        labels = kmeans.labels_

        # Création d'un dictionnaire pour mapper l'abscisse médiane à l'étiquette de la colonne
        median_map = {}
        for label in set(labels):
            median_map[label] = np.median(x_coords[labels == label])
            
        # Tri des labels en fonction de leur abscisse médiane
        sorted_labels = sorted(median_map, key=median_map.get)
        
        # Remplacement des labels par des numéros de colonne triés
        column_numbers = [sorted_labels.index(label) for label in labels]
        
        return np.array(column_numbers)
    
    def check_cells_color(self):
        self.cells_to_read_idxs = []
        for i in range(len(self.cell_images)):


            # Obtient les dimensions
            h, w = self.cell_images[i].shape

            # Calcule les nouvelles dimensions
            new_h = int(0.1 * h)
            new_w = int(0.1 * w)


            self.cell_images[i] = self.cell_images[i][new_h:h-new_h, new_w:w-new_w]

            if np.mean(self.cell_images[i])>245:
                self.grid_matrix[self.rows[i]][self.columns[i]] = 0
            else:
                self.cells_to_read_idxs.append(i)

    def read_cells_tesseract(self):
        for i in self.cells_to_read_idxs:
            # Seuillage pour améliorer la reconnaissance
            _, cell_thresh = cv2.threshold(self.cell_images[i], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            kernel = np.ones((2,2),np.uint8)
            cell_thresh = cv2.morphologyEx(cell_thresh, cv2.MORPH_CLOSE, kernel)



            # Utilisation de Tesseract pour effectuer l'OCR
            text = pytesseract.image_to_string(cell_thresh, config='--psm 6')
            
            try:
                self.grid_matrix[self.rows[i]][self.columns[i]] = int(text)
            except ValueError:  # Pas de numéro reconnu
                print('Un chiffre a été mal lu par le programme ! Veuilliez modifier la valeur de la matrice à la main')