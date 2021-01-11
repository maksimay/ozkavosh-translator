import random
import math
import csv
import re
import os
import glob
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
        # print('FILENAME IS' + filename)
        rdm_audiopick_list.append(filename)
    for filename in glob.glob('./audio/' + audio_name + '[0-9]' + '.wav'):
        rdm_audiopick_list.append(filename)
        # print(rdm_audiopick_list)
    randompick = str(random.choices(rdm_audiopick_list)).replace('[', '').replace(']', '').replace("'", '')
    print(randompick, "is random pick!")


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


def combine_sentence():
    global word_audio
    global full_sentence_audio
    full_sentence_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=300)
    for filename in glob.glob('./TEMP/'+'*.wav'):
        word_audio = AudioSegment.from_wav(filename)
        full_sentence_audio += word_audio + silence


def export_words():
    if not os.path.exists('./TEMP'):
        os.makedirs('./TEMP')
    combined_audio.export("./TEMP/" + str(ozk_word) + ".wav", format="wav")


def delete_tempwords():
    for files in glob.glob('./TEMP/'+'*.wav'):
        os.remove(files)


combined_audio = AudioSegment.empty()
ExportID = 0
audio_dir = "audio"
oz_sample_file = "./oz_audiolist.csv" # NEEDS UPDATING

with open('Translation_Dictionary.csv', mode='r') as infile:
    reader = csv.reader(infile)
    Translation_Dictionary = {rows[0]: rows[1] for rows in reader}

dict_charpairs = {
    'a': ["ac", "ach", "ah", "ahm", "ahmi", "al", "ala", "ark", "as", "ash", "ath", "atho"],
    'c': ["ch", "cha"],
    'd': ["do", "dom", "doq"],
    'e': ["ek", "en", "ey"],
    'f': ["fa", "fath", "fe", "fek", "fi", "fo", "fol"],
    'g': ["gl", "glu", "gr", "gro", "groth"],
    'h': ["ha", "hag", "has", "he", "hedo", "hm", "ho", "hol", "hro"],
    'i': ["ich", "ik", "iru", "is", "isk", "iz", "izh"],
    'k': ["ka", "kala", "kath", "ko"],
    'l': ["lo", "lof", "lofa", "lom"],
    'm': ["mi", "mis", "mo", "moz"],
    'n': ["ne", "ni", "ns"],
    'o': ["of", "ok", "ol", "om", "omf", "omo", "oq", "osh", "oth", "ov", "oz", "ozh"],
    'p': ["po", "pr", "pz"],
    'q': ["oq", "ok"],
    'r': ["ro", "ros", "rush"],
    's': ["se", "sek", "sh", "shk", "so", "sof", "sol", "sov", "sovo"],
    't': ["ta", "tak", "th", "tho"], # thu do
    'u': ["uch", "uth"],
    'v': ["vo", "vot", "voth", "vr", "vro", "vroshk"],
    'w': ["wr"],
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
    "i": [1, 3, 3, 2, 1, 3, 2],
    "l": [1, 2, 2, 2],
    "m": [1, 1, 1, 2],
    "n": [1, 2, 2],
    "o": [1, 2, 3, 3, 3, 3, 2, 2, 2, 3, 3, 2],
    "p": [1, 2, 2],
    "q": [1, 2],
    "r": [1, 2, 2],
    "s": [1, 2, 3, 3, 3, 3, 3, 3, 2],
    "t": [1, 2, 2, 1],
    "u": [1, 2],
    "v": [1, 2, 2, 2, 2, 2],
    "w": [1],
    "y": [1],
    "z": [1, 2]
}

if not os.path.exists('./sentences'):
    os.makedirs('./sentences')

forbidden_letters = {'b': 'q', 'j': 'i', 'x': 'k'}

f = open('test.txt', 'r')
poem = f.readlines()

