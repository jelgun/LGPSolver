import re
import json
import csv
import ktrain

predictor = ktrain.load_predictor('classification_model')

# comparison words
more_list = ['more', 'after', 'later', 'ahead', 'longer', 'taller', 'older', 'larger', 'farther', 'better', 'quicker', 'warmer', 'wider', 'further', 'thicker', 'greater', 'pricier', 'hotter', 'deeper', 'faster', 'heavier', 'richer', 'higher', 'louder']
less_list = ['fewer', 'before', 'less', 'behind', 'shorter', 'younger', 'smaller', 'closer', 'colder', 'earlier', 'tighter', 'slower', 'cooler', 'short', 'lesser', 'lower', 'quitier']

ordinals = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
numerical = {
    'hundred':100,
    'thousand':1000,
    'million':1000000
}


# find the compared category given non-compared categories
def get_compared(non_compared_list):
    categories = ['C', 'B', 'A']
    for i in categories:
        if i not in non_compared_list:
            return i
    return 'A'


# classify the given clue using the trained model
def classify_clue(clue):
    clue_class = predictor.predict([clue])[0]
    
    if clue_class == '0':
        desc = 'is('
    elif clue_class == '1':
        desc = 'either('
    elif clue_class == '2':
        desc = 'comp('
    elif clue_class == '3':
        desc = 'diff('
    else:
        desc = 'pairdiff('

    return desc


# parse the given puzzle set
def parse_puzzle_set(fl, length, ch = 0):
    for docnum in range(1, length + 1):
        st = str(docnum)

        if ch == 0 and docnum < 10:
            st = '0' + st
        filename = fl + st + "/entities.txt"
        dct = {}
        instance2quant = {}
        non_compared_list = set()

        # parse categories
        with open(filename) as f:
            lines = f.read().splitlines()
            # map each instance to [A-C][0-3] pairs
            letters = ['A', 'B', 'C']
            for j in range(3):
                k = 0
                arr = lines[j+2].split(',')
                if len(arr) > 4:
                    arr = lines[j+2].split(' ')

                for i in arr:
                    i = i.strip().lower()
                    i = i.replace(',', '')
                    i = re.sub('[$]+', '', i)
                    try:
                        quantifier = float(re.findall("\d*\.\d+|\d+", i)[0])
                        if len(i.split()) == 2 and i.split()[1] in numerical:
                            quantifier *= numerical[i.split()[1]]
                        instance2quant[letters[j]+str(k)] = int(quantifier)
                    except:
                        if i in ordinals:
                            instance2quant[letters[j]+str(k)] = ordinals.index(i) + 1
                        elif i in months:
                            instance2quant[letters[j]+str(k)] = months.index(i) + 1
                        else:
                            non_compared_list.add(letters[j])

                    dct[letters[j]+str(k)] = i
                    k += 1

        # parse clues
        filename = fl + st + "/clues.txt"
        with open(filename) as f:
            clues = f.read().splitlines()
            relationships = []
            
            for j in clues:
                j = j.lower()
                j = re.sub('[$]+', '', j)
                j = j.replace(',', '')
                j = j.replace(';', '')
                # replace each instance with corresponding pair
                for key in sorted(dct, key=lambda k: len(dct[k]), reverse=True):
                    try:
                        idx = j.index(dct[key])
                        if idx > 0 and ((j[idx-1] >= 'a' and j[idx-1] <= 'z') or (j[idx-1] >= 'A' and j[idx-1] <= 'Z')):
                            continue
                    except:
                        pass

                    j_upd = j.replace(dct[key], key)
                    if (dct[key][-1] == 's' and j_upd == j):
                        j = j.replace(dct[key][:-1], key)
                    else:
                        j = j_upd
                        
                    j = j.replace(key+'s', key)
                
                desc = classify_clue(j)

                comparison = ""
                for i in more_list:
                    if re.search(i, j):
                        comparison = '>'
                        break
                for i in less_list:
                    if re.search(i, j):
                        comparison = '<'
                        break
                
                res = re.findall('[A-Z]\d', j)
                if comparison != "" and len(res) == 3:
                    desc += "{}, {}, {}".format(res[0], res[2], instance2quant[res[1]])
                    desc += ', ' + comparison
                    relationships.append(desc+')\n')
                    non_compared_list.add(res[0][0]) 
                    non_compared_list.add(res[2][0])
                    continue
                else:
                    for i in res[:-1]:
                        desc += i+', '
                
                desc += res[-1]
                if re.search('\s\d+', j):
                    quant = int(re.findall('\s\d+', j)[0])
                    for key, value in numerical.items():
                        if re.search(key, j):
                            quant *= value
                    
                    desc += ', ' + str(quant)

                if comparison != "":
                    desc += ', ' + comparison
                    non_compared_list.add(res[0][0])
                    non_compared_list.add(res[1][0])

                relationships.append(desc+')\n')

            with open(fl + st + "/parseActual.txt", "w") as f:
                for i in relationships:
                    f.write(i)

            compared_category = get_compared(non_compared_list)
            instance2quant['compared'] = compared_category
            json.dump(instance2quant, open(fl + st + '/quant.json', 'w'))
            json.dump(dct, open(fl + st + '/label.json', 'w'))


def parse():
    parse_puzzle_set("data/puzzles_extra/test/puzzle_", 50, ch = 1)
    parse_puzzle_set("data/puzzles_extra/test_na/puzzle_", 50, ch = 1)
    parse_puzzle_set("data/puzzlesEasy/puzzle", 28)
    parse_puzzle_set("data/puzzlesModerate/puzzle", 20)
    parse_puzzle_set("data/puzzlesChallenging/puzzle", 20)


parse()