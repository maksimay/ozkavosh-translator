import csv
import random
import math
import re
from pydub import AudioSegment
from random import choice
import os
import glob
import fnmatch
'''
currently not used
import pyphen
from hyphenate import hyphenate_word
import scipy
from scipy import stats
'''

FILEPATH_ENG = "commonwords.txt"
FILEPATH_OZK = "DemonWords.txt"
FILEPATH_TRL = "EnglishWords.txt"
# to do
# FILEPATH_DIR_TRL = "synonym_dict.csv" # exported from synonymwiki.py

# direct translations from dotawiki (INCOMPLETE)

'''
englist = [i.strip().split() for i in open(FILEPATH_TRL).readlines()]
ozklist = [i.strip().split() for i in open(FILEPATH_OZK).readlines()]
'''

# 3000 most common english words (INCOMPLETE, UNTAGGED) -> REPLACE WITH PARSED LIST

BigList = [i.strip().split() for i in open(FILEPATH_ENG).readlines()]


# TO DO: PARSE DBNARY.MORPHO.TTL FOR CATEGORIZED WORDZ (WIP)
# TO DO: WORD CLASS AND TAG CHECK (WIP) simple suffix prefix rules for vu'gluth combinations -> audio effect? 2.0?
# TO DO: REPLACE TRANSLATION IN FINAL DICT IF IT IS FOUND IN SYNONYM_DICT.CSV


