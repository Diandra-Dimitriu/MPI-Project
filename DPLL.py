
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


def count(g, r, b):  # b and r have to be 2 empty lists
    for i in range(len(g)):
        for j in range(len(g[i])):
            if g[i][j] not in r:
                r.append(g[i][j])  # put every variable that exists in r
    for l in range(len(r)):  # count how many times each variable is in g
        nr = 0
        for i in range(len(g)):
            for j in range(len(g[i])):
                if g[i][j] == r[l]:
                    nr += 1
        b.append(nr)


def maximum(b):  # index of the biggest number in a list
    max_val = -1
    j = -1
    for i in range(len(b)):
        if b[i] > max_val:
            max_val = b[i]
            j = i
    return j


def splitting(g):
    variables = []
    variable_counts = []
    count(g, variables, variable_counts)

    if not variables:
        return cond(g)

    #choose the variable with the highest occurrence
    max_index = maximum(variable_counts)
    selected_var = variables[max_index]

    #attempt setting selected_var to True
    g_true = []
    for clause in g:
        if selected_var in clause:
            continue  # clause satisfied
        new_clause = []
        for literal in clause:
            if literal != -selected_var:
                new_clause.append(literal)
        g_true.append(new_clause)

    if cond(g_true) == 1:
        return 1
    elif cond(g_true) == 0:
        if splitting(g_true) == 1:
            return 1

    # attempt setting selected_var to False
    g_false = []
    for clause in g:
        if -selected_var in clause:
            continue  # clause satisfied
        new_clause = []
        for literal in clause:
            if literal != selected_var:
                new_clause.append(literal)
        g_false.append(new_clause)

    if cond(g_false) == 1:
        return 1
    elif cond(g_false) == 0:
        if splitting(g_false) == 1:
            return 1

    return -1


def Davis_Putnam_Logemann_Loveland(g):
    t = 0
    while True:
        t = cond(g)
        if t == -1 or t == 1:
            break

        # One literal rule
        i = 0
        while i < len(g):
            if len(g[i]) == 1:
                f = g[i][0]
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
                i = 0  # restart after modification
            else:
                i += 1

        # Pure literal rule
        d = 0
        while d < len(g):
            r = g[d][:]
            found_pure = False
            for lit in r:
                is_pure = True
                for i in range(len(g)):
                    if d == i:
                        continue
                    if -lit in g[i]:
                        is_pure = False
                        break
                if is_pure:
                    # Remove all clauses with this pure literal
                    i = 0
                    while i < len(g):
                        if lit in g[i]:
                            g.pop(i)
                        elif -lit in g[i]:
                            g[i].remove(-lit)
                            i += 1
                        else:
                            i += 1
                    d = 0  # restart after changes
                    found_pure = True
                    break
            if not found_pure:
                d += 1

        if t == 0:
            t = splitting(g)
            if t != 0:
                break

    if t == -1:
        print("unsatisfiable")
        return
    elif t == 1:
        print("satisfiable")
        return


g = clauses()
time_function(Davis_Putnam_Logemann_Loveland, g)