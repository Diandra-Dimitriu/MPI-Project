import time

def time_function(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    return result

def clauses():
    print("input clauses")
    clauses = []  # list of all clauses
    while True:
        line = input()
        if line == "":
            break
        g = []
        for i in line.split(","):  # use digits separated with "," for each clause
            g.append(int(i))
        clauses.append(g)
    return clauses

def cond(g):
    if len(g) == 0:
        return 1  # condition for satisfiability
    else:
        j = 0
        for i in range(len(g)):
            if len(g[i]) == 0:
                j = j + 1
        if j == len(g):  # condition for unsatisfiability
            return -1
        else:
            return 0


def unit_propagate(formula, assignments, decision_level, trail, implication_graph):
    #perform unit propagation, record implications
    changed = True
    while changed:
        changed = False
        for clause in formula[:]:
            unassigned = []
            true_lits = []
            for lit in clause:
               var = abs(lit)
    
               if var not in assignments:
                  unassigned.append(lit)
               else:
                  assigned_val = assignments[var]  # True or False
                  if (lit > 0 and assigned_val) or (lit < 0 and not assigned_val):
                      true_lits.append(lit)
            if len(true_lits) > 0:
                continue  #clause is already satisfied

            if len(unassigned) == 1:
                unit = unassigned[0]
                var = abs(unit)
                val = unit > 0
                assignments[var] = val
                trail.append((var, decision_level))
                implication_graph[var] = [lit for lit in clause if abs(lit) != var]
                changed = True

            elif len(unassigned) == 0:
                return clause  #conflict detected
    return None


def analyze_conflict(conflict, trail, implication_graph):
    #conflict analysis: learns the negation of the last assigned variable
    if not trail:
        return []

    last_var, _ = trail[-1]
    return [-last_var]


def backjump(assignments, trail, backjump_level):
    #undo assignments made after the backjump_level.
    new_trail = []
    for var, level in trail:
        if level <= backjump_level:
            new_trail.append((var, level))
        else:
            assignments.pop(var, None)
    return new_trail



def choose_variable(assignments, formula):
    #select most frequent unassigned variable (simplified VSIDS)
    counter = {}
    for clause in formula:
        for lit in clause:
            var = abs(lit)
            if var not in assignments:
                counter[var] = counter.get(var, 0) + 1
    return max(counter, key=counter.get, default=None)



def CDCL(formula):
    assignments = {}
    trail = []
    implication_graph = {}
    decision_level = 0

    while True:
        conflict = unit_propagate(formula, assignments, decision_level, trail, implication_graph)

        if conflict:
            if decision_level == 0:
                print("unsatisfiable")
                return
            learned_clause = analyze_conflict(conflict, trail, implication_graph)
            formula.append(learned_clause)
            # backjump to previous level (simplified)
            decision_level -= 1
            trail = backjump(assignments, trail, decision_level)
        else:
            if all(abs(lit) in assignments for clause in formula for lit in clause):
                print("satisfiable")
                return
            var = choose_variable(assignments, formula)
            if var is None:
                print("satisfiable")
                return
            decision_level += 1
            # decide var = True (can alternate for completeness)
            assignments[var] = True
            trail.append((var, decision_level))



g=clauses()
time_function(CDCL,g)
