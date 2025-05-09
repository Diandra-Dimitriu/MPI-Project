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
    timeout_seconds = 10  # Maximum time allowed for resolution
    start_time = time.time()  # Start a timer to enforce a timeout

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

        # Check for timeout
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout_seconds:
            print(f"Result: Timeout reached after {timeout_seconds} seconds. Terminating to prevent hanging.")
            return 1

    if t == 0: # unsatisfiable
        print("unsatisfiable")
        return -1
    elif t == -1: # unknown
        print("satisfiable (unknown)")
        return 0

g = clauses()
time_function(resolution, g)
