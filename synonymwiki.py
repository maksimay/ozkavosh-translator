from nltk.corpus import wordnet
import csv
import collections
from collections import defaultdict
import time


# key ############ value #####
dict_syndLUL = {"Ozh":["Self","I","me","my","mine"],
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
}
###################


#temporary list#
templist=[]

for key, value in dict_syndLUL.items():
            for i in value:
                #Get synonyms for every value in dict and append it to temporary list
                for syn in wordnet.synsets(i):
                    for l in syn.lemmas():
                        templist.append(l.name())
            #append the elemnts of the templist to the values of our dictionary
            for i in templist
                value.append(i)
            templist = []

#Get some key for testing
print("HERE COMES THE IRUSH SYNONYM LIST::::::::::::::::::")
print(dict_syndLUL.get("irush"))

#Safe our dict elements into csv file
with open("synonym_dict.csv", "w") as f:
    wr = csv.writer(f, delimiter="\n")
    wr.writerow(dict_syndLUL.items()) 