Current_Word = []
words_to_process = 5# amount of words to pick from list
looprange = range(len(BigList))  
for words in looprange:
    if words >= words_to_process:
        break
    Current_Word = str(BigList[words])
    Current_Word = str.lower(Current_Word)
    Current_Word = [character for character in Current_Word if character.isalnum()] #clean string
    Current_Word = "".join(Current_Word)
    print("en word is", Current_Word)

    ### FORBIDDEN LETTERS ####
    # TO DO: maybe fix the export naming at some point aka asap (->jannis) =)
    # (english part of the filename is unintentionally modified by this currently)

    forbiddenletters = {'b': 'q', 'j': 'ia', 'x': 'ks'}
    for key in forbiddenletters.keys():
        Current_Word = Current_Word.replace(key, forbiddenletters[key])

    ##### cheap equal chunks hyphenation ########
    ##### to do maybe: replace this with english hyphenation ######
    '''
    ########## HYPHENATION ############# (correct english hyphenation - use this later to make stuff better v2.0)
    hyphens = hyphenate_word(Current_Word)
    print(hyphens)
    '''

    Current_Word_Length = len(str(Current_Word))
    Hyphens_Length = math.sqrt(Current_Word_Length)
    Hyphens_Rounded = int(Hyphens_Length)
    hyphens = [Current_Word[i:i+Hyphens_Rounded] for i in range(0, len(Current_Word), Hyphens_Rounded)]

    ########## MAPPING TABLES ########################
    # TO DO: USE DISTRIBUTION FUNCTIONS TO GENERATE WEIGHT MAPPING PAIRS
    # TO DO: load and save tables from csv to keep things neat, find a way to visualize distributions

    '''
    X = stats.binom(10, 0.2) # Declare X to be a binomial random variable
    print(X.pmf(3))          # P(X = 3)
    print(X.cdf(4))          # P(X <= 4)
    print(X.mean())          # E[X]
    print(X.var())           # Var(X)
    print(X.std())           # Std(X)
    print(X.rvs())           # Get a random sample from X
    print(X.rvs(10))         # Get 10 random samples form X
    
    print(X)
    '''

    # ! = missing audio TO DO: EXTRACT MORE SYLLABLES FROM WIKI AUDIO (about 10% done PepeHands)
    dict_charpairs = {'a': ["ac", "ach", "ah", "ahm", "ahmi", "al", "ala", "ark", "as", "ash", "ath", "atho"],
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
    weights_dict = {"a": [1, 2, 2, 2, 3, 2, 3, 3, 2, 3, 2, 1],
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
                    "z": [1, 2]}

    char_amt = []
    start_chars = []
    iterations = len(hyphens)
    for i in range(iterations):
        char_amt.append(len(hyphens[i]))
        start_chars.append(hyphens[i][:1])


    oz_sample_file = "./oz_audiolist.csv"
    oz_audiolist = []
    your_dir = "audio"
    with open(oz_sample_file) as csvfile:
        dictionary = csv.reader(csvfile, delimiter=' ')
        for row in dictionary:
            oz_audiolist.append(','.join(row))
    # ########## MAPPING TABLES END #########################

    # ###### REPLACEMENT/TRANSLATION START ##################
    # # could do many other things here instead!
    # get number of characters in each hyphen, append to list
    # get start character for each hyphen, append to list


    # weighted random pick to replace hyphen depending on english start character
    ozwordlist = []
    pathlist = []
    audionamelist = []
    randompick = ''
    for i in start_chars:
        character_mapping = dict_charpairs.get(i)
        weightlist_mapping = weights_dict.get(i)
        ozk_audio_result = str(random.choices(population=character_mapping, weights=weightlist_mapping, k=1)) # returns randomly weighted pick from ozk syllables
        ozwordlist.append(ozk_audio_result)

        ################## A U D I O ####################
        #append = random.randrange(0,num_files)
        audioname = str(re.sub(r'\W+', '', ozk_audio_result))
        #print(randompick)
        print(audioname, "is audioname")
        audio_filepath = './audio/' + audioname + '.wav' #
        print("searching for", audioname, "in", audio_filepath)
        pathlist.append(audio_filepath)

    
    # print the new ozk word
    ozwordlist = str(ozwordlist)
    ozword = [character for character in ozwordlist if character.isalnum()]
    ozword = "".join(ozword)
    print("oz word is", ozword)

    #### AUDIO PROCESSING ####

    # TO DO: for added variation later on, export multiple versions with random parameters for pitch, stretch etc
    # maybe variations for questions and exclamations?! (if the speech to text picks up on that)
    # do something about legion commanders responses sticking out so much (kick them out or distort etc)

    ### REMOVING SILENCE FUNCTION ####

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

    combined_audio = AudioSegment.empty()
    rdm_audiopick_list = []
    randompick = ""
    audioisvalid = False
    
    ########## Random Pick function##########    
    def random_pick():
        global rdm_audiopick_list
        global randompick
        rdm_audiopick_list = []
        for filename in glob.glob('./audio/'+ audioname +'.wav'):
            print('FILENAME IS' + filename)
            rdm_audiopick_list.append(filename)
        for filename in glob.glob('./audio/'+ audioname +'[0-9]'+'.wav'):
            rdm_audiopick_list.append(filename)
            print(rdm_audiopick_list)
        randompick = str(random.choices(rdm_audiopick_list)).replace('[','').replace(']','').replace("'",'')
        return randompick

    ########## Combine and trim audio function##########
    def combine_audios(audiopath):
        """
        Takes audiopath trims the silence and appends the audios
        """
        global combined_audio
        src_audio = AudioSegment.from_wav(audiopath)
        print("Trimming Audiofiles..")
        duration = len(src_audio)
        start_trim = detect_silence(src_audio)
        end_trim = detect_silence(src_audio.reverse())
        trimmed_audio = src_audio[start_trim:duration - end_trim]
        end = trimmed_audio[-100:]
        combined_audio += trimmed_audio.append(end, crossfade=100)
        return combined_audio

    ######### Check our list of filepaths #########
    for i in pathlist:
        wav_filepath = i
        print(i)
        audioname = wav_filepath.replace('.wav', '').replace('./audio/', '')
        # if condition cannot be replaced because we dont have all syllables yet
        if audioname in oz_audiolist:
            audioisvalid = True
            random_pick()
            print("random pick is", randompick)
            print("Samples found! Creating combined Audiosnippet...")
            combine_audios(randompick)
        else:
            print("Syllable not found!!")
            audioisvalid = False
    ### Make Directory for Combined audios if it doesnt exist yet ###
    if not os.path.exists('./combined'):
        os.makedirs('./combined')

    #### FINAL EXPORT ####
    if audioisvalid == True:
        print("Exporting audio to disk ...")
        combined_audio.export("./combined/_" + ozword + "_" + Current_Word + "_combined.wav", format="wav")
        print("Exported succesfully!")
