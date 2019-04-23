#!/usr/bin/env python3
# Arman Siddique 115960558

import sys


def is_neg(var):
    return var[0] == '-'


def neg(var):
    if is_neg(var):
        return var[1:]
    return '-' + var


def add_edge(a, b):
    if not a in adj:
        adj[a] = []
    if not b in adj:
        adj[b] = []
    adj[a].append(b)


def add_edge_inv(a, b):
    if not a in adjInv:
        adjInv[a] = []
    if not b in adjInv:
        adjInv[b] = []
    adjInv[b].append(a)


def dfs1(u):
    if visited[u]:
        return

    visited[u] = True
    for v in adj[u]:
        dfs1(v)

    s.append(u)


def dfs2(u):
    if visitedInv[u]:
        return

    visitedInv[u] = True
    for v in adjInv[u]:
        dfs2(v)

    scc[u] = counter


def dfs3(i):
    if visitedC[i]:
        return

    visitedC[i] = True
    for j in condensed[i]:
        dfs3(j)

    s.append(i)


def solve_2sat(formula):
    global adj
    global adjInv
    global visited
    global visitedInv
    global scc
    global s
    global counter

    adj = {}
    adjInv = {}
    visited = {}
    visitedInv = {}
    scc = {}
    s = []
    counter = 1

    for i in range(len(formula)):
        if len(formula[i]) == 1:
            formula[i] = formula[i] + formula[i]

    for clause in formula:
        visited[clause[0]] = False
        visited[clause[1]] = False
        visitedInv[clause[0]] = False
        visitedInv[clause[1]] = False

        if '-' not in clause[0] and '-' not in clause[1]:
            visited['-' + clause[0]] = False
            visited['-' + clause[1]] = False
            visitedInv['-' + clause[0]] = False
            visitedInv['-' + clause[1]] = False

            add_edge('-' + clause[0], clause[1])
            add_edge_inv('-' + clause[0], clause[1])
            add_edge('-' + clause[1], clause[0])
            add_edge_inv('-' + clause[1], clause[0])
        elif '-' not in clause[0]:
            visited['-' + clause[0]] = False
            visited[clause[1][1:]] = False
            visitedInv['-' + clause[0]] = False
            visitedInv[clause[1][1:]] = False

            add_edge('-' + clause[0], clause[1])
            add_edge_inv('-' + clause[0], clause[1])
            add_edge(clause[1][1:], clause[0])
            add_edge_inv(clause[1][1:], clause[0])
        elif '-' not in clause[1]:
            visited[clause[0][1:]] = False
            visited['-' + clause[1]] = False
            visitedInv[clause[0][1:]] = False
            visitedInv['-' + clause[1]] = False

            add_edge(clause[0][1:], clause[1])
            add_edge_inv(clause[0][1:], clause[1])
            add_edge('-' + clause[1], clause[0])
            add_edge_inv('-' + clause[1], clause[0])
        else:
            visited[clause[0][1:]] = False
            visited[clause[1][1:]] = False
            visitedInv[clause[0][1:]] = False
            visitedInv[clause[1][1:]] = False

            add_edge(clause[0][1:], clause[1])
            add_edge_inv(clause[0][1:], clause[1])
            add_edge(clause[1][1:], clause[0])
            add_edge_inv(clause[1][1:], clause[0])

    for var in visited:
        if not visited[var]:
            dfs1(var)

    while not len(s) == 0:
        n = s[-1]
        s = s[:-1]

        if not visitedInv[n]:
            dfs2(n)
            counter += 1

    for var in scc:
        if '-' not in var:
            if scc[var] == scc['-' + var]:
                return None
        else:
            if scc[var] == scc[var[1:]]:
                return None

    global condensed
    condensed = {}
    global visitedC
    visitedC = {}
    for u in adj:
        for v in adj[u]:
            i = scc[u]
            j = scc[v]

            if i not in condensed:
                visitedC[i] = False
                condensed[i] = []
            if j not in condensed:
                visitedC[j] = False
                condensed[j] = []

            if j not in condensed[i]:
                condensed[i].append(j)

    for i in range(1, counter):
        if not visitedC[i]:
            dfs3(i)

    assignment = {}

    for i in s:
        for var in scc:
            if scc[var] == i and var not in assignment:
                assignment[var] = True
                if '-' not in var:
                    assignment['-' + var] = False
                else:
                    assignment[var[1:]] = False

    return assignment


