#!/usr/bin/env python3
# Arman Siddique 115960558

import sys

# Data structures for 2SAT
adj = {}
adjInv = {}
visited = {}
visitedInv = {}
scc = {}


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
    global s
    s = []
    global counter
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


main(sys.argv)
