import time
import threading


# this function measures and prints the execution time of another function
def time_function(func, *args, **kwargs):
    # start timer
    start_time = time.time()
    result = func(*args, **kwargs)
    # end timer
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    return result


# reads clauses from user input, each clause is a set of integers
def clauses():
    print("input clauses")
    clauses = []  # list of all clauses
    while True:
        line = input()
        if line == "":
            break
        g = set()
        for i in line.split(","):  # use digits separated with "," for each clause
            g.add(int(i))
        clauses.append(g)
    return clauses


# resolve two clauses, return set of resolvents
def resolve(ci, cj):
    resolvents = set()
    for literal in ci:
        if -literal in cj:
            # remove literal and its negation, combine rest
            new_clause = (ci - {literal}) | (cj - {-literal})
            resolvents.add(frozenset(new_clause))
    return resolvents


# main resolution algorithm
def resolution(clauses):
    # convert each clause (which is a set) to a frozenset for use in a set
    clause_set = set(frozenset(clause) for clause in clauses)
    print("Initial clauses:", clause_set)

    while True:
        new_clauses = set()
        clause_list = list(clause_set)

        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                ci = set(clause_list[i])  # convert frozenset back to set for resolve
                cj = set(clause_list[j])
                resolvents = resolve(ci, cj)

                for res in resolvents:
                    if len(res) == 0:  # found empty clause
                        print(f"Contradiction found by resolving {ci} and {cj}")
                        print("unsatisfiable")
                        return

                new_clauses.update(resolvents)

        if new_clauses.issubset(clause_set):  # no new clauses
            print("satisfiable")
            return

        print("New clauses generated this round:", new_clauses)
        clause_set.update(new_clauses)


# runs a function with a timeout, prints execution time, and stops if too slow
def run_with_timeout(func, args=(), kwargs=None, timeout=10):
    if kwargs is None:
        kwargs = {}
    result = [None]
    exc = [None]
    start_time = time.time()  # start timer

    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exc[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    end_time = time.time()  # end timer
    elapsed = end_time - start_time
    if thread.is_alive():
        print(f"Computation stopped: exceeded {timeout} seconds.")
        print(f"Execution time: {elapsed:.6f} seconds")
        return None
    if exc[0]:
        raise exc[0]
    print(f"Execution time: {elapsed:.6f} seconds")
    return result[0]


# main program: get clauses and run resolution with timeout
g = clauses()
run_with_timeout(resolution, args=(g,), timeout=10)
