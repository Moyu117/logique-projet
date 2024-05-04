# pour affichier le plateau de jeu
class Puzzle:
    def __init__(self):
        self.size = 0
        self.board = []

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.size = len(lines)
            self.board = [list(line.strip()) for line in lines]
            
    def print_board(self):
        for row in self.board:
            print(' '.join(row))


class LightUp(Puzzle):
    def __init__(self, size):
        super().__init__(size)
        self.L = [[0 for _ in range(size)] for _ in range(size)]
        self.I = [[0 for _ in range(size)] for _ in range(size)]
        self.blocks = set()  # un ensemble pour stocker les cases noires
        self.numbers = {}  # un dictionnaire pour stocker les cases noires avec un nombre

    def add_block(self, i, j):
        # ajouter une case noire en (i, j)
        self.blocks.add((i, j))
        
    def add_numbered_block(self, i, j, n):
        # ajouter une case noire avec un nombre en (i, j)
        self.numbers[(i, j)] = n

    def print_board(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.I[i][j]:  # si la case est illuminée
                    row.append('I')
                elif self.L[i][j]:  # si la case contient une lumière
                    row.append('L')
                elif (i, j) in self.blocks:
                    row.append('X')
                elif (i, j) in self.numbers:
                    row.append(str(self.numbers[(i, j)]))
                else:
                    row.append('.')
            print(' '.join(row))