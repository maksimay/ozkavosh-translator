import os
import glob
import csv
import re
import random
import math
import re
from unidecode import unidecode
from hyphenate import hyphenate_word
from pydub import AudioSegment


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


def random_pick():
    global rdm_audiopick_list
    global randompick
    rdm_audiopick_list = []
    for filename in glob.glob('./audio/' + audio_name + '.wav'):
        #print('FILENAME IS' + filename)
        rdm_audiopick_list.append(filename)
    for filename in glob.glob('./audio/' + audio_name + '[0-9]' + '.wav'):
        rdm_audiopick_list.append(filename)
        #print('FILENAME IS' + filename)
        # print(rdm_audiopick_list)
    randompick = str(random.choices(rdm_audiopick_list)).replace('[', '').replace(']', '').replace("'", '')
    # print(randompick, "is random pick!")


def combine_syllables():
    global combined_audio
    # combined_audio = AudioSegment.empty()
    src_audio = AudioSegment.from_wav(randompick)
    # print("Trimming Audiofiles..")
    duration = len(src_audio)
    start_trim = detect_silence(src_audio)
    end_trim = detect_silence(src_audio.reverse())
    trimmed_audio = src_audio[start_trim:duration - end_trim]
    end = trimmed_audio[-100:]
    combined_audio += trimmed_audio.append(end, crossfade=100)


def combine_sentence():
    global word_audio
    global full_sentence_audio
    full_sentence_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=220)
    for filename in glob.glob('./TEMP/'+'*.wav'):
        word_audio = AudioSegment.from_wav(filename)
        full_sentence_audio += word_audio + silence


def export_word():
    global TempID
    global inSentenceID
    if not os.path.exists('./TEMP'):
        os.makedirs('./TEMP')
    TempID += 1
    xTempID = str(TempID)
    xTempID = xTempID.zfill(3)
    inSentenceID += 1
    xinSentenceID = str(inSentenceID)
    xinSentenceID = xinSentenceID.zfill(3)
    print("Word", xinSentenceID, "exported")
    combined_audio.export("./TEMP/" + str(xinSentenceID) + str(oz_word) + str(xTempID) + ".wav", format="wav")


def delete_tempwords():
    for files in glob.glob('./TEMP/'+'*.wav'):
        os.remove(files)


def get_key(val):
    for key, value in Synonym_Dictionary.items():
        if val in value:
            return key

    return "key doesn't exist"


_whitespace_re = re.compile(r'\s+')


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
  return unidecode(text)


