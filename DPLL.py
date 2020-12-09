from copy import deepcopy


def create_vector(Cnf):
    absolute_max = 0
    for Cn in Cnf:
        for lit in Cn:
            if abs(lit) > absolute_max:
                absolute_max = abs(lit)

    value_vector = [None] * (absolute_max + 1)
    return value_vector[1:]


def find_mod(true_false_None_list, mod=None):
    if mod is None:
        mod = []
    current_true_false = true_false_None_list
    index_chart = []
    for index in range(len(true_false_None_list)):
        if true_false_None_list[index] is None:
            index_chart.append(index)
    n = len(index_chart)
    if n == 0:
        mod += [current_true_false]
        return mod
    for i in range(2 ** n):
        number = bin(i)
        number = number[2:]
        if (len(number)) < n:
            for index1 in range(n - (len(number))):
                current_true_false[index_chart[index1]] = False

            for index2 in range(len(number)):

                if number[index2] == '1':
                    current_true_false[index_chart[(n - len(number)) + index2]] = True
                if number[index2] == '0':
                    current_true_false[index_chart[(n - len(number)) + index2]] = False
        else:
            for index2 in range(len(number)):

                if number[index2] == '1':
                    current_true_false[index_chart[(n - len(number)) + index2]] = True
                if number[index2] == '0':
                    current_true_false[index_chart[(n - len(number)) + index2]] = False

        mod += [current_true_false]
        current_true_false = deepcopy(true_false_None_list)
    return mod


def simplify_clause_literal(cnf, mono_lit):
    new_cnf = []
    for Cn_1_index in range(len(cnf)):
        new_Cn = []
        is_continue = False
        for literal_index in range(len(cnf[Cn_1_index])):
            if cnf[Cn_1_index][literal_index] == -mono_lit:
                continue
            elif cnf[Cn_1_index][literal_index] == mono_lit:
                is_continue = True
                break
            new_Cn += [cnf[Cn_1_index][literal_index]]
        if is_continue:
            continue
        new_cnf += [new_Cn]
    return new_cnf


def assign_value(value_vector, mono_lit):
    if mono_lit < 0:
        value_vector[-mono_lit - 1] = False
    if mono_lit > 0:
        value_vector[mono_lit - 1] = True

    return value_vector


