from nltk.corpus import wordnet
import csv
# import time
import numpy as np


dict_syndLUL = {"Ozh":["Self","I","me","my","mine"],
"Izh":["you","him","her"],
"Izhai":["group"],
"Ozkavosh":["demons","spirits"],
"sa":["this"],
"vu":["that"],
"doq":["upon","ontop","above"],
"roq":["far","distant"],
"doz":["below","beneath","underneath"],
"ahm":["very","super"],
"ashm":["more","additional"],
"vo":["not"],
"Vom":["less"],
"acha":["am","be","now"],
"icha":["could","will","possibility"],
"ucha":["was","existed"],
"hollom":["without","nothing","hollow"],
"tak":["take","have","own"],
"wroth":["again","repeated", "iterative"],
"lash":["part","segment","share"],
"alatho":["forward","ahead"],
"ulatho":["Back","backwards"],
"tho":["at","local"],
"sek":["introspection"],
"thok":["move","go","walk","run"],
"fek":["stop","cease"],
"ses":["hide","unseen"],
"hahsh":["feel","touch"],
"eyik":["look,at","witness","behold"],
"zomfa":["leisure","happiness"],
"domosh":["reign","domination","dominion","kingship"],
"Arkosh":["master","king"],
"voth":["war","battle","fight","slaughter"],
"hedoq":["desirable","delicious","wanted"],
"nith":["land","earth","ground","kingdom"],
"gluth":["eat","devour","consume"],
"omoz":["darkness","abyss","blackness","hell"],
"nesh":["home","sanctuary","safety"],
"safras":["pain","suffer","wound"],
"poz":["power","ability","skill","action"],
"irush":["Illness","common,cold","plague"],
"groth":["spread","widen","open","welcome"],
"greesh":["debt","lack"],
"lieyev":["payment","gift","tithe","taxes","tax"],
"chron":["time","duration"],
"rast":["toys","puppets","amusement","entertainment"],
"miskath":["failure","incomplete","unfinished"],
"fol":["weakling","whelp","peasant","fool"],
"ensh":["know","learn"],
"ov":["one","once","singular"],
"sav":["seven","seventh"],
"kish":["excrement","waste"],
"sol":["hope","light","brightness","sun","fire"],
"sovoz":["french dip sandwich"],
}


# "thok":["move","go","walk","run"],
templist = []
for key, value in dict_syndLUL.items():                             # for each key value pair item:
            for i in value:                                         # for each value:
                print(i)
                for syn in wordnet.synsets(i):                      # for each synonyms in wordnet:
                    for k in syn.lemmas():                          # for each lemma (synonym list word element):
                        templist.append(k.name())                   # stash the synonym into a temp list!

            templist = np.unique(templist).tolist()                 # remove duplicates from templist!
            for i in templist:                                      # for each element in the stashed synonym list:
                print(templist, "i")                               # for each word in list, print the list (lul)
                i = [character for character in str.lower(i) if character.isalnum()]
                i = "".join(i)
                value.append(i)                                     # append each temp element to value list in the dict!
            #print(templist)

            templist = []                                           # clear the stash for the next iteration!
                                                                    # profit?

# Save our dict elements into csv file
with open('synonym_dict.csv', 'w') as f:
    for key in dict_syndLUL.keys():
        f.write("%s, %s\n" % (key, str(dict_syndLUL.get(key))))