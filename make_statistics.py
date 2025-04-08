import sys
import os
import re
import json
import pickle

nouns_d = set()
verbs_d = set()
adjectives_d = set()
adverbs_d = set()

with open('neuter_nouns.txt', 'r', encoding='utf-8') as f1:
    with open('female_nouns.txt', 'r', encoding='utf-8') as f2:
        with open('male_nouns.txt', 'r', encoding='utf-8') as f3:
            with open('nouns.txt', 'r', encoding='utf-8') as f4:
                with open('verbs.txt', 'r', encoding='utf-8') as f5:
                    with open('adjectives.txt', 'r', encoding='utf-8') as f6:
                        text1 = f1.read()
                        text2 = f2.read()
                        text3 = f3.read()
                        text4 = f4.read()
                        text5 = f5.read()
                        text6 = f6.read()
                        
                        text_clean1 = re.sub(r'[\u200B\u2060\uFEFF]', '', text1)
                        text_clean2 = re.sub(r'[\u200B\u2060\uFEFF]', '', text2)
                        text_clean3 = re.sub(r'[\u200B\u2060\uFEFF]', '', text3)
                        text_clean4 = re.sub(r'[\u200B\u2060\uFEFF]', '', text4)
                        text_clean5 = re.sub(r'[\u200B\u2060\uFEFF]', '', text5)
                        text_clean6 = re.sub(r'[\u200B\u2060\uFEFF]', '', text6)
                        
                        words1 = set(word.strip(".,!?\"'") for word in text_clean1.split())
                        words2 = set(word.strip(".,!?\"'") for word in text_clean2.split())
                        words3 = set(word.strip(".,!?\"'") for word in text_clean3.split())
                        words4 = set(word.strip(".,!?\"'") for word in text_clean4.split())
                        words5 = set(word.strip(".,!?\"'") for word in text_clean5.split())
                        words6 = set(word.strip(".,!?\"'") for word in text_clean6.split())
                        
                        nouns_d = words1 | words2 | words3 | words4
                        verbs_d = words5
                        adjectives_d = words6
                    
                        
with open('adverbs.txt', 'r', encoding='utf-8') as f7:
    text7 = f7.read()
    text_clean7 = re.sub(r'[\u200B\u2060\uFEFF]', '', text7)
    words7 = set(word.strip(".,!?\"'") for word in text_clean7.split())
    adverbs_d = words7    
    
verbs = set()
for verb in verbs_d:
    word = verb.replace('פ','פֿ')
    word = word.replace('וֹ','וי')
    word = word.replace('בּ','ב')
    if word.endswith('ען'): #перевод неопр формы (инфиниив) в основу
        verbs.add(word[:-2])
    elif word.endswith('ן'): #перевод неопр формы (инфиниив) в основу
        verbs.add(word[:-1])
    else:
        verbs.add(word)
    

vowel = {'א', 'אָ', 'ו', 'י', 'ע', 'אַ', 'וּ', 'יִ', 'וֹ'}

vowel_diphthongs = {'ייַ'}

def_articles = {'דאָס','דעם', 'דער', 'די'}
undef_articels = {'אַ', 'אַן', 'א', 'אן'}
negative_articles = {'ניין'}
single_articles = {'דאָס','דעם', 'דער', 'אַ', 'אַן', 'א', 'אן'}
articles = def_articles | undef_articels | negative_articles

preps1 = {"וועגן", "העכער", "אַריבער", "נאָך", "קעגן", "צווישן", "אַרום",
         "ווי", "בייַ", "פריער", "הינטער", "ונטן", "ונטער", "בייַ",
         "צווישן", "ווייטער פון", "אָבער", "דורך", "טראָץ", "אַראָפּ",
         "בעשאַס", "ויסער", "פֿאַר", "0פון", "אין", "ין", "אַרייַן", "לעבן",
         "קומענדיק", "פון", "אויף", "פאַרקערט", "אַרויס", "אַרויס",
         "איבער", "פּער", "פּלוס", "קייַלעכיק", "זינט", "ווי", "דורך",
         "ביז", "צו", "צו", "ונטער", "ניט ענלעך", "ביז", "אַרויף",
         "דורך", "מיט", "ין", "אָן", "אונטער", "איידער"}

