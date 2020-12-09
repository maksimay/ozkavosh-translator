import csv
import random
import math
from random import choice
import re
from pydub import AudioSegment
from pydub.playback import play
import os
# currently not used, might use later
import pyphen
from hyphenate import hyphenate_word
import scipy
from scipy import stats

FILEPATH_ENG = "commonwords.txt"
FILEPATH_OZK = "DemonWords.txt"
FILEPATH_TRL = "EnglishWords.txt"

# direct translations from dotawiki (INCOMPLETE)
'''
englist = [i.strip().split() for i in open(FILEPATH_TRL).readlines()]
ozklist = [i.strip().split() for i in open(FILEPATH_OZK).readlines()]
'''
# 3000 most common english words (INCOMPLETE, UNTAGGED)
BigList = [i.strip().split() for i in open(FILEPATH_ENG).readlines()]
# get random word from list
Current_Word = []
sequence = [i for i in range(len(BigList))]
for words in range(len(BigList)):
    selection = choice(sequence)
    Current_Word = str(BigList[selection])
    Current_Word = str.lower(Current_Word)
    Current_Word = [character for character in Current_Word if character.isalnum()]
    Current_Word = "".join(Current_Word)
print("en word is", Current_Word)


##### WORD CLASS AND TAG CHECK #########
'''
is it an adjective? adverb? verb? subjective?
is it a superlative? if it is a verb, what tense does it have? 
'''
########################


#################################

'''
########## HYPHENATION ############# (correct english hyphenation - use this later to make stuff better)
hyphens = hyphenate_word(Current_Word)
print(hyphens)
'''

### FORBIDDEN LETTERS ####

forbiddenletters = {'b': 'q', 'j': 'ia', 'x': 'ks'}
for key in forbiddenletters.keys():
    Current_Word = Current_Word.replace(key, forbiddenletters[key])

##########################

##### cheap hyphenation/chunk replacing ########

Current_Word_Length = len(str(Current_Word))
Hyphens_Length = math.sqrt(Current_Word_Length)
Hyphens_Rounded = int(Hyphens_Length)
#list of chunks/hyphens
hyphens = [Current_Word[i:i+Hyphens_Rounded] for i in range(0, len(Current_Word), Hyphens_Rounded)]

#################################################



########## MAPPING TABLES ########################


dict_charpairs = {'a': ["as", "ath", "ah", "al", "ar", "af"], 'c': ["ch"], 'd': ["do"], 'e': ["es", "ek"],
                  'f': ["fe", "fa", "fr", "fo"], 'g': ["gr", "gl"], 'h': ["ha", "ho", "hm"],
                  'i': ["iz", "ir", "it", "ik", "ish", "isk"], 'k': ["ka", "ko", "ki"], 'l': ["la", "lo", "li", "lu"],
                  'm': ["mo", "mi"], 'n': ["ne", "ni", "ns"], 'o': ["om", "oz", "ot", "osh"], 'p': ["po", "pr", "pz"],
                  'q': ["qo"], 'r': ["ro", "ra", "re", "rk"], 's': ["sas", "ath", "sah", "sal", "sar", "saf"],
                  't': ["th", "tho", "ta"], 'u': ["uch", "ul", "ush", "uth"], 'v': ["vo", "vu"], 'w': ["wr"],
                  'y': ["ye", "yi"], 'z': ["zh", "zk", "zo"]}




X = stats.binom(10, 0.2) # Declare X to be a binomial random variable
print(X.pmf(3))          # P(X = 3)
print(X.cdf(4))          # P(X <= 4)
print(X.mean())          # E[X]
print(X.var())           # Var(X)
print(X.std())           # Std(X)
print(X.rvs())           # Get a random sample from X
print(X.rvs(10))         # Get 10 random samples form X

print(X)




weights_dict = {"a": [0.35, 0.25, 0.1, 0.1, 0.1, 0.1], "c": [1], "d": [1], "e": [0.5, 0.5],
                "f": [0.25, 0.25, 0.25, 0.25], "g": [0.5, 0.5], "h": [0.45, 0.45, 0.1],
                "i": [0.3, 0.125, 0.125, 0.125, 0.125, 0.12], "k": [0.5, 0.25, 0.25], "l": [0.6, 0.15, 0.15, 0.1],
                "m": [0.66, 0.34], "n": [0.35, 0.34, 0.32], "o": [0.4, 0.3, 0.15, 0.15], "p": [0.5, 0.2, 0.3], "q": [1],
                "r": [0.5, 0.25, 0.125, 0.125], "s": [0.4, 0.3, 0.15, 0.04, 0.04, 0.045], "t": [0.7, 0.26, 0.04],
                "u": [0.25, 0.25, 0.25, 0.25], "v": [0.8, 0.2], "w": [1], "y": [0.5, 0.5], "z": [0.6, 0.2, 0.2]}


oz_sample_file = "./oz_audiolist.csv"
oz_audiolist = []

with open(oz_sample_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
        oz_audiolist.append(','.join(row))



################## TABLES END #########################



####### REPLACEMENT START #########

# get number of characters in each hyphen, append to list
# get start character for each hyphen, append to list
char_amt = []
start_chars = []
iterations = len(hyphens)
for i in range(iterations):
    char_amt.append(len(hyphens[i]))
    start_chars.append(hyphens[i][:1])




# weighted random pick to replace hyphen depending on english start character, look for matching audio
ozwordlist = []
pathlist = []
audionamelist = []

for i in start_chars:

    character_mapping = dict_charpairs.get(i)
    weightlist_mapping = weights_dict.get(i)
    result = str(random.choices(population=character_mapping, weights=weightlist_mapping, k=1))
    ozwordlist.append(result)

    audioname = str(re.sub(r'\W+', '', result))
    audio_filepath = './audio/' + audioname + '.wav'
    print("searching for oz_audio in", audio_filepath)
    pathlist.append(audio_filepath)

# print the new ozk word
ozwordlist = str(ozwordlist)
ozword = [character for character in ozwordlist if character.isalnum()]
ozword = "".join(ozword)
print("oz word is", ozword)

#### AUDIO PROCESSING ####
### REMOVING SILENCE FUNCTION####

def detect_silence(sound, silence_threshold=-50.0, chunk_size=10):
    # silence_threshold in dB
    # chunk_size in ms
    # iterate over chunks until you find the first one with sound
    trim_ms = 0
    # to avoid infinite loop
    assert chunk_size > 0
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

########## AUDIO TRIMMING / APPENDING ##########

audioisvalid = False
combined_audio = AudioSegment.empty()

for i in pathlist:
    wav_filepath = i
    print(i)
    audioname = wav_filepath.replace('.wav', '').replace('./audio/', '')
    print(audioname)
    if audioname in oz_audiolist:
        print("Samples found! Creating combined Audiosnippet...")
        audioisvalid = True
        src_audio = AudioSegment.from_wav(wav_filepath)
        print("Trimming Audiofiles..")
        duration = len(src_audio)
        start_trim = detect_silence(src_audio)
        end_trim = detect_silence(src_audio.reverse())
        trimmed_audio = src_audio[start_trim:duration - end_trim]
        combined_audio += trimmed_audio
        # combined_audio += src_audio


###### REPLACEMENT END #############




### Make Directory for Combined audios if it doesnt exist yet ###
if not os.path.exists('./combined'):
    os.makedirs('./combined')

#### FINAL EXPORT ####
if audioisvalid == True:
    print("Exporting audio to disk ...")
    combined_audio.export("./combined/_" + ozword + "_" + Current_Word + "_combined.wav", format="wav")
    print("Exported succesfully!")



