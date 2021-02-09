import os
import glob
import pandas as pd
import csv
import math
import random
import re
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


def export_word():
    global word_temp_id
    global sentence_index
    if not os.path.exists('./TEMP'):
        os.makedirs('./TEMP')
    word_temp_id += 1
    temp_id = str(word_temp_id)
    temp_id = temp_id.zfill(3)
    sentence_index += 1
    str_sentence_index = str(sentence_index)
    str_sentence_index = str_sentence_index.zfill(3)
    print("Word", str_sentence_index, "exported")
    combined_audio.export("./TEMP/" + str(str_sentence_index) + str(oz_word) + str(temp_id) + ".wav", format="wav")


def combine_sentence():
    global word_audio
    global full_sentence_audio
    full_sentence_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=220)
    for filename in glob.glob('./TEMP/'+'*.wav'):
        word_audio = AudioSegment.from_wav(filename)
        full_sentence_audio += word_audio + silence


def delete_tempwords():
    for files in glob.glob('./TEMP/'+'*.wav'):
        os.remove(files)


# init

oz_syllable_mapping = {
    'a': ["ac", "ach", "ah", "ahm", "al", "ar", "as", "ash", "ath"],
    'c': ["ch", "cha"],
    'd': ["do", "dom", "doq"],
    'e': ["ek", "en", "ey"],
    'f': ["fa", "fe", "fek", "fi", "fo"],
    'g': ["gl", "glu", "gr", "gro"],
    'h': ["ha", "hag", "has", "he", "hm", "ho", "hol", "hro"],
    'i': ["ich", "ik", "iru", "is", "isk", "iz", "izh"],
    'k': ["ka", "kala", "kath", "ko"],
    'l': ["lo", "lof", "lom"],
    'm': ["mi", "mis", "mo", "moz"],
    'n': ["ne", "ni", "ns"],
    'o': ["of", "ok", "ol", "om", "omf", "omo", "oq", "osh", "oth", "ov", "oz", "ozh"],
    'p': ["po", "pr", "pz"],
    'q': ["oq", "ok"],
    'r': ["ro", "ros", "rush"],
    's': ["se", "sek", "sh", "shk", "so", "sof", "sol", "sov"],
    't': ["ta", "tak", "th", "tho"],
    'u': ["uch", "ucha", "uth"],
    'v': ["vo", "vot", "voth", "vr", "vro"],
    'w': ["wr"],
    'y': ["yi"],
    'z': ["zh"]}
