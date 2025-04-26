import sys
import os
import re
import json
import Levenshtein
from multiprocessing import Pool

with open("counter.json", "r", encoding="utf-8") as dict_json:
    d = json.load(dict_json)
   
def change_word(word):
    threshold = 20 #up to you
    k = len(word)
    kp1 = str(k+1)
    kp2 = str(k+2)
    km1 = str(k-1)
    km2 = str(k-2)
    k = str(k)
    d[kp1] = d.get(kp1, dict())
    d[kp2] = d.get(kp2, dict())
    d[km1] = d.get(km1, dict())
    d[km2] = d.get(km2, dict())
    res = word
    count = 0
    for key in d[km1].keys():
        if (d[km1][key] > threshold):
                dis = Levenshtein.distance(word, key)
                if dis == 1:
                        return key
                if dis == 2:
                        res = key
    for key in d[k].keys():
        if (d[k][key] > threshold):
                dis = Levenshtein.distance(word, key)
                if dis == 1:
                        return key
                if dis == 2:
                        res = key
        
    for key in d[kp1].keys():
        if (d[kp1][key] > threshold):
                dis = Levenshtein.distance(word, key)
                if dis == 1:
                        return key
                if dis == 2:
                        res = key
    if res != word:
            return res
    for key in d[km2].keys():
        if (d[km2][key] > threshold and Levenshtein.distance(word, key) == 2):
            return key
    for key in d[km1].keys():
        if (d[km1][key] > threshold and Levenshtein.distance(word, key) == 2):
            return key
    for key in d[k].keys():
        if (d[k][key] > threshold and Levenshtein.distance(word, key) == 2):
            return key
    for key in d[kp1].keys():
        if (d[kp1][key] > threshold and Levenshtein.distance(word, key) == 2):
            return key
    for key in d[kp2].keys():
        if (d[kp2][key] > threshold and Levenshtein.distance(word, key) == 2):
            return key
    return word

def levi(file):
    path1 = '/tmp/iaindenbaum/test1/'
    path2 = '/tmp/iaindenbaum/res1/'
    file_path = os.path.join(path1, file)
    new_path = os.path.join(path2, file)

    count = 0
    text = None
    with open(file_path, 'r', encoding = 'utf-8') as filei:
        text = filei.readlines()
    lemm_text = "" #сюда кладется новый текст
    for line in text:
        lemm_line = "" #сюда кладется новая строка
        split_line = line.replace('.', ' . ')
        split_line = split_line.replace('?', ' ? ')
        split_line = split_line.replace('!', ' ! ')
        split_line = split_line.split()
        for i in range (len(split_line)):
            if (count > 10000):
                print("DIRTY", file_path, flush = True)
                return
            if (split_line[i] == '.' or split_line[i] == '?' or split_line[i] == '!'):
                lemm_line += split_line[i]
                lemm_line += " "
                continue
            split_line[i] = split_line[i].replace('-','')
            k = len(split_line[i])
            if (str(k) not in d):
                count += 1
            elif (split_line[i] not in d[str(k)]):
                count += 1
                new_word = change_word(split_line[i])
                #print(split_line[i], new_word)
                lemm_line += new_word
            elif (k > 2 and d[str(k)][split_line[i]] < 7): #kill it
                count += 1
                new_word = change_word(split_line[i])
                #print(split_line[i], new_word)
                lemm_line += new_word
            else:
                lemm_line += split_line[i]
            lemm_line += " "
        lemm_text += lemm_line
        lemm_text += '\n' #перенос строки
    os.remove(file_path)
    with open(new_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(lemm_text)
        print(new_path, count, flush = True)
                   
        
if __name__ == "__main__":

    print(os.environ.get('OMP_THREAD_LIMIT'))

    before_path = '/tmp/iaindenbaum/test1/'
    files = os.listdir(before_path)
    files = sorted(files)
    num_proc = 44
    selected = files[4232:4848]

    p = Pool(num_proc)
    p.map(levi, selected)

