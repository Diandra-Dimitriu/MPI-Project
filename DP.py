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

def resolution(g):
    t = 1  # if 0 then unsatisfiable, if -1 unknown
    d = 0  # current clause index
    r = []  # to store the current clause we're resolving
    previous_g = None  # To track changes in g

    while True:
        i = 0  # index for navigating through g

        while len(r) == 0:
            if d < len(g):
                if len(g[d]) != 0:
                    r = g[d]
                    g.pop(d)
                    # no need to increment d here since we popped that element
                else:
                    t = 0 
                    break
            else:
                t = -1
                break

        if t == 0 or t == -1:
            break

        k = 0
        while i < len(g):
            l = 0
            while l < len(g[i]):
                j = 0
                while j < len(r):
                    if g[i][l] == -r[j]:  # if resolution is possible
                        g[i].pop(l)
                        r.pop(j)
                        k = 1
                        l -= 1  # adjust index due to pop
                        break  # exit inner loop after resolution
                    else:
                        j += 1
                l += 1

            if k == 1:
                for item in g[i]:
                    if item not in r:  # avoid duplicates
                        r.append(item)
                g.pop(i)
                if len(r) == 0:     # <=== ADD THIS CHECK!
                    t = 0
                    break
                g.append(r.copy())
                r = []
                break  # restart resolution with new r
            else:
                i += 1

        # Add a safeguard to prevent infinite loops
        if g == previous_g:  # If g hasn't changed, terminate to avoid infinite loop
            t = -1
            break
        previous_g = g.copy()
    if t == 0: # unsatisfiable
        return -1
    elif t == -1: # unknown
        return 0

def Davis_Putnam(g):
    t = 0
    r = []
    while True:
        if len(g) == 0:  # condition for satisfiability
            t = 1
            break
        else:
            j = 0
            for i in range(len(g)):
                if len(g[i]) == 0:
                    j = j + 1
            if j > 0:  # condition for unsatisfiability
                t = -1
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
                    d = 0  # restart loop after changes
                    break
            else:
                d += 1

        # If no progress, call resolution
        if t == 0:
            t = resolution(g)
            if t != 0:
                break

        # Add a safeguard to prevent infinite loops
        if len(g) == 0:
            t = 1
            break

    if t == -1:
        print("unsatisfiable")
        return
    elif t == 1:
        print("satisfiable")
        return

g = clauses()
time_function(Davis_Putnam, g)
