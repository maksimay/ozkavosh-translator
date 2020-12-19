import random
import math
import csv
from pydub import AudioSegment
import glob
import re
import os
import glob
import nltk

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
    for filename in glob.glob('./audio/' + audio_name + '.wav'):
        #print('FILENAME IS' + filename)
        rdm_audiopick_list.append(filename)
    for filename in glob.glob('./audio/' + audio_name + '[0-9]' + '.wav'):
        rdm_audiopick_list.append(filename)
        #print(rdm_audiopick_list)
    randompick = str(random.choices(rdm_audiopick_list)).replace('[', '').replace(']', '').replace("'", '')

########## Combine and trim audio function##########
def combine_audios():
    global combined_audio
    src_audio = AudioSegment.from_wav(randompick)
    # print("Trimming Audiofiles..")
    duration = len(src_audio)
    start_trim = detect_silence(src_audio)
    end_trim = detect_silence(src_audio.reverse())
    trimmed_audio = src_audio[start_trim:duration - end_trim]
    end = trimmed_audio[-100:]
    combined_audio += trimmed_audio.append(end, crossfade=100)

#tokens = nltk.sent_tokenize(contents)
#for t in tokens:
    #print (t, "\n")

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

f = open('tolkien.txt', 'r')
poem = f.readlines()

### Make Directory for Combined audios if it doesnt exist yet ###
if not os.path.exists('./combined'):
    os.makedirs('./combined')

for lines in poem:
    audio_pathlist = []
    lines = lines.lower()
    #print("sentence is: ", lines)
    print(lines)
    # translate words that are not in the dict and update dict
    sentence = lines.split()
    for words in sentence: # for each of the words in sentence
        print(words)

        ozk_syllables = []  # list of new Ozkavosh syllables

        randompick = ''

        if words not in Translation_Dictionary.keys():
            # translator.py loop:
            print("no translation key for", words, "found in dict")
            Translation_Word = words
            Translation_Word = [character for character in str.lower(Translation_Word) if character.isalnum()]
            Translation_Word = "".join(Translation_Word)
            forbidden_letters = {'b': 'q', 'j': 'i', 'x': 'k'}

            for key in forbidden_letters.keys():
                Translation_Word = Translation_Word.replace(key, forbidden_letters[key])

            Translation_Word_Length = len(str(Translation_Word))
            Hyphens_Length = math.sqrt(Translation_Word_Length)
            Hyphens_Rounded = int(Hyphens_Length)
            if Hyphens_Rounded == 0:
                Hyphens_Rounded += 1
            hyphens = [Translation_Word[i:i + Hyphens_Rounded] for i in range(0, Translation_Word_Length, Hyphens_Rounded)]

            char_amt = []  # how many characters each syllable will have
            start_chars = []  # list of English syllable start characters for Ozkavosh lookup replacement

            iterations = len(hyphens)
            for i in range(iterations):
                char_amt.append(len(hyphens[i]))
                start_chars.append(hyphens[i][:1])

            ozk_syllables = []

            for i in start_chars:
                character_mapping = dict_charpairs.get(i)
                weightlist_mapping = weights_dict.get(i)
                ozk_syllable_result = str(random.choices(population=character_mapping, weights=weightlist_mapping,k=1))  # returns randomly weighted pick from ozk syllables
                ozk_syllables.append(ozk_syllable_result)

                ################## A U D I O P A T H ###################

                audio_name = str(re.sub(r'\W+', '', ozk_syllable_result))
                print(audio_name, "is audioname")
                audio_filepath = './audio/' + audio_name + '.wav'  #
                print("searching for", audio_name, "in", audio_filepath)
                audio_pathlist.append(audio_filepath)

            # print the new ozk word
            ozk_word = str(ozk_syllables)
            ozk_word = [character for character in ozk_word if character.isalnum()]
            ozk_word = "".join(ozk_word)
            print("oz word is", ozk_word)

            oz_sample_file = "./oz_audiolist.csv"
            oz_audiolist = []
            your_dir = "audio"
            with open(oz_sample_file) as csvfile:
                dictionary = csv.reader(csvfile, delimiter=' ')
                for row in dictionary:
                    oz_audiolist.append(','.join(row))

            for i in audio_pathlist:
                wav_filepath = i
                #print(i)
                audio_name = wav_filepath.replace('.wav', '').replace('./audio/', '')
                # if condition cannot be replaced because we dont have all syllables yet
                if audio_name in oz_audiolist:
                    audioisvalid = True
                    random_pick()
                    print("random pick is", randompick)
                    print("Samples found! Creating combined Audiosnippet...")
                    combine_audios()

                else:
                    print("Syllable not found!!")
                    audioisvalid = False

            audio_pathlist = []
            ozk_word = str(ozk_syllables)
            ozk_word = [character for character in ozk_word if character.isalnum()]
            ozk_word = "".join(ozk_word)  # get a clean Ozkavosh string for printing
            print("ozkavosh word is", ozk_word)

            Translation_Dictionary.update({words: ozk_word})
            print("translation for", words, "added to dict")

        else:
            ozk_word = Translation_Dictionary.get(words)
            print(ozk_word, "was direct wiki translation for", words)

    #### FINAL EXPORT ####
    if audioisvalid == True:
        print("Exporting audio to disk ...")
        combined_audio.export("./combined/_" + ozk_word + "_combined.wav", format="wav")
        print("Exported succesfully!")

    audio_pathlist = []


    print(audio_filepath , words)
    with open('LJSpeech.csv', 'a+', newline='') as csvfile:
        fieldnames = ["audio", "transcription"]
        LJSpeechwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        LJSpeechwriter.writerow({"audio": audio_filepath, "transcription": lines})

