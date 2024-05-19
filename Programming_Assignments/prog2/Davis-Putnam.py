def davis_putnam(clauses, assignments={}):
    if not clauses:
        return True, assignments
    
    if any(not clause for clause in clauses):
        return False, {}
    
    simplified_clauses, new_assignments = simplify_clauses(clauses)
    if new_assignments is None:
        return False, {}
    
    assignments.update(new_assignments)
    
    if not simplified_clauses:  
        return True, assignments
    
    #select a literal
    literal = select_literal(simplified_clauses)
    
    #literal be True
    true_branch = assign_and_simplify(simplified_clauses, literal, True)
    solvable, true_assignments = davis_putnam(true_branch, {**assignments, literal: True})
    if solvable:
        return True, true_assignments
    
    #literal be False
    false_branch = assign_and_simplify(simplified_clauses, literal, False)
    solvable, false_assignments = davis_putnam(false_branch, {**assignments, literal: False})
    if solvable:
        return True, false_assignments
    
    return False, {}


def simplify_clauses(clauses):
    simplified_clauses = clauses[:]
    assignments = {}
    changed = True
    
    while changed:
        changed = False
        unit_clauses = [clause for clause in simplified_clauses if len(clause) == 1]
        for clause in unit_clauses:
            literal = clause[0]
            val = True if literal > 0 else False
            literal = abs(literal)
            
            if literal in assignments:
                continue
            
            assignments[literal] = val
            changed = True
            #apply to all clauses
            simplified_clauses = [simplify_clause(clause, literal, val) for clause in simplified_clauses]

    #remove empty clauses after simplification
    simplified_clauses = [clause for clause in simplified_clauses if clause]

    #check for empty clause --> contradiction
    if [] in simplified_clauses:
        return None, None 
    
    return simplified_clauses, assignments


def simplify_clause(clause, literal, val):
    #create a new clause without the literal if it should be removed
    if val:
        return [l for l in clause if l != -literal]  # Remove if True
    else:
        return [l for l in clause if l != literal]  # Remove if False


def select_literal(clauses):
    for clause in clauses:
        for literal in clause:
            return abs(literal)  #return the first found literal

def assign_and_simplify(clauses, literal, value):
    result = []
    for clause in clauses:
        if literal in clause and value or -literal in clause and not value:
            #satisfied
            continue
        #remove negation
        new_clause = [l for l in clause if l != -literal]
        result.append(new_clause)
    return result

def read_file(filepath):
    clauses, backmatter, max_atom = [], '', 0
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # see if we passed the clauses
    past_clauses = False
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == '0':
            past_clauses = True 
            continue 

        if not past_clauses:
            clause = list(map(int, stripped_line.split()))
            clauses.append(clause)
            # update max_atom 
            max_atom = max(max_atom, max(abs(lit) for lit in clause))
        else:
            backmatter += line
    
    return clauses, max_atom, backmatter


def output(solution, success, backmatter, filepath):
    with open(filepath, 'w') as file:
        if success:
            for atom in sorted(solution.keys(), key=int):
                value = solution[atom]
                file.write(f"{atom} {'T' if value else 'F'}\n")
            file.write("0\n")
        else:
            file.write("0\n")
        file.write(backmatter)

def main():
    input_filepath = 'dp_input.txt' 
    output_filepath = 'dp_output.txt' 
    
    clauses, max_atom, backmatter = read_file(input_filepath)
    solvable, assignments = davis_putnam(clauses)
    output(assignments, solvable, backmatter, output_filepath)

if __name__ == "__main__":
    main()