def STAND_check(formula, assignment):
    if len(formula) == 0:
        return "yes"

    all_true = True
    for clause in formula:
        if len(clause) == 0:
            return "no"

        any_true = False
        all_false = True
        for var in clause:
            if var not in assignment:
                all_false = False
                continue

            any_true = any_true or assignment[var]
            all_false = all_false and not assignment[var]

        all_true = all_true and any_true
        if all_false:
            return "no"

    if all_true:
        return "yes"

    return "maybe"


def STAND_step(formula, assignment, annihilated):
    newFormula = []
    for clause in formula:
        newClause = []
        for var in clause:
            if var not in newClause:
                newClause.append(var)
        newFormula.append(newClause)
    formula = newFormula

    i = 0
    while i < len(formula):
        j = 0
        while j < len(formula[i]):
            if (formula[i][j] in assignment and assignment[formula[i][j]]) \
                    or (neg(formula[i][j]) in formula[i]):
                for var in formula[i]:
                    if var not in assignment:
                        present = False
                        for clause2 in formula:
                            if clause2 == formula[i]:
                                continue
                            for var2 in clause2:
                                if var == var2 or var == neg(var2):
                                    present = True
                                    break
                            if present:
                                break
                        if not present:
                            annihilated.append(var)
                #if formula[i][j] in assignment and assignment[formula[i][j]]:
                #    print(i, "- getting rid of clause", formula[i], "because", formula[i][j], "is", assignment[formula[i][j]], formula)
                #else:
                #    print(i, "- getting rid of clause", formula[i], "because", formula[i][j], "and", neg(formula[i][j]), "are in it", formula)
                formula = formula[:i] + formula[(i + 1):]
                i -= 1
                return [formula, assignment, annihilated]
            elif formula[i][j] in assignment and not assignment[formula[i][j]]:
                #print(i, j, formula[i], "- getting rid of literal", formula[i][j], "because it equals", assignment[formula[i][j]], formula[i])
                formula[i] = formula[i][:j] + formula[i][(j + 1):]
                j -= 1
                return [formula, assignment, annihilated]

            j += 1
        i += 1

    counts = {}
    i = 0
    for clause in formula:
        if len(clause) == 1:
            var = clause[0]
            assignment[var] = True
            assignment[neg(var)] = False
            #print(i, clause, "- assigning", var, "to", True)
            return [formula, assignment, annihilated]
        for var in clause:
            if var not in counts:
                counts[var] = 0
            counts[var] += 1
        i += 1

    for var in counts:
        if var not in assignment and neg(var) not in counts:
            assignment[var] = True
            #print("Assigning", var, "to", True, "because there is no", neg(var))
            return [formula, assignment, annihilated]

    return [formula, assignment, annihilated]


def STAND(formula, assignment):
    original_formula = formula.copy()

    old_assignment = assignment.copy()
    for var in old_assignment:
        if neg(var) in assignment and assignment[neg(var)] == assignment[var]:
            return ["no", assignment, formula]
        assignment[neg(var)] = not assignment[var]

    old_formula = []
    old_assignment = []
    annihilated = []
    old_annihilated = []
    while old_assignment != assignment or old_formula != formula or old_annihilated != annihilated:
        #print(old_assignment != assignment, old_formula != formula, old_annihilated != annihilated)
        #print("A:", annihilated)
        if len(formula) == 0:
            #print("formula is empty")
            for var in annihilated:
                if var not in assignment:
                    assignment[var] = not is_neg(var)
                    assignment[neg(var)] = is_neg(var)
            return ["yes", assignment, formula]

        for clause in formula:
            if len(clause) == 0:
                #print("clause is empty", formula)
                for var in annihilated:
                    if var not in assignment:
                        assignment[var] = not is_neg(var)
                        assignment[neg(var)] = is_neg(var)
                return ["no", assignment, formula]

        is_2sat = True
        for clause in formula:
            if len(clause) > 2:
                is_2sat = False
        if is_2sat:
            sat_res = solve_2sat(formula)

            for var in annihilated:
                if var not in assignment:
                    assignment[var] = not is_neg(var)
                    assignment[neg(var)] = is_neg(var)

            #print("SAT Formula:", formula)
            #print("SAT:", sat_res)

            if sat_res:
                for var in sat_res:
                    if var in assignment and assignment[var] != sat_res[var]:
                        return ["no", assignment, formula]
                    assignment[var] = sat_res[var]
                return ["yes", assignment, formula]
            else:
                return ["no", assignment, formula]

        old_formula = formula.copy()
        old_assignment = assignment.copy()
        old_annihilated = annihilated.copy()

        assgn_copy = assignment.copy()
        for var in assgn_copy:
            if neg(var) in assignment and assignment[neg(var)] == assignment[var]:
                for var in annihilated:
                    if var not in assignment:
                        assignment[var] = True
                return ["no", assignment, formula]
            assignment[neg(var)] = not assignment[var]

        res = STAND_step(formula, assignment, annihilated)
        formula = res[0]
        assignment = res[1]
        annihilated = res[2]

        #print(STAND_check(formula, assignment))

    for var in annihilated:
        if var not in assignment:
            assignment[var] = not is_neg(var)
            assignment[neg(var)] = is_neg(var)

    #print(formula)
    #print("A:", annihilated)
    #print(STAND_check(formula, assignment), evaluate(formula, assignment))
    return [STAND_check(original_formula, assignment), assignment, formula]


