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

def clause_is_satisfied(clause, mask):
    #loop over each literal in the clause
    for lit in clause:
        #get the index of the variable (zero-based for bitmask ops)
        var_idx = abs(lit) - 1

        # extract the bit at position var_idx from the mask
        # (mask >> var_idx) shifts the bit of interest to the rightmost position
        # & 1 isolates that single bit (0 or 1)
        bit = (mask >> var_idx) & 1

        #check if the literal is satisfied under this bitmask assignment
        #if the literal is positive (e.g. x3), it’s satisfied when the bit is 1 (True)
        #if the literal is negative (e.g. ¬x3), it’s satisfied when the bit is 0 (False)
        if (lit > 0 and bit == 1) or (lit < 0 and bit == 0):
            return True  # At least one literal in the clause is satisfied

    #if none of the literals are satisfied, the clause is not satisfied
    return False

def count(g):
    n=len(g)
    return n

def formula_is_satisfied(clauses, mask):
    #check if all clauses are satisfied by this assignment
    for clause in clauses:
        if not clause_is_satisfied(clause, mask):
            return False
    return True

def sat_solver(clauses, num_vars):
    max_mask = 1 << num_vars  # 2^num_vars total assignments
    timeout_seconds = 10  # Maximum time allowed for the solver
    start_time = time.time()  # Start a timer to enforce a timeout

    for mask in range(max_mask):
        # Check for timeout
        if time.time() - start_time >= timeout_seconds:
            print("Timeout reached. Terminating SAT solver.")
            return False

        # Early exit: If any clause is unsatisfiable under the current mask, skip further checks
        if not formula_is_satisfied(clauses, mask):
            continue

        # Found a satisfying assignment
        assignment = [(f"x{i+1}", (mask >> i) & 1) for i in range(num_vars)]
        print("SATISFIABLE")
        print("Assignment:", assignment)
        return True

    print("UNSATISFIABLE")
    return False

g=clauses()
n=count(g)
time_function(sat_solver,g,n)

