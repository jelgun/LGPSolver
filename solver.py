import json
import shutil
import os
from pyswip import Prolog
prolog = Prolog()


def is_rel(line, instance2quant):
    if line[1][0] == 'B':
        line[0], line[1] = line[1], line[0]
    if line[0][0] == 'B':
        statement = line[1][0] + line[0][1] + ' = '
        if line[1][0] == 'C':
            return statement + 'c' + line[1][1]
        else:
            return statement + str(int(instance2quant[line[1]]))
    else:
        if line[1][0] == 'A':
            line[0], line[1] = line[1], line[0]
        return 'member([' + str(int(instance2quant[line[0]])) +', c'+ line[1][1] + '], All)'


def either_rel(line, instance2quant):
    A = is_rel([line[0], line[1]], instance2quant)
    B = is_rel([line[0], line[2]], instance2quant)

    return 'and([or([{},{}]), not(and([{},{}]))])'.format(A, B, A, B)


def pairdiff_rel(line, instance2quant):
    A = is_rel([line[0], line[2]], instance2quant)
    B = is_rel([line[1], line[3]], instance2quant)
    C = is_rel([line[0], line[3]], instance2quant)
    D = is_rel([line[1], line[2]], instance2quant)

    return 'or([and([{},{}]),and([{},{}])])'.format(A, B, C, D)


def diff_rel(line, instance2quant):
    res = []
    for i in range(len(line)):
        for j in range(i + 1, len(line)):
            if line[i][0] != line[j][0]:
                rel = is_rel([line[i], line[j]], instance2quant)
                res.append('not({})'.format(rel))

    return res


def comp_rel(line, instance2quant):
    res = []
    if line[0][0] == 'B':
        A = 'A' + line[0][1]
    else:
        A = 'C{}_val'.format(line[0][1])
        res.append('member([C{}_val, c{}], All)'.format(line[0][1], line[0][1]))

    if line[1][0] == 'B':
        B = 'A' + line[1][1]
    else:
        B = 'C{}_val'.format(line[1][1])
        res.append('member([C{}_val, c{}], All)'.format(line[1][1], line[1][1]))

    if len(line) == 3:
        res.append(A + line[-1] + B)
    else:
        if line[-1] == '>':
            t = A + '-' + B
        else:
            t = B + '-' + A
        res.append(t + '=:=' + line[2])

    return res


