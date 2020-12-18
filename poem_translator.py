import random
import math
import csv
import re
import nltk

dict_charpairs = {
    'a': ["ac", "ach", "ah", "ahm", "ahmi", "al", "ala", "ark", "as", "ash", "ath", "atho"],
    'c': ["ch", "cha"],
    'd': ["do", "dom", "doq"],
    'e': ["ek", "en", "ey"],
    'f': ["fa", "fath", "fe", "fek", "fi", "fo", "fol"],
    'g': ["gl", "glu", "gr", "gro", "groth"],
    'h': ["ha", "hag", "has", "he", "hedo", "hm", "ho", "hol", "hro"],
    'i': ["ich", "icha", "ik", "iru", "is", "isk", "iz", "izh"],
    'k': ["ka", "kala", "kath", "ko"],
    'l': ["lo", "lof", "lofa", "lom"],
    'm': ["mi", "mis", "mo", "moz"],
    'n': ["ne", "ni", "ns"],  # !
    'o': ["of", "ok", "ol", "om", "omf", "omfa", "omo", "omoz", "oq", "osh", "oth", "ov", "oz", "ozh"],
    'p': ["po", "pr", "pz"],  # !
    'q': ["oq", "ok"],  # !
    'r': ["ro", "ros", "rush"],
    's': ["se", "sek", "sh", "shk", "so", "sof", "sol", "sov", "sovo"],
    't': ["ta", "tak", "th", "tho"], # thu do
    'u': ["uch", "uth"],
    'v': ["vo", "vot", "voth", "vr", "vro", "vroshk"],
    'w': ["wr"],  # !
    'y': ["yi"],
    'z': ["zh", "zomoz"]}
weights_dict = {
    "a": [1, 2, 2, 2, 3, 2, 3, 3, 2, 3, 2, 1],
    "c": [1, 2],
    "d": [1, 2, 2],
    "e": [1, 2, 2],
    "f": [1, 2, 2, 3, 2, 3, 2],
    "g": [1, 2, 2, 2, 1],
    "h": [1, 2, 2, 1, 2, 2, 1, 2, 2],
    "i": [1, 3, 2, 3, 2, 1, 3, 2],
    "l": [1, 2, 2, 2],
    "m": [1, 1, 1, 2],
    "n": [1, 2, 2],  # !
    "o": [1, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 2],
    "p": [1, 2, 2],  # !
    "q": [1, 2],  # !
    "r": [1, 2, 2],
    "s": [1, 2, 3, 3, 3, 3, 3, 3, 2],
    "t": [1, 2, 2, 1],
    "u": [1, 2],
    "v": [1, 2, 2, 2, 2, 2],
    "w": [1],
    "y": [1],
    "z": [1, 2]
}

with open('Translation_Dictionary.csv', mode='r') as infile:
    reader = csv.reader(infile)
    Translation_Dictionary = {rows[0]: rows[1] for rows in reader}

'''
with open('tolkien.txt') as f, open('tolkien_cleaned.txt', 'a') as f1:
    f1.write(' '.join(set(re.findall("[a-zA-Z\-\.'/]+", f.read()))))
'''
'''
f = open('tolkien.txt', 'r')
contents = f.readlines()
'''

#print(contents)
#tokens = nltk.sent_tokenize(contents)
#for t in tokens:
    #print (t, "\n")


mytext = "TEXT GOES HERE, TRANSLATION COMES OUT AND UNKNOWN WORDS ARE ADDED TO WIKI SORT OF"
mytext = mytext.split()
print(mytext)


for word in mytext:
    if word not in Translation_Dictionary.keys():
        print("no translation key for", word, "found in dict")
        Translation_Word = word
        Translation_Word = [character for character in str.lower(Translation_Word) if character.isalnum()]
        Translation_Word = "".join(Translation_Word)
        forbidden_letters = {'b': 'q', 'j': 'i', 'x': 'k'}

        for key in forbidden_letters.keys():
            Translation_Word = Translation_Word.replace(key, forbidden_letters[key])

        Translation_Word_Length = len(str(Translation_Word))
        Hyphens_Length = math.sqrt(Translation_Word_Length)
        Hyphens_Rounded = int(Hyphens_Length)
        hyphens = [Translation_Word[i:i + Hyphens_Rounded] for i in range(0, len(Translation_Word), Hyphens_Rounded)]

        char_amt = []  # how many characters each syllable will have
        start_chars = []  # list of English syllable start characters for Ozkavosh lookup replacement

        iterations = len(hyphens)
        for i in range(iterations):
            char_amt.append(len(hyphens[i]))
            start_chars.append(hyphens[i][:1])

        ozk_syllables = []  # list of new Ozkavosh syllables

        for i in start_chars:
            character_mapping = dict_charpairs.get(i)
            weightlist_mapping = weights_dict.get(i)
            ozk_syllable_result = str(random.choices(population=character_mapping, weights=weightlist_mapping,k=1))  # returns randomly weighted pick from ozk syllables
            ozk_syllables.append(ozk_syllable_result)

        ozk_word = str(ozk_syllables)
        ozk_word = [character for character in ozk_word if character.isalnum()]
        ozk_word = "".join(ozk_word)  # get a clean Ozkavosh string for printing
        print("ozkavosh word is", ozk_word)

        Translation_Dictionary.update({word: ozk_word})
        print("translation for", word, "added to dict")
    else:
        ozk = Translation_Dictionary.get(word)
        print(ozk)


'''
with open('Translation_Dictionary.csv', 'a+') as f:
    for key in Translation_Dictionary.keys():
        f.write("%s,%s\n" % (key, Translation_Dictionary[key]))
'''
