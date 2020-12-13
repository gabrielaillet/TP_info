from time import *
from matplotlib import pyplot as plt
from DPLL import *


def pigeons(n):
    literals = [i for i in range(1, n*(n-1)+1)]
    literals_sorted = []
    cnf = []

    for i in range(n):
        clause = []
        for j in range(n-1):
            clause.append(literals[i*(n-1) + j])
        cnf.append(clause)

    for i in range(n-1):
        cage = []
        for j in range(n):
            cage.append(literals[j*(n-1) + i])
        literals_sorted.append(cage)

    for i in range(n):
        for j in range(n-1):
            for k in range(n-j-2):
                clause = [-literals[i*(n-1) + j], -literals[i*(n-1) + j + k + 1]]
                cnf.append(clause)

    for i in range(n-1):
        for j in range(n):
            for k in range(n-j-1):
                clause = [-literals_sorted[i][j], -literals_sorted[i][j + k + 1]]
                cnf.append(clause)

    return n, literals, cnf


def time_pigeons_once(n):

    start = time()
    a = pigeons(n)
    end = time()
    exe_time = end - start
    print(len(a[2]))
    return exe_time


def time_pigeons_plt(n, s=1):
    x = [i for i in range(0, n, s)]
    tm = []
    for i in x:
        tm.append(time_pigeons_once(i))
    plt.plot(x, tm)
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.show()
    plt.loglog(x, tm)
    plt.show()


def create_txt_pigeons(n):
    filename = 'Pigeons ' + str(n)
    file = open(filename, 'w+')
    results = pigeons(n)
    file.write(str(results[0]) + '\n' + str(results[1]) + '\n' + str(results[2]))
    file.close()


def read(filepath):
    file = open(filepath, 'r')
    content = file.readlines()

    n = int(content[0])

    literals = content[1]

    cnf_str = content[2]
    cnf_str = cnf_str[1:]
    cnf_str = cnf_str[:-1]
    cnf = []
    last = ''

    for i in range(len(cnf_str)):

        if cnf_str[i] == '[':
            cnf.append([])
            last = cnf_str[i]
            continue

        if cnf_str[i] == ']':
            last = cnf_str[i]
            continue

        if last == '[':
            if cnf_str[i] != ' ' and cnf_str[i] != ',' and cnf_str[i] != '-':
                if cnf_str[i - 1] == '-':
                    cnf[-1].append(-int(cnf_str[i]))
                else:
                    cnf[-1].append(int(cnf_str[i]))

    file.close()

    return n, literals, cnf


def time_dpll_pigeon_once(n, heuristic=1, want_mod=True):
    cnf = pigeons(n)[2]
    t = time()
    DPLL(cnf, heuristic, want_mod)
    t = time() - t
    return t


def time_dpll_pigeons_range(n, s, heuristic=1, want_mod=True):
    time_list = []
    x = []
    for k in range(0, n, s):
        x.append(k)
        time_list.append(time_dpll_pigeon_once(k, heuristic, want_mod))
    return x, time_list



a = pigeons(4)
c = a[1]
b = a[2]
print(len(a[1]))
a = DPLL(b,2,want_mod=True)
print(a[1])