for lines in poem:
    lines = lines.lower()
    print("line in poem is:", lines)
    sentence = lines.split()
    for en_word in sentence:
        print("looping over", en_word)
        value = 1
        if value == 1:  # words not in Translation_Dictionary.keys():
            print("no translation key for", en_word, "found in dict")
            Translation_Word = en_word
            Translation_Word = [character for character in str.lower(Translation_Word) if character.isalnum()]
            Translation_Word = "".join(Translation_Word)

            for key in forbidden_letters.keys():
                Translation_Word = Translation_Word.replace(key, forbidden_letters[key])

            Translation_Word_Length = len(str(Translation_Word))
            Hyphens_Length = math.sqrt(Translation_Word_Length)
            Hyphens_Rounded = int(Hyphens_Length)
            if Hyphens_Rounded == 0:
                Hyphens_Rounded += 1
            hyphens = [Translation_Word[i:i + Hyphens_Rounded] for i in
                       range(0, Translation_Word_Length, Hyphens_Rounded)]

            char_amt = []
            start_chars = []
            iterations = len(hyphens)
            for i in range(iterations):
                char_amt.append(len(hyphens[i]))
                start_chars.append(hyphens[i][:1])

            ozk_syllables = []
            audio_pathlist = []
            print("audio path array cleared")

            for i in start_chars:
                char_map = dict_charpairs.get(i)
                weights_map = weights_dict.get(i)
                ozk_syllable_result = str(random.choices(population=char_map, weights=weights_map, k=1))
                ozk_syllables.append(ozk_syllable_result)

                audio_name = str(re.sub(r'\W+', '', ozk_syllable_result))
                # print(audio_name, "is name of audio")
                audio_filepath = './audio/' + audio_name + '.wav'
                print("searching for audio name", audio_name, "in path", audio_filepath)
                audio_pathlist.append(audio_filepath)

            ozk_word = str(ozk_syllables)
            ozk_word = [character for character in ozk_word if character.isalnum()]
            ozk_word = "".join(ozk_word)
            print("oz word is", ozk_word)

            oz_audiolist = []

            with open(oz_sample_file) as csvfile:
                dictionary = csv.reader(csvfile, delimiter=' ')
                for row in dictionary:
                    oz_audiolist.append(','.join(row))
            print(audio_pathlist, "AUDIO PATHLIST ENTRIES")
            for i in audio_pathlist:
                wav_filepath = i
                audio_name = wav_filepath.replace('.wav', '').replace('./audio/', '')
                if audio_name in oz_audiolist:
                    audioisvalid = True
                    random_pick()
                    print("random pick is", randompick)
                    print("Samples found! Creating combined Audiosnippet...")
                    combine_audios()
                else:
                    print("Syllable not found in Lookup Table")
                    audioisvalid = False

            # ### CREATE NEW DICTIONARY ENTRY
            Translation_Dictionary.update({en_word: ozk_word})
            print("translation for", en_word, "added to dict as", ozk_word, "\n")
            # ### EXPORT THE WORDS AS SINGLE AUDIOS ###
            export_words()
            # ### EMPTY THE SEGMENT AND PATHLIST FOR THE NEXT WORD
            audio_pathlist = []
            combined_audio = AudioSegment.empty()

        else:
            # ozk_word = Translation_Dictionary.get(words)
            print(ozk_word, "was direct wiki translation for", en_word)

    print("Exporting audio to disk ...")
    combine_sentence()
    delete_tempwords()
    ExportID += 1
    LJCounter = str(ExportID)
    LJCounter = LJCounter.zfill(3)

    full_sentence_audio.export("./sentences/" + str(sentence) + LJCounter + ".wav", format="wav")
    csvaudiofilepath = "./sentences/" + str(sentence) + LJCounter + ".wav"

    with open('LJSpeech.csv', 'a+', newline='') as csvfile:
        fieldnames = ["audio", "transcription"]
        LJSpeechwriter = csv.DictWriter(csvfile, delimiter="|", fieldnames=fieldnames)
        LJSpeechwriter.writerow({"audio": csvaudiofilepath, "transcription": lines})