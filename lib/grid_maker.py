import tkinter as tk
import numpy as np

class YakazuGame:
    def __init__(self, matrix):
        self.game_matrix = np.array(matrix)
        self.user_matrix = np.zeros_like(self.game_matrix)
        self.entries = {}
        self.root = tk.Tk()
        n, m = self.game_matrix.shape
        self.root.geometry(f"{n * 50}x{m * 50}")
        self.init_grid()
        self.root.mainloop()

    def init_grid(self):
        for i in range(self.game_matrix.shape[0]):
            for j in range(self.game_matrix.shape[1]):
                x, y = i * 50, j * 50
                color = "black" if self.game_matrix[i, j] == -1 else "white"
                
                canvas = tk.Canvas(self.root, bg=color, width=50, height=50)
                canvas.place(x=y, y=x)

                if self.game_matrix[i, j] == 0:
                    text_var = tk.StringVar()
                    text_var.trace("w", lambda *args, text_var=text_var, i=i, j=j: self.update_matrix(text_var, i, j))
                    entry = tk.Entry(self.root, textvariable=text_var, width=3, font=("Times", 28), justify='center')
                    entry.place(x=y, y=x, width=50, height=50)
                    self.entries[(i, j)] = entry
                
                elif self.game_matrix[i, j] != -1:
                    label = tk.Label(self.root, text=str(self.game_matrix[i,j]), background="white", font=("Times", 28), justify='center')
                    label.place(x=y+5, y=x+5, width=40, height=40, bordermode='ignore')


    def flash_red(self, entries):
        for entry in entries:
            entry.configure({"background": "red"})
        self.root.after(500, lambda: self.reset_color(entries))

    def reset_color(self, entries):
        for entry in entries:
            entry.configure({"background": "white"})

    def update_matrix(self, text_var, i, j):
        try:
            value = int(text_var.get())
            
            if value in self.user_matrix[i, :j] or value in self.user_matrix[i, j+1:]:
                print("Valeur déjà présente sur la même ligne")
                self.flash_red([self.entries[(i, x)] for x in range(self.user_matrix.shape[1]) if (i, x) in self.entries])
                text_var.set("")
                return
                
            if value in self.user_matrix[:i, j] or value in self.user_matrix[i+1:, j]:
                print("Valeur déjà présente sur la même colonne")
                self.flash_red([self.entries[(x, j)] for x in range(self.user_matrix.shape[0]) if (x, j) in self.entries])
                text_var.set("")
                return

            self.user_matrix[i, j] = value
        except ValueError:
            print("Valeur invalide")
# Exemple d'utilisation

# matrice = np.array([
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1]
# ])

# cases_noires = [
#                 (0,2), (0,4), (0,6), (0,7),
#                 (2,7),
#                 (4,2), (4,4), (4,7),
#                 (6,0),(6,2), (6,4), (6,7),
#                 (7,0),
#                 (8,7), (8,8)
#                 ]

# for i in cases_noires:
#     matrice[i[1]][i[0]] = 0
# game = YakazuGame(matrice)