def solve_puzzle_set(fl, length, ch = 0):
    for docnum in range(1, length + 1):
        st = str(docnum)

        if ch == 0 and docnum < 10:
            st = '0' + st
        instance2quant = json.load(open(fl + st + '/quant.json'))
        filename = fl + st + "/parseActual.txt"
        
        with open(filename) as f:
            lines = f.read().splitlines()

            compared = instance2quant["compared"]
            if compared != 'A':
                new_instance2quant = {}
                for key, value in instance2quant.items():
                    if key[0] == compared:
                        new_instance2quant['A' + key[1]] = value
                instance2quant = new_instance2quant
            
            for key, value in instance2quant.items():
                if key != 'compared':
                    instance2quant[key] = int(value)
            
            shutil.copy(os.getcwd() + '/solve.pl', os.getcwd() + '/' + fl + st + '/prolog-puzzle.pl')
            t = 'all_members([{}, {}, {}, {}], [{}, {}, {}, {}])'.format(
                instance2quant['A0'],
                instance2quant['A1'],
                instance2quant['A2'],
                instance2quant['A3'],
                'A0', 'A1', 'A2', 'A3'
            )
            with open(os.getcwd() + '/' + fl + st + '/prolog-puzzle.pl', 'a') as f:
                f.write(t + ',\n')
            
            for line in lines:
                rel = line[0]
                line = line[line.index('(') + 1:line.index(')')].split(',')
                line = [i.strip() for i in line]

                if compared != 'A':
                    for i in range(len(line)):
                        if line[i][0] == 'A':
                            line[i] = compared + line[i][1]
                        elif line[i][0] == compared:
                            line[i] = 'A' + line[i][1]
                
                with open(os.getcwd() + '/' + fl + st + '/prolog-puzzle.pl', 'a') as f:
                    try:
                        if rel == 'i':
                            f.write(is_rel(line, instance2quant) + ',\n')
                        elif rel == 'e':
                            f.write(either_rel(line, instance2quant) + ',\n')
                        elif rel == 'p':
                            f.write(pairdiff_rel(line, instance2quant) + ',\n')
                        elif rel == 'd':
                            for t in diff_rel(line, instance2quant):
                                f.write(t + ',\n')
                        else:
                            for t in comp_rel(line, instance2quant):
                                f.write(t + ',\n')
                    except:
                        pass

        with open(os.getcwd() + '/' + fl + st + '/prolog-puzzle.pl', 'rb+') as f:
            f.seek(-2, os.SEEK_END)
            f.truncate()
        
        with open(os.getcwd() + '/' + fl + st + '/prolog-puzzle.pl', 'a') as f:
            f.write('.\n')
        
        prolog.consult(fl + st + '/prolog-puzzle')
        try:
            res = list(prolog.query("solve(B0, B1, B2, B3)"))
            
            k = [0, 1, 2]
            ans = [[], [], []]

            for i in res:
                for key, value in i.items():
                    ans[1].append(key)
                    for key2, value2 in instance2quant.items():
                        if value2 == value[0]:
                            ans[0].append(key2)
                            break
                    ans[2].append('C' + str(value[1])[1])
            
            try:
                if compared == 'C':
                    k[0], k[2] = k[2], k[0]
                    for i in range(4):
                        ans[0][i] = 'C' + ans[0][i][1]
                        ans[2][i] = 'A' + ans[2][i][1]
                elif compared == 'B':
                    k[0], k[1] = k[1], k[0]
                    for i in range(4):
                        ans[0][i] = 'B' + ans[0][i][1]
                        ans[1][i] = 'A' + ans[1][i][1]
            except:
                pass

            dct = json.load(open(fl + st + '/label.json'))
            with open(os.getcwd() + '/' + fl + st + '/answerActual.txt', 'w') as f:
                for j in range(4):
                    try:
                        f.write("{}, {}, {}\n".format(dct[ans[k[0]][j]], dct[ans[k[1]][j]], dct[ans[k[2]][j]]))
                    except:
                        pass
        except:
            pass


def get_acc_puzzle_set(fl, length, ch = 0):
    correct = 0
    for docnum in range(1, length + 1):
        st = str(docnum)

        if ch == 0 and docnum < 10:
            st = '0' + st

        filename = fl + st + "/answerActual.txt"
        answerActual = []
        with open(filename) as f:
            lines = f.read().splitlines()
            for i in lines:
                instances = i.split(',')
                answerActual.append([j.strip().lower() for j in instances])
        if len(answerActual) > 0:
            correct += 1
        else:
            print(fl + str(docnum))
    
    return correct, length


def solve():
    solve_puzzle_set("data/puzzlesEasy/puzzle", 28)
    solve_puzzle_set("data/puzzlesModerate/puzzle", 20)
    solve_puzzle_set("data/puzzlesChallenging/puzzle", 20)
    solve_puzzle_set("data/puzzles_extra/test/puzzle_", 50, ch=1)
    solve_puzzle_set("data/puzzles_extra/test_na/puzzle_", 50, ch=1)


def solver_acc():
    correct = 0
    total = 0

    easy_correct, easy_total = get_acc_puzzle_set("data/puzzlesEasy/puzzle", 28)
    moderate_correct, moderate_total = get_acc_puzzle_set("data/puzzlesModerate/puzzle", 20)
    hard_correct, hard_total = get_acc_puzzle_set("data/puzzlesChallenging/puzzle", 20)
    extra_test_correct, extra_test_total = get_acc_puzzle_set("data/puzzles_extra/test/puzzle_", 50, ch=1)
    extra_test_na_correct, extra_test_na_total = get_acc_puzzle_set("data/puzzles_extra/test_na/puzzle_", 50, ch=1)

    correct = easy_correct + moderate_correct + hard_correct + extra_test_correct + extra_test_na_correct
    total = easy_total + moderate_total + hard_total + extra_test_total + extra_test_na_total
    
    return correct, total


solve()
print(solver_acc())
