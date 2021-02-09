import numpy as np
import pandas as pd
from hyphenate import hyphenate_word
import math
import random
import re
# init vars
forbidden_letters = {'b': 'q', 'j': 'i', 'x': 'k'}
oz_syllable_mapping = {
    'a': ["ac", "ach", "acha", "ah", "ahm", "ahmi", "al", "ar", "ark", "as", "ash", "ashm", "ath"],
    'c': ["ch", "cha"],
    'd': ["do", "dom", "doq"],
    'e': ["ek", "en", "ensh", "ey", "eyik"],
    'f': ["fa", "fath", "fe", "fek", "fi", "fo", "fol"],
    'g': ["gl", "glu", "gr", "gro", "groth"],
    'h': ["ha", "hag", "has", "he", "hedo", "hm", "ho", "hol", "hro", "hollom"],
    'i': ["ich", "icha", "ik", "iru", "is", "isk", "iz", "izh"],
    'k': ["ka", "kala", "kath", "ko"],
    'l': ["lo", "lof", "lom"],
    'm': ["mi", "mis", "mo", "moz"],
    'n': ["ne", "ni", "nith", "ns"],
    'o': ["of", "ok", "ol", "om", "omf", "omo", "oq", "osh", "oth", "ov", "oz", "ozh"],
    'p': ["po", "pr", "pz"],
    'q': ["oq", "ok"],
    'r': ["ro", "ros", "rush"],
    's': ["se", "sek", "sh", "shk", "so", "sof", "sol", "sov", "sovo"],
    't': ["ta", "tak", "th", "tho"], # thu do
    'u': ["uch", "ucha", "uth"],
    'v': ["vo", "vot", "voth", "vr", "vro", "vroshk"],
    'w': ["wr"],
    'y': ["yi"],
    'z': ["zh", "zomfa", "zomoz"]}
# nicht uniforme zufallsvariable hier
weight_mapping = {
    "a": [1, 2, 1, 2, 2, 3, 3, 3, 3, 2, 3, 1, 2],
    "c": [1, 2],
    "d": [1, 2, 2],
    "e": [2, 3, 1, 2, 1],
    "f": [1, 2, 2, 3, 2, 3, 2],
    "g": [1, 2, 2, 2, 1],
    "h": [1, 2, 2, 1, 2, 2, 1, 2, 2, 1],
    "i": [2, 1, 3, 3, 2, 1, 3, 2],
    "l": [1, 2, 2],
    "m": [1, 1, 1, 2],
    "n": [2, 2, 1, 1],
    "o": [1, 2, 3, 3, 3, 3, 2, 2, 2, 3, 3, 2],
    "p": [1, 2, 2],
    "q": [1, 2],
    "r": [1, 2, 2],
    "s": [1, 2, 3, 3, 3, 3, 3, 3, 1],
    "t": [1, 2, 2, 1],
    "u": [1, 2, 2],
    "v": [1, 2, 3, 2, 3, 1],
    "w": [1],
    "y": [1],
    "z": [2, 1, 2]
}

# create training dataframe
# train_df = pd.DataFrame()

# load dataframe
df = pd.read_pickle('df_translation.pkl')



f = open('test.txt', 'r')
poem = f.readlines()

for lines in poem:
    lines = lines.lower()
    print("line in poem is:", lines)
    sentence = lines.split()
    for en_word in sentence:
        en_word = [character for character in str.lower(en_word) if character.isalnum()]
        en_word = "".join(en_word)
        en_hyphens = hyphenate_word(en_word)
        # print(en_hyphens, "is en_hyphenation")

        if df['english'].eq(en_word).any():
            print(en_word, "found")
            loc = df.loc[df['english'] == en_word]
            print(loc)

        else:
            print(en_word, "not found")
            hyphens = en_hyphens
            if len(en_hyphens) == 1:
                Translation_Word_Length = len(str(en_word))
                Hyphens_Length = math.sqrt(len(en_word))
                Hyphens_Rounded = int(Hyphens_Length)
                if Hyphens_Rounded == 0:
                    Hyphens_Rounded += 1
                hyphens = [en_word[i:i + Hyphens_Rounded] for i in
                           range(0, Translation_Word_Length, Hyphens_Rounded)]
                print(hyphens, "are hyphens in custom translate condition")

            char_amt = []
            start_chars = []
            iterations = len(hyphens)
            for i in range(iterations):
                char_amt.append(len(hyphens[i]))
                start_chars.append(hyphens[i][:1])
            # initialise and or clear lists of syllables and corresponding audio paths to sample from
            oz_syllables = []
            audio_pathlist = []

            for i in start_chars:
                char_map = oz_syllable_mapping.get(i)
                weights_map = weight_mapping.get(i)
                oz_syllable_pick = str(random.choices(population=char_map, weights=weights_map, k=1))
                oz_syllables.append(oz_syllable_pick)
                # create clean audio string
                audio_name = str(re.sub(r'\W+', '', oz_syllable_pick))
                audio_filepath = './audio/' + audio_name + '.wav'
                # print("searching for audio name", audio_name, "in path", audio_filepath)
                audio_pathlist.append(audio_filepath)

            oz_word = str(oz_syllables)
            oz_word = [character for character in oz_word if character.isalnum()]
            oz_word = "".join(oz_word)

            df.loc[len(df.index)] = [en_word, oz_word, oz_syllables]


print(df)


# update the training dataframe

# save the dataframe