preps2 = {
   "אָב", "אַדורך", "אָהן", "אויף", "אויפֿן", "אויפן", "אום", "אונטער", 
    "אונטערן", "אַחוץ", "איבער", "איבערן", "אין", "אינם", "אינמיטן", 
    "אינעם", "אכוץ", "אָן", "אן", "אַנטקעגן", "אַנשטאָט", "אַקעגן", "אַרײַנציִענדיק", 
    "באַ", "באַם", "בהסכּם", "בזכות", "ביז", "ביזן", "בײַ", "בײַם", "במשך", "בעפֿאָר", 
    "דורכן", "הינטער", "הינטערן", "ווי", "וועגן", "כּדי", "לויט", "לויטן", "לזכּרון", 
    "לכּבֿוד", "לכבֿוד", "לעבן", "לענגאויס", "מיט", "מיטן", "נאָך", "נאָכן", "פֿאַר", 
    "פֿאַרבײַ", "פֿאַרן", "פֿון", "פֿונעם", "פֿיר", "צו", "צוא", "צווישן", "צוליב", 
    "צום", "קיין", "קעגן", "אָנשטאָט", "אַפילע", "אוֹנטער"
}

not_vivo_conjunctions = {
    "אַבי", "אָבער", "אָדער", "אויב", "און", "אונ", "אונד", "אונ׳", "אַז", "אז", "איידער", "אַלס",
    "באשר", "בכדי", "בעת", "דען", "הגם", "היות", "וואָרעם", "ווי באַלד", "וויבאַלד", "ווײַל", "ווען",
    "זינט", "טאָ", "טאָמער", "טראָץ דעם וואָס", "כּל־זמן", "כאָטש", "מאָל", "מה־דאָך", "מחמת", "מינוס",
    "נאָך דעם וואָס", "נאָך דעם ווי", "ניעזשעלי", "סײַ", "סײַדן", "פּלוס", "צוליב דעם וואָס"
} #тут все союзы

pronouns = {"איך", "דו", "ער", "זי", "מיר", "זיי", "אים",
            "אונדז", "מייַן", "דיין", "זייַן", "אונדזער", "זייער",
            "הערס", "אונדזערער", "זייערער", "איר", "דייַן", "אייַער"} #тут все местоимения

counting_numbers = {'איין','איינס','צוויי','דרייַ','פיר','פינף','זעקס','זיבן',
           'אַכט','נײַן','צען','עלף','צוועלף','דרײַצן','פערצן','פופצן',
           'זעכצן','זיבעצן','אַכצן','נײַנצן','צוואַנציק','דרײַסיק','פערציק',
           'פופציק','זעכציק','זיבעציק','אַכציק','נײַנציק','הונדערט','טויזנט',
           'מיליאָן','מיליאַרד', 'ביליאָן'} #все количественные числительные

ordinal_numbers = {'ערשט','ערשטער','צווייט','דריט','פערט','פינפט','זעקסט','זיבעט',
            'אַכט','נייַנט','צענט','עלפט','צוועלפט','דרײַצנט','פֿערצנט','פֿופֿצנט',
            'זעכצנט','זיבעטצנט','אַכצנט','נײַנצנט','צוואַנציקסט','דרײַסיקסט',
            'פֿערציקסט','פֿופֿציקסט','זעכציקסט','זיבעציקסט','אַכציקסט','נײַנציקסט',
            'הונדערטסט','טויזנטסט'} #все порядковые числительные

not_vivo_numbers = counting_numbers | ordinal_numbers

not_vivo_adverbs = {"נעכטן", "הייַנט", "מאָרגן", "איצט", "דעריבער", "שפּעטער", 
    "שוין", "לעצטנס", "לעצטנס", "באַלד", "טייקעף", "נאָך", "נאָך",
    "צוריק", "דאָ", "דאָרט", "איבער דאָרט", "ומעטום", "ערגעץ", "היים",
    "אַוועק", "אַרויס", "זייער", "גאַנץ", "שיין", "טאַקע", "פעסט", "געזונט",
    "שווער", "געשווינד", "סלאָולי", "קערפאַלי", "קום", "קום", "מערסטנס",
    "קימאַט", "לעגאַמרע", "צוזאַמען", "אַליין", "שטענדיק", "אָפט", "יוזשאַוואַלי",
    "זעלטן", "ראַרעלי" }

