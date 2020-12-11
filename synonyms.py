from nltk.corpus import wordnet
import csv, time

e_file = "EnglishWords.csv"

englist = []
synonyms = []
dict_en = {}
newlist = []
eng_new = []


# convert function
def convert(list):
    return tuple(list)


# CREATE LIST FROM ENGLISHWORDS CSV
with open(e_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
        englist.append(','.join(row))

for words in englist:
    eng_new.append(words)
    for words in eng_new:
        for syn in wordnet.synsets(words):
            for l in syn.lemmas():
                newlist.append(l.name())
                list2 = newlist
            # newlist = []

    print(eng_new)
    print(list2)
    time.sleep(2)
    with open("out.csv", "w") as f:
        wr = csv.writer(f, delimiter="\n")
        wr.writerow(newlist)
        print("save complete")
        newlist = []
# print(newlist)
# print(list2)


# new_tuple = convert(newlist)
# eng_tuple = convert(eng_new)
# zipObj = zip(eng_tuple, new_tuple)
# dict_en = dict(zipObj)
# dict_en = dict.update(dict_en)
# newlist = []
# print(dict_en)