def lowercase(text):
  return text.lower()


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  '''Pipeline for English text, including number and abbreviation expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  return text

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]
if not os.path.exists('./sentences'):
    os.makedirs('./sentences')
# initialise variables
combined_word_audio = AudioSegment.empty()
combined_audio = AudioSegment.empty()
ExportID = 0
TempID = 0
inSentenceID = 0
audio_pathlist = []

# syllable audio directory
audio_dir = "audio"
# list of syllables to pick from ( syllable1 syllable2 can be removed? test later)
oz_sample_file = "./oz_audiolist.csv"

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
forbidden_letters = {'b': 'q', 'j': 'i', 'x': 'k'}
# initialise dicts

# read in available key value pairs | en, ozk
with open('Translation_Dictionary.csv', mode='r') as infile:
    reader = csv.reader(infile, delimiter='|')
    Translation_Dictionary = {rows[0]: rows[1] for rows in reader}
# read in list of available syllables | ozk, ['syll1','syll2','syll3']
with open('Syllable_Dictionary.csv', mode='r') as infile:
    reader = csv.reader(infile, delimiter='|')
    Syllable_Dictionary = {rows[0]: rows[1] for rows in reader}
# read in direct translations and wordnet synonyms | {ozk:[en1,...]}
with open('synonym_dict.csv', mode='r') as infile:
    reader = csv.reader(infile)
    Synonym_Dictionary = {rows[0]: rows[1:] for rows in reader}

# assign each value to a new key to update en<->ozk dictionary with synonyms and direct translations from wiki
for key, value in Synonym_Dictionary.items():
    for i in value:
        Translation_Dictionary.update({i: get_key(i)})
# clean the key

Translation_Dictionary = {key.replace('[', '').replace(']', '').replace("'", '').replace(" ", ''): value
                          for key, value in Translation_Dictionary.items()}


# update syllable picks for direct wiki translation words to find audio files
if os.stat('Syllable_Dictionary.csv').st_size == 0:
    print("syllable dict empty, populating with direct word translations")
    wikiwords = []
    for key in Synonym_Dictionary.keys(): # this is the SYN dict (list of ozk words)
        wikiwords.append(key)
        Syllable_Dictionary[key] = wikiwords # this is the SYLL dict (syll = ozk word = arkosh1,2,3.wav)
        wikiwords = []

# re save the dict
with open('Translation_Dictionary.csv', 'w') as f:
    for key in Translation_Dictionary.keys():
        f.write("%s,%s\n" % (key, Translation_Dictionary[key]))


# initialise list of available syllable audios # this was previously inside the translation loop
oz_available_audio = []
# read in list of available ozk syllable variations aka audio files ek, ek1, ek2...
with open(oz_sample_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
        oz_available_audio.append(','.join(row))

f = open('test.txt', 'r')
poem = f.readlines()
for lines in poem:
    lines = lines.lower()

    print("line in poem is:", lines)
    sentence = lines.split()
    for en_word in sentence:
        # print("iterating over", en_word)
        # remove any special characters
        en_word = [character for character in str.lower(en_word) if character.isalnum()]
        en_word = "".join(en_word)
        # replace forbidden english letters with ozkavosh lore friendly ones
        for key in forbidden_letters.keys():
            en_word = en_word.replace(key, forbidden_letters[key])
        # hyphenate word
        en_hyphens = hyphenate_word(en_word)
        print(en_hyphens, "is en_hyphenation")
        # check if the word already has a translation, recombine it and export audio variation
# ################     ##############################################################################################
        if en_word in Translation_Dictionary.keys():
            # get the ozkavosh word
            oz_word = Translation_Dictionary[en_word]
            print("iterating over known word", oz_word, "(", en_word, ")")
            audio_pathlist = []
            # get list of ozkavosh syllables
            repick_sylls = []
            repick_sylls.append(Syllable_Dictionary[oz_word])
            # repick_sylls.append(Syllable_Dictionary[oz_word])
            print(repick_sylls, "is repick_sylls")
            # get clean string from list entry to look for audio file (WORKAROUND)
            for i in repick_sylls:
                audiostring = str(i).replace('[', '').replace(']', '').replace("'", '').replace(" ", '').replace('"', '').replace('\\', '').replace('/', '')
                print(audiostring, "is audio string")
                audio_filepath = './audio/' + audiostring + '.wav'
                audio_pathlist.append(audio_filepath)
                print("searching for audio", audiostring, "in path", audio_filepath)

            # pick a random variation for each syllable and combine word audio
            print(audio_pathlist)
            for i in audio_pathlist:
                wav_filepath = i
                audio_name = wav_filepath.replace('.wav', '').replace('./audio/', '')
                if audio_name in oz_available_audio:
                    audioisvalid = True
                    random_pick()
                    print("Sample", randompick, "found! Trimming and Appending Syllable...")
                    # append randomly chosen syllable audio to previous audio block
                    combine_syllables()
                else:
                    audioisvalid = False
                    print("Sample not found in Lookup Table RECOMBINE LOOP")
            export_word()
            # empty pathlist and audio segment for next word
            audio_pathlist = []
            repick_sylls = []
            combined_audio = AudioSegment.empty()
# #################       ############################################################################################
        if en_word not in Translation_Dictionary.keys():
            print("no translation key for", en_word, "found in dict")
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
            # en_syllable start characters, assign rand ozk syllable to each one, make list of audios for random pick
            for i in start_chars:
                char_map = oz_syllable_mapping.get(i)
                weights_map = weight_mapping.get(i)
                oz_syllable_pick = str(random.choices(population=char_map, weights=weights_map, k=1))
                oz_syllables.append(oz_syllable_pick)
                # create clean audio string
                audio_name = str(re.sub(r'\W+', '', oz_syllable_pick))
                audio_filepath = './audio/' + audio_name + '.wav'
                # print("searching for audio name", audio_name, "in path", audio_filepath)
                # append to list for random syllable pick
                audio_pathlist.append(audio_filepath)
            # clean word string
            oz_word = str(oz_syllables)
            oz_word = [character for character in oz_word if character.isalnum()]
            oz_word = "".join(oz_word)


            val = []
            for i in oz_syllables:
                valstr = str(i).replace('[', '').replace(']', '').replace("'", '').replace(" ", '').replace('"', '').replace('\\', '').replace('/', '')
                val.append(valstr)

            Syllable_Dictionary[oz_word] = val


            print("syllable list for", oz_word, "added to dict as", val, "\n")
            # update english to ozkavosh dictionary
            Translation_Dictionary[en_word] = oz_word
            print("translation for", en_word, "added to dict as", oz_word, "\n")
            # print(audio_pathlist, "AUDIO PATHLIST ENTRIES")
            # pick a random variation for each syllable
            # rand syllable selection, combine word audio
            for i in audio_pathlist:
                wav_filepath = i
                audio_name = wav_filepath.replace('.wav', '').replace('./audio/', '')
                if audio_name in oz_available_audio:
                    audioisvalid = True
                    random_pick()
                    # print("Sample found! Trimming and Appending Syllable...")
                    combine_syllables()
                else:
                    audioisvalid = False
                    print("Sample not found in Lookup Table TRANSLATION LOOP")

            export_word()
            # empty pathlist and audio segment for next word
            audio_pathlist = []
            combined_audio = AudioSegment.empty()
            oz_syllables = []
            # END TRANSLATION LOOP =)

    print("Exporting sentence audio to disk ...")
    combine_sentence()
    ExportID += 1
    LJCounter = str(ExportID)
    LJCounter = LJCounter.zfill(3)
    csvaudiofilepath = "./sentences/" + str(sentence) + LJCounter + ".wav"
    full_sentence_audio.export("./sentences/" + "Sentence" + LJCounter + ".wav", format="wav")
    delete_tempwords()
    TempID = 0
    SentenceID = 0


    with open('LJSpeech.csv', 'a+', newline='') as csvfile:
        fieldnames = ["audio", "transcription"]
        LJSpeechwriter = csv.DictWriter(csvfile, delimiter="|", fieldnames=fieldnames)
        LJSpeechwriter.writerow({"audio": csvaudiofilepath, "transcription": lines})

with open('Syllable_Dictionary.csv', 'w') as f:
    for key in Syllable_Dictionary.keys():
        f.write("%s|%s\n" % (key, Syllable_Dictionary[key]))
'''
with open('Syllable_Dictionary.csv', 'w', newline='') as csvfile:
    fieldnames = ["ozkavosh", "syllables"]
    SyllWriter = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
    for key, value in Syllable_Dictionary.keys():
        SyllWriter.writerow({"ozkavosh": key, "syllables": value})
'''

with open('Translation_Dictionary.csv', 'w') as f:
    for key in Translation_Dictionary.keys():
        f.write("%s|%s\n" % (key, Translation_Dictionary[key]))