not_vivo_prefixes = {
    "אַוועק", "אויס", "אויפֿ", "אומ", "אונ", "אונטער", "אור", "איבער", "אייבער", "אײַנ",
    "אינטער", "אָנ", "אַנידער", "אָפּ", "אַפֿער", "אַר", "אַראָפּ", "אַרויס", "אַרויפֿ", "אַרומ",
    "אַרונטער", "אַריבער", "אַרײַנ", "באַ", "ביאָ", "גע", "דער", "טראַנס", "כּלל", "מילי",
    "נאָכ", "נעווראָ", "סך", "פֿאַר", "פֿאַרבײַ", "פֿאָרויס", "פֿונאַנדער", "פֿיר", "צו", "צונויפֿ",
    "צוריק", "צע", "צענטי", "שטיפֿ"
}

not_vivo_preps = preps1 | preps2

nouns = set()
for noun in nouns_d:
    z = noun.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    nouns.add(z)
#тут существительные

adjectives = set()
for adj in adjectives_d:
    z = adj.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    adjectives.add(z)
#тут все прилагательные
    
preps = set()
for prep in not_vivo_preps:
    z = prep.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    preps.add(z)
#тут все предлоги

numbers = set()
for number in not_vivo_numbers:
    z = number.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    numbers.add(z)
#тут все числительные

adverbs = set()
for adverb in adverbs_d:
    z = adverb.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    adverbs.add(z)
adverbs = adverbs | not_vivo_adverbs
#тут наречия

conjunctions = set()
for conj in not_vivo_conjunctions:
    z = conj.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    conjunctions.add(z)
#тут союзы

prefixes = set()
for prefix in not_vivo_prefixes:
    z = prefix.replace('פ','פֿ')
    z = z.replace('וֹ','וי')
    z = z.replace('בּ','ב')
    prefixes.add(z)
#тут частоупотребимые приставки

#в иддише предлоги склеиваются с артиклем в дательном падеже
#строго правила, конечно, нет, так что тут полный перебор, благо их не так много
merged_preps = set()
for prep in preps:
    for ending in {'ן', 'ם', 'עם'}:
        merged_prep = prep + ending
        merged_preps.add(merged_prep)

help_words = {'פֿלעגט','פֿלעגן','פֿלעג','פֿלעגסט'} #для многпрошедшего времени

have = {'האָבן','האָב','האָט','האָסט'} #для других прошедших времен

ist = {'זײַן','איז','בין','זײַנען','ביסט','זײַט'} #для других прошедших времен

future = {'וועל', 'וועסט', 'וועט', 'וועלן'} #буду в разных родах (будущее время)

special = 'געהאט' #спец слово для предпрошедшего времени

condition = {'װאָלט','װאָלטן','װאָלסט'} #бы в разных родах

temporus = dict()
irr_verbs = dict()
with open("data.json", "r", encoding="utf-8") as file:
    temporus = json.load(file) #словарь неправильных глаголов инфинитив:партицип
    for key, value in temporus.items():
        k = key.replace('פ','פֿ')
        k = k.replace('וֹ','וי')
        k = k.replace('בּ','ב')
        v = value.replace('פ','פֿ')
        v = v.replace('וֹ','וי')
        v = v.replace('בּ','ב')
        irr_verbs[k] = v
        
def cut_adj(word): #убираем у прилагательного родовое окончание
    if word.endswith('ער'):
        return word[:-2]
    if word.endswith('ע'):
        return word[:-1]
    if word.endswith('נעס') or word == 'נייַעס' or word == 'נענוֹיעס':
        return word[:-2] #так надо
    for token in vowel|vowel_diphthongs|{'מ'}:
        ending = token + 'ען' #справа налево
        if word.endswith(ending):
            return word[:-2]
    if word.endswith('ן'):
        return word[:-1]
    return word #ну это или не прилагательное или уже краткая форма

def normalize_adj(word): #убираем у суффикс сравнительной степени без родового окончания
    if word.endswith('ער'):#сравнительная степень
        lemma = word[:-2]
        return lemma
    if word.endswith('סט'):#превосходная степень
        lemma = word[:-2]
        return lemma
    return word
    
def normalize_noun(word):#обработка существительного во множ числе
    if word.endswith('עס'):
        return word[:-2]
    if word.endswith('ען'):
        return word[:-2]
    if word.endswith('עך'):
        return word[:-2]
    if word.endswith('ס'): #чередование не определено строго
        return word[:-1]
    if word.endswith('ער'): #чередование часто определено, но не идеально, мир жесток
        shift_word = word[:-2].replace('אָ','ע').replace('אָ','ע').replace('ו', 'י')
        return shift_word
    if word.endswith('ים'): #чередование не определено строго
        return word[:-2]
    if word.endswith('ן'):
        return word[:-1]
    return word

