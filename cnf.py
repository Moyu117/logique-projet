from itertools import combinations

# make sure that variable numbers start from 1, cause cannot be 0 in SAT
# every cell in the grid has a variable number
def convert_to_var_num(i, j, size):
    return i * size + j + 1

# make sure that lights in the same row or column do not illuminate each other, unless there is a wall between them
def block_other_lights(i, j, size, puzzle, clauses):
    # check right
    blocked = False
    for x in range(j + 1, size):
        if puzzle[i][x] != '.':
            blocked = True
        elif not blocked:
            clauses.append([-convert_to_var_num(i, j, size), -convert_to_var_num(i, x, size)])
        else:
            break

    # check left
    blocked = False
    for x in range(j - 1, -1, -1):
        if puzzle[i][x] != '.':
            blocked = True
        elif not blocked:
            clauses.append([-convert_to_var_num(i, j, size), -convert_to_var_num(i, x, size)])
        else:
            break

    # check down
    blocked = False
    for y in range(i + 1, size):
        if puzzle[y][j] != '.':
            blocked = True
        elif not blocked:
            clauses.append([-convert_to_var_num(i, j, size), -convert_to_var_num(y, j, size)])
        else:
            break

    # check up
    blocked = False
    for y in range(i - 1, -1, -1):
        if puzzle[y][j] != '.':
            blocked = True
        elif not blocked:
            clauses.append([-convert_to_var_num(i, j, size), -convert_to_var_num(y, j, size)])
        else:
            break

def illuminate_required_cells(i, j, size, puzzle, clauses):
    if puzzle[i][j] == '.':
        # Initialize a list. Variables storing the lamps that may illuminate the current grid
        illuminating_lights = []

        # Check left until border or wall/number is encountered
        for x in range(j - 1, -1, -1):
            if puzzle[i][x] != '.':
                break
            illuminating_lights.append(convert_to_var_num(i, x, size))

        # Check right
        for x in range(j + 1, size):
            if puzzle[i][x] != '.':
                break
            illuminating_lights.append(convert_to_var_num(i, x, size))

        # Check up
        for y in range(i - 1, -1, -1):
            if puzzle[y][j] != '.':
                break
            illuminating_lights.append(convert_to_var_num(y, j, size))

        # Check down
        for y in range(i + 1, size):
            if puzzle[y][j] != '.':
                break
            illuminating_lights.append(convert_to_var_num(y, j, size))

        # Adds its own lamp variable
        illuminating_lights.append(convert_to_var_num(i, j, size))

        # Adding constructed clauses to the clause set
        clauses.append(illuminating_lights)





def puzzle_to_cnf(puzzle):
    clauses = []
    size = len(puzzle)

    def add_clause_if_valid(i,j):
        if 0 <= i < size and 0 <= j < size:
            clauses.append([-(convert_to_var_num(i, j, size))])


    for i in range(size):
        for j in range(size):
            cell = puzzle[i][j]

            # -----case avec un nombre-----
            if cell.isdigit():
                n = int(cell)

                if n == 0:
                    add_clause_if_valid(i-1, j)  # case au-dessus
                    add_clause_if_valid(i+1, j)  # case en-dessous
                    add_clause_if_valid(i, j-1)  # case à gauche
                    add_clause_if_valid(i, j+1)  # case à droite
                else:
                    # For all numbers to be processed, define uniformly the indexes of adjacent grids
                    adjacent_indices = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    adjacent_vars = [convert_to_var_num(x, y, size) for x, y in adjacent_indices if 0 <= x < size and 0 <= y < size]

                    if n == 1:
                        # At least one neighboring grid has a light
                        clauses.append(adjacent_vars)
                        # Make sure no more than one compartment has a light
                        for k1, var1 in enumerate(adjacent_vars):
                            for var2 in adjacent_vars[k1+1:]:
                                clauses.append([-var1, -var2])


                    elif n == 2:
                        two_combos = list(combinations(adjacent_vars, 2))
                        clauses.append([var for combo in two_combos for var in combo])

                        for var in adjacent_vars:
                            if not any(var in combo for combo in two_combos):
                                clauses.append([-var])

                        # Ajouter une logique pour s'assurer qu'il n'y a pas plus de deux ampoules allumées.
                        for combo in combinations(adjacent_vars, 3):
                            clauses.append([-combo[0], -combo[1], -combo[2]])




                    elif n == 3:
                        three_combos = list(combinations(adjacent_vars, 3))
                        # Make sure three bulbs light up exactly
                        clauses.append([var for combo in three_combos for var in combo])

                        # All other lights should be turned off except for these three
                        other_vars = [var for var in adjacent_vars if not any(var in combo for combo in three_combos)]
                        for var in other_vars:
                            clauses.append([-var])

                        if len(adjacent_vars) > 3:  # Lorsqu'il existe quatre grilles voisines
                            for combo in combinations(adjacent_vars, 4):
                                clauses.append([-var for var in combo])




                    elif n == 4: #ok
                        # Light bulbs must be placed in all adjacent compartments
                        for var in adjacent_vars:
                            clauses.append([var])


            # -----case noire-----
            elif cell == 'X':
                var_num = convert_to_var_num(i, j, size)
                clauses.append([-var_num])

            # -----case vide-----
            elif cell == '.':
                pass

            block_other_lights(i, j, size, puzzle, clauses)

            illuminate_required_cells(i, j, size, puzzle, clauses)

    
                    

    
    cnf_formula = {
        "variables": size * size,
        "clauses": clauses
    }

    return cnf_formula







def write_dimacs(num_vars, clauses, filename):
    with open(filename, 'w') as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

def generate_dimacs(puzzle):
    cnf_formula = puzzle_to_cnf(puzzle)
    num_vars = cnf_formula['variables']
    clauses = cnf_formula['clauses']
    write_dimacs(num_vars, clauses, "output.cnf")