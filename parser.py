import re
import json
import csv
import ktrain
import os
import bs4
import lxml
from bs4 import BeautifulSoup as bs

predictor = ktrain.load_predictor('classification_model')

# comparison words
more_list = ['more', 'after', 'later', 'ahead', 'longer', 'taller', 'older', 'larger', 'farther', 'better', 'quicker', 'warmer', 'wider', 'further', 'thicker', 'greater', 'pricier', 'hotter', 'deeper', 'faster', 'heavier', 'richer', 'higher', 'louder']
less_list = ['fewer', 'before', 'less', 'behind', 'shorter', 'younger', 'smaller', 'closer', 'colder', 'earlier', 'tighter', 'slower', 'cooler', 'short', 'lesser', 'lower', 'quitier']

ordinals = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
numerical = {
    'hundred':100,
    'thousand':1000,
    'million':1000000
}

# get heideltag values of a text
def get_heideltag(text):
    with open("input.txt", 'w') as fl:
        fl.write(text)
    
    os.system("java -jar de.unihd.dbs.heideltime.standalone.jar input.txt > output.xml")

    content = []
    # Read the XML file
    with open("output.xml", "r") as file:
        # Read each line in the file, readlines() returns a list of lines
        content = file.readlines()
        # Combine the lines in the list into a string
        content = "".join(content)
        bs_content = bs(content, "lxml")

    if not bs_content.find("timex3"):
        return "", ""
    
    tp = bs_content.find("timex3").attrs['type']
    value = bs_content.find("timex3").attrs['value']

    return tp, value


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


# parse the comparison quantifier from a clue
def parse_comp_quant(date_type, clue):
    quant = ''

    time_fractions = {
        'half an hour': 30,
        'half-hour': 30,
        'quarter of an hour': 15,
        'quarter-hour': 15
    }
   
    for k, v in time_fractions.items():
        if k in clue:
            quant = v
            break 

    tp, val = get_heideltag(clue)
    if quant == '' and tp == "DURATION":
        if date_type == "DAYS":
            if val[-1] == "W":
                quant = 7 * int(val[1:-1])
            elif val[-1] == "D":
                quant = int(val[1:-1])

        elif date_type == "MONTHS":
            if val[-1] == "M":
                quant = int(val[1:-1])
        
        elif date_type == "YEARS":
            if val[-1] == "Y":
                quant = int(val[1:-1])
            elif val[-2:] == "DE":
                quant = 10 * int(val[1:-2])
            elif val[-2:] == "CE":
                quant = 100 * int(val[1:-2])

        elif date_type == "TIME":
            if val[-1] == "H":
                quant = int(val[2:-1]) * 60
            elif val[-1] == 'M':
                quant = int(val[2:-1])
                

    if quant == '' and re.search('\s\d+', clue):
        quant = int(re.findall('\s\d+', clue)[0])
        for key, value in numerical.items():
            if re.search(key, clue):
                quant *= value
    
    if quant == '':
        return ''
    
    return ', ' + str(quant)


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
        date_type = ""

        print("Processing:", fl + st)
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

                    # check if an instance is a numerical value
                    quantifier = ''
                    if i in ordinals:
                        quantifier = ordinals.index(i) + 1
                    if quantifier == '':
                        tp, val = get_heideltag(i[0].upper() + i[1:])
                        if tp == "DATE":
                            if len(val) == 7 and val[-2:].isdigit():
                                date_type = "MONTHS"
                                quantifier = int(val[-2:])
                            elif len(val) == 10:
                                date_type = "DAYS"
                            elif len(val) == 4:
                                date_type = "YEARS"
                        elif tp == "TIME":
                            date_type = "TIME"
                            # convert to minutes
                            if i == "12:00pm":
                                quantifier = 720
                            elif i == "00:00am":
                                quantifier = 0
                            else:
                                quantifier = int(val[-5:-3]) * 60 + int(val[-2:])
                    
                    if quantifier == '' and len(re.findall("\d*\.\d+|\d+", i)) != 0:
                        quantifier = float(re.findall("\d*\.\d+|\d+", i)[0])
                        if len(i.split()) == 2 and i.split()[1] in numerical:
                            quantifier *= numerical[i.split()[1]]
                        quantifier = int(quantifier)
                    
                    if quantifier == '':
                        non_compared_list.add(letters[j])
                    else:
                        instance2quant[letters[j]+str(k)] = quantifier
                    
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
                desc += parse_comp_quant(date_type, j)

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