def normalize_adverb(word):#убираем родовое окончание у нарчеия
    #наречия неизменяемые, почти всегда совпдаюат с краткой формой прилагательного
    return word
        
def normalize_verb(word): #привести глагол в инфинитив
    #общепрошедшее время = have (чаще) или ist (редко) + партицип
    if word.startswith('גע') and word.endswith('ט'): #приставка для партиципа если глагол не приставочный
        #почти все правильные глаголы в партиципе так заканчиваются
        base = word[:-1]
        base = base[2:] #python easy
        return base
    for prefix in prefixes: #у приставочных глаголов приставка партиципа идет после приставки
        if word.startswith(prefix) and word[(len(prefix)):].startswith('גע') and word.endswith('ט'):
            base = prefix + word[(len(prefix)+2):] #справа налево
            base = base[:-1]
            return base
    for prefix in {'אנט','אב','נע','דער','פֿאר','צע'}: #особые приставки перед которым нет приставки партиципа
        if word.startswith(prefix) and word.endswith('ט'):
            return word[:-1]
        
    if word.endswith('ען'): #перевод неопр формы (инфиниив) в основу 
        return word[:-2]
    if word.endswith('ן'): #перевод неопр формы (инфиниив) в основу
        return word[:-1]
    
    #настоящее время = основа + родовое окончание
    if word.endswith('ען'): #да, также образоыввается аж два родовых окончания
        return word[:-2]
    if word.endswith('ן'): #да, также образоыввается аж два родовых окончания
        return word[:-1]
    if word.endswith('סט'):
        return word[:-2]
    if word.endswith('ט'): #да, также образоыввается аж три родовых окончания
        return word[:-1]
    
    #будущее время = буду + инфинитив, ищем будду и убираем
    
    #предпрошедшее врем = спец слово + have + партицип основного глагола
    
    #предбудущее время = буду + 'האָבן' / 'זײַן' + партицип
    
    #Appelle mon numero
    
    #условное наклоение = бы + партицип / инфинитив (даже тут нет единого правила)

    return word
    