def DPLL(Cnf, heuristics=1, want_mod=True):
    mod = []
    new_cnf = Cnf

    if not new_cnf:
        if want_mod:
            return mod
        else:
            return False

    back_track_list = []
    back_track_litt = []
    back_track_val = []
    back_track_list.append(new_cnf)
    value_vector = create_vector(Cnf)
    as_been_back_track = []
    back_track_val += [value_vector.copy()]

    while (new_cnf != []) and ([] not in new_cnf):

        check = False

        '''Mono-literal rule'''
        for Cn in new_cnf:
            if len(Cn) == 1:
                mono_lit = Cn[0]
                value_vector = assign_value(value_vector, mono_lit)
                new_cnf = simplify_clause_literal(new_cnf, mono_lit)
                if (new_cnf != []) and ([] not in new_cnf):
                    back_track_list += [new_cnf]
                    back_track_val += [value_vector.copy()]
                back_track_litt += [mono_lit]

                check = True
                break
        if check:
            continue

        """pure-literal"""
        list_lit = set()
        for cn in new_cnf:
            for lit in cn:
                if lit not in list_lit:
                    list_lit.add(lit)
        for lit in list_lit:
            if -lit in list_lit:
                continue
            else:
                value_vector = assign_value(value_vector, lit)
                new_cnf = simplify_clause_literal(new_cnf, lit).copy()
                if (new_cnf != []) and ([] not in new_cnf):
                    back_track_list += [new_cnf]
                    back_track_val += [value_vector.copy()]
                back_track_litt += [lit]

                check = True
                break
        if check:
            continue

        if heuristics is None:

            chosen_lit = new_cnf[0][0]

        else:
            '''Count for heuristics'''
            list_lit2 = []
            for cn in new_cnf:
                for lit in cn:
                    list_lit2.append(lit)
            list_lit2.sort()
            list_tuple = [[list_lit2[0], 0]]
            for i in range(len(list_lit2)):
                if list_lit2[i] != list_tuple[-1][0]:
                    list_tuple.append([list_lit2[i], 1])
                else:
                    list_tuple[-1][1] += 1
            '''Heuristics'''
            max_value = 0
            chosen_lit = None
            if heuristics == 1:
                for t in list_tuple:
                    if (t[0] > 0) and (t[1] > max_value):
                        max_value = t[1]
                        chosen_lit = t[0]

            if heuristics == 2:
                for t in list_tuple:
                    if (t[0] < 0) and (t[1] > max_value):
                        max_value = t[1]
                        chosen_lit = t[0]

            if chosen_lit is None:
                chosen_lit = list_tuple[0][0]

        value_vector = assign_value(value_vector, chosen_lit)
        new_cnf = simplify_clause_literal(new_cnf, chosen_lit).copy()
        if (new_cnf != []) and ([] not in new_cnf):
            back_track_list += [new_cnf]
            back_track_val += [value_vector.copy()]
        back_track_litt += [chosen_lit]

    if want_mod or ([] in new_cnf):
        while len(back_track_litt) != 0:
            check = False

            if not new_cnf:
                if not want_mod:
                    return True
                mod = find_mod(value_vector, mod)
                check = True
                current_lit = back_track_litt.pop()
                if abs(current_lit) not in as_been_back_track:
                    a = back_track_list.pop()
                    current_val = back_track_val.pop()
                    back_track_list += [a]
                    back_track_val += [current_val]
                    new_cnf = simplify_clause_literal(a, -current_lit)
                    value_vector = assign_value(current_val, -current_lit)
                    back_track_litt += [-current_lit]
                    if (new_cnf != []) and ([] not in new_cnf):
                        back_track_list += [new_cnf]
                        back_track_val += [value_vector.copy()]
                    as_been_back_track += [abs(current_lit)]
                else:
                    as_been_back_track.remove(abs(current_lit))
                    back_track_list.pop()
                    back_track_val.pop()
                    new_cnf = [[]]

            if check:
                continue

            if [] in new_cnf:
                check = True
                current_lit = back_track_litt.pop()
                if abs(current_lit) not in as_been_back_track:
                    a = back_track_list.pop()
                    current_val = back_track_val.pop()
                    back_track_list += [a]
                    back_track_val += [current_val]
                    new_cnf = simplify_clause_literal(a, -current_lit)
                    value_vector = assign_value(current_val, -current_lit)
                    back_track_litt += [-current_lit]
                    if (new_cnf != []) and ([] not in new_cnf):
                        back_track_list += [new_cnf]
                        back_track_val += [value_vector.copy()]
                    as_been_back_track += [abs(current_lit)]
                else:
                    as_been_back_track.remove(abs(current_lit))
                    back_track_list.pop()
                    back_track_val.pop()
                    new_cnf = [[]]
            if check:
                continue

            '''Mono-literal rule'''
            for Cn in new_cnf:
                if len(Cn) == 1:
                    mono_lit = Cn[0]
                    value_vector = assign_value(value_vector, mono_lit)
                    new_cnf = simplify_clause_literal(new_cnf, mono_lit)
                    if (new_cnf != []) and ([] not in new_cnf):
                        back_track_list += [new_cnf]
                        back_track_val += [value_vector.copy()]
                    back_track_litt += [mono_lit]

                    check = True
                    break
            if check:
                continue

            """pure-literal"""
            list_lit = set()
            for cn in new_cnf:
                for lit in cn:
                    if lit not in list_lit:
                        list_lit.add(lit)
            for lit in list_lit:
                if -lit in list_lit:
                    continue
                else:
                    value_vector = assign_value(value_vector, lit)
                    new_cnf = simplify_clause_literal(new_cnf, lit).copy()
                    if (new_cnf != []) and ([] not in new_cnf):
                        back_track_list += [new_cnf]
                        back_track_val += [value_vector.copy()]
                    back_track_litt += [lit]

                    check = True
                    break
            if check:
                continue

            if heuristics is None:

                chosen_lit = new_cnf[0][0]
            else:
                '''Count for heuristics'''
                list_lit2 = []
                for cn in new_cnf:
                    for lit in cn:
                        list_lit2.append(lit)
                list_lit2.sort()
                list_tuple = [[list_lit2[0], 0]]
                for i in range(len(list_lit2)):
                    if list_lit2[i] != list_tuple[-1][0]:
                        list_tuple.append([list_lit2[i], 1])
                    else:
                        list_tuple[-1][1] += 1
                '''Heuristics'''
                max_value = 0
                chosen_lit = None
                if heuristics == 1:
                    for t in list_tuple:
                        if (t[0] > 0) and (t[1] > max_value):
                            max_value = t[1]
                            chosen_lit = t[0]

                if heuristics == 2:
                    for t in list_tuple:
                        if (t[0] < 0) and (t[1] > max_value):
                            max_value = t[1]
                            chosen_lit = t[0]

                if chosen_lit is None:
                    chosen_lit = list_tuple[0][0]

            value_vector = assign_value(value_vector, chosen_lit)
            new_cnf = simplify_clause_literal(new_cnf, chosen_lit).copy()
            if (new_cnf != []) and ([] not in new_cnf):
                back_track_list += [new_cnf]
                back_track_val += [value_vector.copy()]
            back_track_litt += [chosen_lit]
        if not want_mod:
            return False
        return mod
    else:
        return True


def text_mod(mod):
    filename = 'Results'
    file = open(filename, 'w+')
    for k in range(len(mod)):
        file.write('Model' + str(k) + ' : ' + str(mod[k]) + '\n')
    file.close()