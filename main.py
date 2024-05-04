import sys
import LightUp
import cnf
import satsolver

def update_and_print_board(solution, puzzle):
    size = len(puzzle.board)
    board = [row[:] for row in puzzle.board] 
    for var_decl in solution:
        var_name = var_decl.name()
        if var_name.startswith('L'):
            index = int(var_name[1:]) - 1  
            row = index // size
            col = index % size
            board[row][col] = 'L'  # placer l'ampoule dans la position résultante

    print("Updated puzzle:")
    for row in board:
        print(' '.join(row))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python3 main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    puzzle = LightUp.Puzzle()
    
    puzzle.load_from_file(filename)
    
    print("Loaded puzzle:")
    puzzle.print_board()

    # puzzle to cnf
    cnf_formula = cnf.puzzle_to_cnf(puzzle.board)

    # generer dimacs format fichier
    dimacs = "output.txt"
    cnf.write_dimacs(cnf_formula['variables'], cnf_formula['clauses'], dimacs)

    # utilise z3 pour trouver des solutions
    solution = satsolver.solve_sat(dimacs)

    if solution:
        print("SAT solution found:")
        print(solution)
        update_and_print_board(solution, puzzle)
    else:
        print("No solution")