def seven_alg(formula, assignment):
    #print(formula, assignment)
    stand_sol = STAND(formula.copy(), assignment.copy())
    #print(stand_sol)
    if stand_sol[0] == "yes":
        #print(stand_sol)
        return stand_sol[1]
    elif stand_sol[0] == "no":
        return None

    assignment = stand_sol[1]
    formula = stand_sol[2]

    formula_copy = formula.copy()
    for clause in formula:
        if len(clause) == 2:
            poss = [(True, True), (True, False), (False, True)]
            for val1, val2 in poss:
                assignment[clause[0]] = val1
                assignment[neg(clause[0])] = not val1
                assignment[clause[1]] = val2
                assignment[neg(clause[1])] = not val2
                sol = seven_alg(formula_copy, assignment.copy())
                if sol:
                    return sol

            return None

    for clause in formula:
        if len(clause) == 3:
            poss = [(True, True, True), (True, True, False),
                    (True, False, True), (True, False, False),
                    (False, True, True), (False, True, False),
                    (False, False, True)]
            for val1, val2, val3 in poss:
                assignment[clause[0]] = val1
                assignment[neg(clause[0])] = not val1
                assignment[clause[1]] = val2
                assignment[neg(clause[1])] = not val2
                assignment[clause[2]] = val3
                assignment[neg(clause[2])] = not val3
                sol = seven_alg(formula_copy, assignment.copy())
                if sol:
                    return sol

            return None

    return None


def evaluate(formula, assignment):
    if not assignment:
        return None

    for var in assignment:
        for i in range(len(formula)):
            for j in range(len(formula[i])):
                if formula[i][j] == var:
                    formula[i][j] = "True" if assignment[var] else "False"

    formula_str = " and ".join(["(" + " or ".join(clause) + ")" for clause in formula])
    #print(formula_str)
    return eval(formula_str)


def main(args):
    line = input()
    formula = [clause.split(",") for clause in line.split(";")]
    solution = solve_2sat(formula)
    if solution:
        print("yes")
        vs = []
        for clause in formula:
            for var in clause:
                if '-' in var:
                    vs.append(var[1:])
                else:
                    vs.append(var)

        vs = list(set(vs))
        for i in range(len(vs) - 1):
            print(vs[i] + "=" + ("T" if solution[vs[i]] else "F"), end=",")
        print(vs[-1] + "=" + ("T" if solution[vs[-1]] else "F"))
    else:
        print("no")
    print("$")

    line = input()
    formula = [clause.split(",") for clause in line.split(";")]
    form_copy = formula.copy()
    line = input()
    assignment = {}
    for a in line.split(","):
        spl = a.split("=")
        assignment[spl[0]] = True if spl[1] == "T" else False
    stand_sol = STAND(formula, assignment)

    #print(stand_sol)
    print(stand_sol[0])
    if stand_sol[0] != "no":
        vs = []
        for clause in formula:
            for var in clause:
                if var in stand_sol[1]:
                    if is_neg(var):
                        vs.append(neg(var))
                    else:
                        vs.append(var)

        vs = list(set(vs))
        for i in range(len(vs) - 1):
            print(vs[i] + "=" + ("T" if stand_sol[1][vs[i]] else "F"), end=",")
        print(vs[-1] + "=" + ("T" if stand_sol[1][vs[-1]] else "F"))
    print("$")

    line = input()
    formula = [clause.split(",") for clause in line.split(";")]
    form_copy = formula.copy()
    solution = seven_alg(formula, {})
    if solution:
        print("yes")
        vs = []
        for clause in formula:
            for var in clause:
                if '-' in var:
                    vs.append(var[1:])
                else:
                    vs.append(var)

        vs = list(set(vs))
        for i in range(len(vs) - 1):
            print(vs[i] + "=" + ("T" if solution[vs[i]] else "F"), end=",")
        print(vs[-1] + "=" + ("T" if solution[vs[-1]] else "F"))
    else:
        print("no")

main(sys.argv)
