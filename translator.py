import csv
import random
import math
import numpy as np
from nltk.corpus import wordnet


# function to return key for any value
def get_key(val):
    for key, value in dict_syndLUL.items():
        if val in value:
            return key

    return "key doesn't exist"


FILEPATH_ENG = "commonwords.txt"
FILEPATH_OZK = "DemonWords.txt"
FILEPATH_TRL = "EnglishWords.txt"

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
    't': ["ta", "tak", "th", "tho"],
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
dict_syndLUL = {
    "Ozh": ["Self", "I", "me", "my", "mine"],
    "Izh": ["you", "him", "her"],
    "Izhai": ["group"],
    "Ozkavosh": ["demons", "spirits"],
    "sa": ["this"],
    "vu": ["that"],
    "doq": ["upon", "ontop", "above"],
    "roq": ["far", "distant"],
    "doz": ["below", "beneath", "underneath"],
    "ahm'": ["very", "super", "absolute"],
    "ashm": ["more", "additional"],
    "vo'": ["not"],
    "Vom": ["less"],
    "acha": ["am", "be", "now"],
    "icha": ["could", "will", "possibility"],
    "ucha": ["was", "existed"],
    "hollom": ["without", "nothing", "hollow", "absence"],
    "tak": ["take", "have", "own"],
    "wroth": ["again", "repeated", "iterative"],
    "lash": ["part", "segment", "share"],
    "alatho": ["forward", "ahead"],
    "ulatho": ["Back", "backwards"],
    "tho": ["at", "local"],
    "sek": ["introspection"],
    "thok": ["move", "go", "walk", "run"],
    "fek": ["stop", "cease", "abandon"],
    "ses": ["hide", "unseen"],
    "hahsh": ["feel", "touch"],
    "eyik": ["look,at", "witness", "behold"],
    "zomfa": ["leisure", "happiness"],
    "domosh": ["reign", "domination", "dominion", "kingship"],
    "Arkosh": ["master", "king"],
    "voth": ["war", "battle", "fight", "slaughter"],
    "hedoq": ["desirable", "delicious", "wanted"],
    "nith": ["land", "earth", "ground", "kingdom"],
    "gluth": ["eat", "devour", "consume"],
    "omoz": ["darkness", "abyss", "blackness", "hell"],
    "nesh": ["home", "sanctuary", "safety"],
    "safras": ["pain", "suffer", "wound"],
    "poz": ["power", "ability", "skill", "action", "able"],
    "irush": ["Illness", "common,cold", "plague"],
    "sol": ["hope", "light", "brightness", "sun", "fire"],
    "groth": ["spread", "widen", "open", "welcome"],
    "greesh": ["debt", "lack", "absence"],
    "lieyev": ["payment", "gift", "tithe", "taxes", "tax"],
    "chron": ["time", "duration"],
    "rast": ["toys", "puppets", "amusement", "entertainment"],
    "miskath": ["failure", "incomplete", "unfinished"],
    "fol": ["weakling", "whelp", "peasant", "fool"],
    "ensh": ["know", "learn"],
    "ov": ["one", "once", "singular"],
    "sav": ["seven", "seventh"],
    "kish": ["excrement", "waste", "shit", "crap"],
    "sovoz": ["french dip sandwich", "sandwich", "snack"]
}

BigList = [i.strip().split() for i in open(FILEPATH_ENG).readlines()]

Translations_Dictionary = {}

Translation_Word = []


temp_list = []
for key, value in dict_syndLUL.items():                     # for each key value pair item in direct wiki translations:
    for i in value:                                         # for each element in the value list:
        for syn in wordnet.synsets(i):                      # for each synonym in wordnet:
            for k in syn.lemmas():                          # for each lemma (actual synonym list word element):
                temp_list.append(k.name())                   # stash the synonym into a temp list!
    temp_list = np.unique(temp_list).tolist()                 # for each key, remove duplicates from temp_list!
    for i in temp_list:                                      # for each element in the stashed synonym list:
        value.append(i)                                     # append each element to value list in the synonym dict!
    temp_list = []                                           # clear the stash for the next iteration!


words_to_process = 40
loop_range = range(len(BigList))
for i in loop_range:
    if i >= words_to_process:
        break
    else:
        Translation_Word = str(BigList[i])
        Translation_Word = [character for character in str.lower(Translation_Word) if character.isalnum()] # clean out [""] etc
        Translation_Word = "".join(Translation_Word)
        English_Word = Translation_Word
        print("en word is", English_Word)
        # get a string for debug printing

        if English_Word in (item for sublist in dict_syndLUL.values() for item in sublist):

            print("jop da gibts schon ne übersetzung für", English_Word, ":)")
            # have to do it the other way around because original dict is ozk -> eng but we want eng -> ozk
            Translations_Dictionary[English_Word] = get_key(English_Word)
            print(Translations_Dictionary)


        else:

            forbiddenletters = {'b': 'q', 'j': 'i', 'x': 'k'}
            for key in forbiddenletters.keys():
                Translation_Word = Translation_Word.replace(key, forbiddenletters[key])

            print("translated word is", Translation_Word)
            Translation_Word_Length = len(str(Translation_Word))
            Hyphens_Length = math.sqrt(Translation_Word_Length)
            Hyphens_Rounded = int(Hyphens_Length)
            hyphens = [Translation_Word[i:i + Hyphens_Rounded] for i in range(0, len(Translation_Word), Hyphens_Rounded)]


            char_amt = [] # how many characters each syllable will have
            start_chars = [] # list of English syllable start characters for Ozkavosh lookup replacement

            iterations = len(hyphens)
            for i in range(iterations):
                char_amt.append(len(hyphens[i]))
                start_chars.append(hyphens[i][:1])

            ozk_syllables = [] # list of new Ozkavosh syllables

            for i in start_chars:
                character_mapping = dict_charpairs.get(i)
                weightlist_mapping = weights_dict.get(i)
                ozk_syllable_result = str(random.choices(population=character_mapping, weights=weightlist_mapping,k=1))  # returns randomly weighted pick from ozk syllables
                ozk_syllables.append(ozk_syllable_result)

            ozk_word = str(ozk_syllables)
            ozk_word = [character for character in ozk_word if character.isalnum()]
            ozk_word = "".join(ozk_word) # get a clean Ozkavosh string for printing
            print("ozkavosh word is", ozk_word)

            Translations_Dictionary.update({English_Word: ozk_word})
            print(Translations_Dictionary)







