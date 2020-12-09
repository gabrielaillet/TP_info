from time import *
import numpy as np
from matplotlib import pyplot as plt
from DPLL import *
from math import sqrt


def dames(n):

    literals = [i for i in range(1, n**2 + 1)]
    cnf = []

    '''Au moins 1 par ligne'''
    for i in range(n):
        clause = []
        for j in range(n):
            clause.append(literals[i*n + j])
        cnf.append(clause)

    literals_sorted_line = []
    for i in range(n):
        literals_sorted_line.append([])
        for j in range(n):
            literals_sorted_line[-1].append(literals[j*n + i])

    '''Au plus 1 par ligne'''
    for i in range(n):
        for j in range(n):
            for k in range(n-j-1):
                clause = [-literals_sorted_line[i][j], -literals_sorted_line[i][j + k + 1]]
                cnf.append(clause)

    '''Au plus 1 par diagonale'''

    for i in range(n):

        for j in range(n-i):
            for k in range(n-i-j-1):
                clause = [-literals[i+j + j*n], -literals[i+j+k+1 + (j+k+1)*n]]
                cnf.append(clause)

        for j in range(i):
            for k in range(i-j):
                clause = [-literals_sorted_line[i-j][j], -literals_sorted_line[i-j-k-1][j+k+1]]
                cnf.append(clause)

    for i in range(1, n-1):

        for j in range(n-1):
            for k in range(n-i-j-1):
                clause = [-literals_sorted_line[i+j][n-1-j], -literals_sorted_line[i+j+k+1][n-1-j-k-1]]
                cnf.append(clause)

        for j in range(i):
            for k in range(i-j):
                clause = [-literals_sorted_line[i-j][n-1-j], -literals_sorted_line[i-j-k-1][n-1-j-k-1]]
                cnf.append(clause)

    return n, literals, cnf


def time_dames_once(n):

    start = time()
    a = dames(n)
    end = time()
    exe_time = end - start
    print(len(a[2]))
    return exe_time


def time_dames_plt(n, s=1):
    x = [i for i in range(0, n, s)]
    tm = []
    for i in x:
        tm.append(time_dames_once(i))
    plt.plot(x, tm)
    plt.xlabel('n')
    plt.ylabel('Time (s)')
    plt.show()
    plt.loglog(x, tm)
    plt.show()


def create_txt_dames(n):
    filename = 'Dames ' + str(n)
    file = open(filename, 'w+')
    results = dames(n)
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

    i = 0
    while i < len(cnf_str):

        if cnf_str[i] == '[':
            cnf.append([])
            last = cnf_str[i]
            i += 1
            continue

        if last == '[':
            print('i', i)
            print(cnf_str[i])
            if cnf_str[i] != ' ' and cnf_str[i] != ',' and cnf_str[i] != '-' and cnf_str[i] != ']':
                string = cnf_str[i]
                j = i + 1
                print('j', j)
                while cnf_str[j] != ' ' and cnf_str[j] != ',' and cnf_str[j] != ']':
                    string += cnf_str[j]
                    j += 1
                    print('oui')
                if cnf_str[i - 1] == '-':
                    cnf[-1].append(-int(string))
                else:
                    cnf[-1].append(int(string))
                i += j-i
            else:
                i += 1

        else:
            i += 1

    file.close()

    return n, literals, cnf


def results_show(mod_tot):
    for mod in mod_tot:
        n = int(sqrt(len(mod)))
        chessboard = np.zeros((n, n))
        for i in range(len(mod)):
            if mod[i] is True:
                chessboard[int(i/n)][i % n] = 1
        plt.spy(chessboard)
        for i in range(n+1):
            for t in range(n * 25):
                plt.plot(i - 0.5, t / 25 - 0.5, '*', color='black')
        for i in range(n+1):
            for t in range(n * 25):
                plt.plot(t/25 - 0.5, i-0.5,'*',color = 'black')
        plt.show()


def time_dpll_dames_once(n, heuristic=1, want_mod=True):
    cnf = dames(n)[2]
    t = time()
    DPLL(cnf, heuristic, want_mod)
    t = time() - t
    return t


def time_dpll_dames_range(n, s, heuristic=1, want_mod=True):
    time_list = []
    x = []
    for k in range(0, n, s):
        print(k)
        x.append(k)
        time_list.append(time_dpll_dames_once(k, heuristic, want_mod))
    return x, time_list