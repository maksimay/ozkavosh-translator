from nltk.corpus import wordnet
import csv
# import time
import numpy as np


dict_syndLUL = {"ozh": ["Self", "I", "me", "my", "mine"],
                "izh": ["you", "him", "her"],
                "izhai": ["group", "they", "them"],
                "ozkavosh": ["demon", "demons", "spirit", "spirits"],
                "sa": ["this", "concept"],
                "vu": ["that", "the"],
                "doq": ["upon", "ontop", "above", "ground"],
                "roq": ["far", "distant", "remote", "reach"],
                "doz": ["below", "beneath", "underneath", "burrowed"],
                "ahm": ["very", "super"],
                "ashm": ["more", "additional", "much"],
                "vo": ["not", "negative", "exclude"],
                "vom": ["less", "fewer", "deplete", "exhaust"],
                "acha": ["am", "be", "now", "is"],
                "icha": ["could", "will", "possibility", "maybe"],
                "ucha": ["was", "existed"],
                "hollom": ["without", "nothing", "hollow"],
                "tak": ["take", "have", "own", "grab"],
                "wroth": ["again", "repeated", "iterative"],
                "lash": ["part", "segment", "share"],
                "alatho": ["forward", "ahead"],
                "ulatho": ["Back", "backwards"],
                "tho": ["at", "local", "position"],
                "sek": ["introspection", "meditate", "meditation"],
                "thok": ["move", "go", "walk", "run", "teleport"],
                "fek": ["stop", "cease", "die", "halt"],
                "ses": ["hide", "unseen", "concealed", "smoked"],
                "hahsh": ["feel", "touch", "sense"],
                "eyik": ["look", "view", "see", "witness", "behold"],
                "zomfa": ["leisure", "happiness", "happy", "glad", ],
                "domosh": ["reign", "domination", "dominion", "kingship"],
                "arkosh": ["master", "king"],
                "voth": ["war", "battle", "fight", "slaughter"],
                "hedoq": ["desirable", "delicious", "wanted", "objective"],
                "nith": ["land", "earth", "ground", "kingdom"],
                "gluth": ["eat", "devour", "consume"],
                "omoz": ["darkness", "abyss", "blackness", "hell"],
                "nesh": ["home", "sanctuary", "safety"],
                "safras": ["pain", "suffer", "wound"],
                "poz": ["power", "ability", "skill", "action", "spell", "ultimate"],
                "irush": ["Illness", "common cold", "plague"],
                "groth": ["spread", "widen", "open", "welcome"],
                "greesh": ["debt", "lack", "need"],
                "lieyev": ["payment", "gift", "tithe", "taxes", "tax"],
                "chron": ["time", "duration", "period"],
                "rast": ["toys", "puppets", "amusement", "entertainment"],
                "miskath": ["failure", "incomplete", "unfinished"],
                "fol": ["weakling", "whelp", "peasant", "fool", "greg", "fools"],
                "ensh": ["know", "learn"],
                "ov": ["one", "once", "singular"],
                "sav": ["seven", "seventh"],
                "kish": ["excrement", "waste"],
                "sol": ["hope", "light", "brightness", "sun", "fire"],
                "sovoz": ["sandwich", "snack"],
                }


templist = []
for key, value in dict_syndLUL.items():                     # for each key value pair item:
    for i in value:                                         # for each value:
        # print(i)
        for syn in wordnet.synsets(i):                      # for each synonyms in wordnet:
            for k in syn.lemmas():                          # for each lemma (synonym list word element):
                templist.append(k.name())                   # stash the synonym into a temp list!

    templist = np.unique(templist).tolist()                 # remove duplicates from templist!
    for i in templist:                                      # for each element in the stashed synonym list:
        # print(templist, "i")                              # for each word in list, print the list (lul)
        i = [character for character in str.lower(i) if character.isalnum()]
        i = "".join(i)
        value.append(i)                                     # append each temp element to value list in the dict!
    #print(templist)

    templist = []                                           # clear the stash for the next iteration! profit?


# Save our dict elements into csv file
with open('synonym_dict.csv', 'w') as f:
    for key in dict_syndLUL.keys():
        f.write("%s, %s\n" % (key, str(dict_syndLUL.get(key))))