# nicht uniforme zufallsvariable hier
weight_mapping = {
    "a": [1, 2, 1, 2, 2, 3, 2, 3, 2],
    "c": [1, 2],
    "d": [1, 2, 2],
    "e": [2, 3, 2],
    "f": [1, 2, 2, 3, 2],
    "g": [3, 2, 2, 2],
    "h": [1, 2, 2, 2, 2, 1, 2, 2], #
    "i": [2, 3, 3, 2, 1, 3, 2],
    "l": [1, 2, 2],
    "m": [1, 1, 1, 2],
    "n": [2, 2, 1],
    "o": [1, 2, 3, 3, 3, 3, 2, 2, 2, 3, 3, 2],
    "p": [1, 2, 2],
    "q": [1, 2],
    "r": [1, 2, 2],
    "s": [1, 2, 3, 3, 3, 3, 3, 3],
    "t": [1, 2, 2, 1],
    "u": [1, 2, 2],
    "v": [1, 2, 3, 2, 3],
    "w": [1],
    "y": [1],
    "z": [2]
}
forbidden_letters = {'b': 'q', 'j': 'o', 'x': 'o'}
audio_dir = "audio"
oz_available_audio = []
oz_sample_file = "./oz_audiolist.csv"
with open(oz_sample_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
        oz_available_audio.append(','.join(row))

word_temp_id = 0
sentence_index = 0
wav_export_id = 0
combined_word_audio = AudioSegment.empty()
combined_audio = AudioSegment.empty()
train_df = pd.DataFrame()

# load dataframe
df = pd.read_pickle('df_translation.pkl')
df2 = pd.read_pickle('df_training.pkl')
f = open('test.txt', 'r')
poem = f.readlines()

for lines in poem:
    lines = lines.lower()
    print("line in poem is:", lines)
    sentence = lines.split()
    for en_word in sentence:
        en_word = [character for character in str.lower(en_word) if character.isalnum()]
        en_word = "".join(en_word)

        if df['english'].eq(en_word).any():
            audio_pathlist = []
            print(en_word, "found")
            entry = df.loc[df['english'] == en_word]
            #print(entry)
            oz_word = entry.iloc[0].iloc[1]
            recombine_sylls = entry.iloc[0].iloc[2]
            #print(recombine_sylls)

            for i in recombine_sylls:
                audiostring = str(i)
                # print(audiostring, "is audio string")
                audio_filepath = './audio/' + audiostring + '.wav'
                audio_pathlist.append(audio_filepath)
                # print("searching for audio", audiostring, "in path", audio_filepath)

            for i in audio_pathlist:
                audio_filepath = i
                audio_name = audio_filepath.replace('.wav', '').replace('./audio/', '')
                if audio_name in oz_available_audio:
                    audioisvalid = True
                    random_pick()
                    # print("Sample", randompick, "found! Trimming and Appending Syllable...")
                    combine_syllables()
                else:
                    audioisvalid = False
                    print("Sample not found in recombine loop")
            export_word()
            # empty pathlist and audio segment for next word
            audio_pathlist = []
            repick_sylls = []
            combined_audio = AudioSegment.empty()

        else:
            print(en_word, " - no translation found in dataframe")
            en_hyphens = hyphenate_word(en_word)
            trl_word = en_word
            trl_hyphens = en_hyphens
            temp_hyphens = []
            for hyphen in en_hyphens:
                print(hyphen)
                for key in forbidden_letters.keys():
                    hyphen = hyphen.replace(key, forbidden_letters[key])
                temp_hyphens.append(hyphen)

            print(temp_hyphens)
            hyphens = temp_hyphens
            if len(en_hyphens) == 1:
                word_len = len(str(en_word))
                hyphens_len = math.sqrt(len(en_word))
                hyphens_rounded = int(hyphens_len)
                if hyphens_rounded == 0:
                    hyphens_rounded += 1
                hyphens = [en_word[i:i + hyphens_rounded] for i in
                           range(0, word_len, hyphens_rounded)]
                # print(hyphens, "are hyphens in custom translate condition")

            char_amt = []
            start_chars = []
            iterations = len(hyphens)
            for i in range(iterations):
                char_amt.append(len(hyphens[i]))
                start_chars.append(hyphens[i][:1])
            oz_syllables = []
            audio_pathlist = []

            for chars in start_chars:
                char_map = oz_syllable_mapping.get(chars)
                weights_map = weight_mapping.get(chars)
                oz_syllable_pick = str(random.choices(population=char_map, weights=weights_map, k=1))
                # create clean string for syllable list
                oz_syllable_pick = str(re.sub(r'\W+', '', oz_syllable_pick))
                oz_syllables.append(oz_syllable_pick)
                # create clean string to look for audio
                audio_name = str(re.sub(r'\W+', '', oz_syllable_pick))
                audio_filepath = './audio/' + audio_name + '.wav'
                # print("searching for audio name", audio_name, "in path", audio_filepath)
                audio_pathlist.append(audio_filepath)

            oz_word = str(oz_syllables)
            oz_word = [character for character in oz_word if character.isalnum()]
            oz_word = "".join(oz_word)

            for i in audio_pathlist:
                wav_filepath = i
                audio_name = wav_filepath.replace('.wav', '').replace('./audio/', '')
                if audio_name in oz_available_audio:
                    audioisvalid = True
                    random_pick()
                    print("Sample found! Trimming and Appending Syllable...")
                    combine_syllables()
                else:
                    audioisvalid = False
                    print("Sample not found in Lookup Table TRANSLATION LOOP")
            
            # update the dataframe
            df.loc[len(df.index)] = [en_word, oz_word, oz_syllables]

            export_word()
            # empty pathlist and audio segment for next word
            audio_pathlist = []
            combined_audio = AudioSegment.empty()
            oz_syllables = []
            # END TRANSLATION LOOP =)
    print("Exporting sentence audio to disk ...")
    combine_sentence()
    wav_export_id += 1
    LJCounter = str(wav_export_id)
    LJCounter = LJCounter.zfill(4)
    full_sentence_audio.export("./sentences/" + "Sentence" + LJCounter + ".wav", format="wav")
    delete_tempwords()
    word_temp_id = 0
    sentence_index = 0
    # update the training df

print(df.tail(-50))
# save the dataframes
df.to_pickle('df_translation.pkl')
df2.to_pickle('df_training.pkl')