#функция для составления статичтиеского словаря (т.е. при 1 пробеге по текстам)
#логика следующая: если слово попадает под какие-то крайне определенные правила
#то мы просто применим их во время 2 пробега, нам незачем даже хранить для них статистику
#иначе накапливаем статистику,как можно лучше разделяя различные случаи, для уменьшения ошибки
def update_dict(file_path, d_f): #путь к файлу, словарь форм
    text = None
    with open(file_path, 'r', encoding = 'utf-8') as file:
        text = file.readlines()
    lemm_text = ""
    line_count = -1
    for line in text:
        line_count += 1
        split_line = line.split()
        for i in range (len(split_line)):
            split_line[i] = split_line[i].replace('פ','פֿ')
            split_line[i] = split_line[i].replace('וֹ','וי')
            split_line[i] = split_line[i].replace('בּ','ב')
            if split_line[i] in preps or split_line[i] in merged_preps:
                continue #если предлог то мы его не трогаем и далее тоже не будем
            if split_line[i] in conjunctions:
                continue #если союз то мы его не трогаем и далее тоже не будем
            if split_line[i] in numbers:
                continue #в последующем мы будем их заменять на токены а пока пропускаем
            if split_line[i] in pronouns:
                continue #в последующем мы будем их заменять на токены а пока пропускаем
            if split_line[i] in articles:
                continue #я пока не понял че делать с артиклями, либо оставим либо токены
            if split_line[i] in irr_verbs.values(): #то есть это инфинитив непр глагола
                lemma = normalize_verb(split_line[i])
                if (len(lemma) > 2):
                    d_f[lemma] = d_f.get(lemma, set()) | {split_line[i]}
                continue
            if split_line[i] in irr_verbs.keys(): #то есть это партицип непр глагола
                lemma = normalize_verb(irr_verbs[split_line[i]])
                if (len(lemma) > 2):
                    d_f[lemma] = d_f.get(lemma, set()) | {split_line[i]}
                continue
            if split_line[i] in adverbs: #просто наречие
                d_f[split_line[i]] = d_f.get(split_line[i], set()) | {split_line[i]}
                continue
            if (i > 0 and (split_line[i-1] in single_articles or split_line[i-1] in merged_preps)):
                #артикль ед числа => прилагательное или существ в ед числе
                d_f[split_line[i]] = d_f.get(split_line[i], set()) | {split_line[i]}
                cut_word = cut_adj(split_line[i]) #убрали родовое окончание
                if (split_line[i] != cut_word and len(cut_word) > 2): #чтобы не считать некоторые формы много раз
                    d_f[cut_word] = d_f.get(cut_word, set()) | {split_line[i]}
                lemm = normalize_adj(cut_word) #убрали сравнительную степень (не факт что есть)
                if (split_line[i] != lemm and lemm != cut_word and len(lemm) > 2): #если сравнительная форма все же была
                    d_f[lemm] = d_f.get(lemm, set()) | {split_line[i]}
                continue
            if (i > 0 and split_line[i-1] in articles):
                #артикль мб множ числа => прилагательное или существ в любом числе
                d_f[split_line[i]] = d_f.get(split_line[i], set()) | {split_line[i]}
                noun = normalize_noun(split_line[i])
                if (noun != split_line[i] and len(noun) > 2):
                    d_f[noun] = d_f.get(noun, set()) | {split_line[i]}
                cut_word = cut_adj(split_line[i]) #убрали родовое окончание
                if (split_line[i] != cut_word and cut_word != noun and cut_word != split_line[i] and len(cut_word) > 2):
                    d_f[cut_word] = d_f.get(cut_word, set()) | {split_line[i]}
                lemm = normalize_adj(cut_word) #убрали сравнительную степень (не факт что есть)
                if (split_line[i] != lemm and lemm != cut_word and lemm != noun and lemm != split_line[i] and len(lemm) > 2): #если сравнительная форма все же была
                    d_f[lemm] = d_f.get(lemm, set()) | {split_line[i]}
                continue
            #артикля нет, с небольшим шансом это существ или прилаг во множ числе
            #а скорее всего, глагол или наречие
            if (split_line[i] in help_words):
                #многпрошедшее время
                #где-то впереди инфинитив, но на это конкретное слово мы забиваем везде
                continue
            if (split_line[i] in have):
                #либо глагол иметь либо часть прошедшего времени
                if (i < len(split_line)-1 and split_line[i+1] in articles):
                    #то есть это в значении иметь
                    #потом будет на האָב меняться, но это при 2 пробеге
                    continue
                else:
                    #общепрошедшее время (почти наверное)
                    #где-то впереди партицип, но на это конкретное слово мы забиваем везде
                    continue
            if (split_line[i] in ist):
                #тут тоже при 2 пробеге будет все однозначно
                continue
            if (split_line[i] in future):
                #будущее время, впереди где-то инфинитив, на это слово само забиваем
                continue
            if (split_line[i] == special):
                #предпрошедшее время, где-то впереди партицип, тут забиваем
                continue
            if (split_line[i] in condition):
                #тут тоже при 2 пробеге будет все однозначно
                continue
            #вероятнее всего перед нами глагол или наречие, но не факт
            d_f[split_line[i]] = d_f.get(split_line[i], set()) | {split_line[i]}
            verb = normalize_verb(split_line[i])
            if (verb != split_line[i] and len(verb) > 2):
                d_f[verb] = d_f.get(verb, set()) | {split_line[i]}
            cut_word = cut_adj(split_line[i]) #убрали родовое окончание
            if (split_line[i] != cut_word and cut_word != verb and len(cut_word) > 2):  
                d_f[cut_word] = d_f.get(cut_word, set()) | {split_line[i]}
            lemm = normalize_adj(cut_word) #скорее на случай наречия (но возможно и прилаг)
            if (split_line[i] != lemm and lemm != cut_word and lemm != verb and len(lemm) > 2):
                d_f[lemm] = d_f.get(lemm, set()) | {split_line[i]}
            noun = normalize_noun(split_line[i])
            if (split_line[i] != noun and noun != cut_word and noun != verb and noun != lemm and len(noun) > 2):
                d_f[noun] = d_f.get(noun, set()) | {split_line[i]}
                                          
def make_statistics(dir_root): #путь к папке с текстами
    d_f = dict() #словарь форм
    files = os.listdir(dir_root)
    for i in range(len(files)):
        file = files[i]
        file_path = os.path.join(dir_root, file)
        update_dict(file_path, d_f)
        print(i)
    #with open('dictionary_forms.pkl', 'wb') as f2:
     #   pickle.dump(d_f, f2)
    d_json = dict()
    for key in d_f.keys():
        d_json[key] = list(d_f[key])
    with open("forms.json", "w", encoding="utf-8") as my_json1:
        json.dump(d_json, my_json1, ensure_ascii=False, indent=4)
        
path = 'C:/Users/Ilia2024/Desktop/yiddish/after/'
make_statistics(path)






            
    
    

        
