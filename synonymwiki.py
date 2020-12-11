from nltk.corpus import wordnet
import csv
import collections
from collections import defaultdict


# key ############ value #####
dict_syndLUL = collections.defaultdict(lambda:{"Ozh":["Self","I","me","my","mine"],
"Izh":["you","him","her"],
"Izhai":["group"],
"Ozkavosh":["demons","spirits"],
"sa":["this"],
"vu":["that"],
"doq":["upon","ontop","above"],
"roq":["far","distant"],
"doz":["below","beneath","underneath"],
"ahm'":["very","super"],
"ashm":["more","additional"],
"vo'":["not"],
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
"sol":["hope","light","brightness","sun","fire"],
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
})
###################


#print("LOOP1 start")


print("LOOP OVER DICT")
for key, value in dict_syndLUL.items(): # arkosh: ["king", "master"]
    for words in value: # string in list
        print(words) # below, above
        for syn in wordnet.synsets(words):
            for l in syn.lemmas():
                dict_syndLUL["a"].append("hello")



for key, value in dict_syndLUL.items():
    print(key, "is", value)


'''
a_dict = collections.defaultdict(list)
a_dict["a"].append("hello")
print(a_dict)
# OUTPUT
# defaultdict(<class 'list'>, {'a': ['hello']})

'''










'''
syn_list = []
valuelist = []

#list of value entries from dict
for key, value in dict_syndLUL.items():
    #print(value)
    syn_list.append(value)

#print(syn_list)

for words in syn_list:
    for words in words:
        #print("word is", words)
        valuelist.append(words)
    #for syn in wordnet.synsets(words):
     #   for l in syn.lemmas():
      #      newlist.append(l.name())
       #     print(newlist)

#for list in syn_list:
 #   for words in list:
  #     print(words) #this gets to each word


    #for syn in wordnet.synsets(value):


#total_keys = len(list(dict_syndLUL))
#print("dict has", total_keys, "keys")
'''