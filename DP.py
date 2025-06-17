import time
import threading
import copy

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

def resolve(ci, cj):
    resolvents = set()
    for literal in ci:
        if -literal in cj:
            # Remove literal and its negation, combine rest
            new_clause = (ci - {literal}) | (cj - {-literal})
            resolvents.add(frozenset(new_clause))
    return resolvents



def resolution(clauses):
    """Apply the resolution algorithm to a set of clauses."""
    clause_set = set(frozenset(clause) for clause in clauses)

    while True:
        new_clauses = set()
        clause_list = list(clause_set)

        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                ci = clause_list[i]
                cj = clause_list[j]
                resolvents = resolve(ci, cj)

                if frozenset() in resolvents:
                    return -1  # unsatisfiable

                new_clauses.update(resolvents)

        if new_clauses.issubset(clause_set):
            return 1  # satisfiable

        clause_set.update(new_clauses)

def Davis_Putnam(g):
    t = 0
    r = []
    original_clauses = copy.deepcopy(g)  # Save original

    while True:
        if len(g) == 0:
            t = 1
            break
        else:
            if any(len(clause) == 0 for clause in g):
                t = -1
                break

        # One literal rule
        i = 0
        while i < len(g):
            if len(g[i]) == 1:
                f = next(iter(g[i]))
                g.pop(i)
                j = 0
                while j < len(g):
                    if f in g[j]:
                        g.pop(j)
                    elif -f in g[j]:
                        g[j].remove(-f)
                        j += 1
                    else:
                        j += 1
                i = 0
            else:
                i += 1

        # Pure literal rule
        d = 0
        while d < len(g):
            r = set(g[d])
            for lit in r:
                is_pure = all(-lit not in g[i] for i in range(len(g)) if i != d)
                if is_pure:
                    i = 0
                    while i < len(g):
                        if lit in g[i]:
                            g.pop(i)
                        elif -lit in g[i]:
                            g[i].remove(-lit)
                            i += 1
                        else:
                            i += 1
                    d = 0
                    break
            else:
                d += 1

        print("No further simplification possible. Falling back to resolution...")
        t = resolution(original_clauses)  # Use original copy!
        break

    if t == -1:
        print("unsatisfiable")
    elif t == 1:
        print("satisfiable")


def run_with_timeout(func, args=(), kwargs=None, timeout=10):
    if kwargs is None:
        kwargs = {}
    result = [None]
    exc = [None]
    start_time = time.time()
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exc[0] = e
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    end_time = time.time()
    elapsed = end_time - start_time
    if thread.is_alive():
        print(f"Computation stopped: exceeded {timeout} seconds.")
        print(f"Execution time: {elapsed:.6f} seconds")
        return None
    if exc[0]:
        raise exc[0]
    print(f"Execution time: {elapsed:.6f} seconds")
    return result[0]

g = clauses()
run_with_timeout(Davis_Putnam, args=(g,), timeout=10)
