# INF402

## LIGHT UP (Akari)
### Description: 
Ce projet est un programme automatisé de résolution de puzzles "Light Up" basé sur des solveurs SAT. 
Le programme utilise la logique booléenne pour convertir les puzzles "Light Up" en problèmes SAT et utilise le solveur Z3 pour trouver des solutions. 

### Installation:
Ce projet a été développé en utilisant Python. Pour exécuter ce projet, Python 3 et les bibliothèques suivantes doivent être installés :

- Z3 Solver

pour installer : 

    pip install z3-solver

### Usage:
Pour résoudre light up puzzle:
depuis terminal: 

    python3 main.py puzzle/ficiher

Conversion des fichiers au format DIMACS en CNF lisibles:
Execute tran.c


#### Fonctionnement:
- Analyse des fichiers de puzzles : lit les puzzles "Light Up" à partir d'un fichier texte.
- Générer le CNF : convertit les règles du puzzle en CNF.
- Résoudre le puzzle : résout le CNF à l'aide du solveur SAT Z3 et affiche la solution.
- Imprimer la solution : imprime la solution du puzzle visuellement sur la console.

#### Affichage:
- case vide : '**.**'
- cases portant un numéro (0-4) : '**0**', '**1**', '**2**', '**3**', '**4**',
- case noire : '**X**'
- lumière : '**L**'

dans un fichier puzzle.txt, on représente une case vide par '**.**',  une case noire par '**X**' et on utilise '**0**' à '**4**' pour représenter directement les cases avec des chiffres, et les chiffres indiquent le nombre d'ampoules à placer autour

par exemple :
voici un puzzle initial:

```python
....1
..X.X
.4...
X..X.
..0..

```

voici le resultat obtenu:

```python
...L1
.LX.X
L4L..
XL.X.
L.0.L
```

#### Pour améliorer
*Dans la fonction **puzzle_to_cnf**, la fonction ne gère pas correctement les grilles contenant le chiffre **2** ou contenant le chiffre **3**.*