import os
import glob
import pandas as pd
import numpy as np
import csv
import math
import random
import re
from hyphenate import hyphenate_word
from pydub import AudioSegment


def detect_silence(sound, silence_threshold=-70.0, chunk_size=10):
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
    for filename in glob.glob('./audio_input/' + audio_name + '.wav'):
        # print('FILENAME IS' + filename)
        rdm_audiopick_list.append(filename)
    for filename in glob.glob('./audio_input/' + audio_name + '[0-9]' + '.wav'):
        rdm_audiopick_list.append(filename)
        # print('FILENAME IS' + filename)
        # print(rdm_audiopick_list)
    randompick = str(random.choices(rdm_audiopick_list)).replace('[', '').replace(']', '').replace("'", '')
    # print(randompick, "is random pick!")


def combine_syllables():
    global combined_audio
    src_audio = AudioSegment.from_wav(randompick)
    # print("Trimming Audiofiles..")
    duration = len(src_audio)
    start_trim = detect_silence(src_audio)
    end_trim = detect_silence(src_audio.reverse())
    trimmed_audio = src_audio[start_trim:duration - end_trim]
    trim_dur = len(trimmed_audio)
    end_offset = trim_dur * 0.5
    end = trimmed_audio[-end_offset:]
    combined_audio += trimmed_audio.append(end, crossfade=(end_offset-1))


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
    # print("Word", str_sentence_index, "exported")
    combined_audio.export("./TEMP/" + str(str_sentence_index) + str(oz_word) + str(temp_id) + ".wav", format="wav")


def combine_sentence():
    global word_audio
    global full_sentence_audio
    full_sentence_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=322)
    for filename in glob.glob('./TEMP/'+'*.wav'):
        word_audio = AudioSegment.from_wav(filename)
        full_sentence_audio += word_audio + silence


def combine_all_sentences():
    global sentence_audio
    global torch_training_audio
    torch_training_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=999)
    for filename in glob.glob('./training_audio/'+'*.wav'):
        sentence_audio = AudioSegment.from_wav(filename)
        torch_training_audio += sentence_audio + silence


def delete_tempwords():
    for files in glob.glob('./TEMP/'+'*.wav'):
        os.remove(files)


# init mappings
####################################################
#               alphabet : oz_sylls                #
####################################################
oz_syllable_mapping = {
    'a': ["ac", "ach", "ah", "ahm", "al", "ar", "as", "ash", "ath", "atho"], # 10
    'c': ["ch", "cha"],
    'd': ["do", "dom"],
    'e': ["ek", "en", "ey"],
    'f': ["fa", "fe", "fek", "fi", "fo"],
    'g': ["gl", "glu", "gr", "gro"],
    'h': ["ha", "hag", "has", "he", "hm", "ho", "hol", "hro"], # 8
    'i': ["ich", "ik", "iru", "is", "isk", "iz", "izh"],
    'k': ["ka", "kala", "kath", "ko"],
    'l': ["lo", "lof", "lom"],
    'm': ["mi", "mis", "mo", "moz"],
    'n': ["ne", "ni", "ns"],
    'o': ["of", "ok", "ol", "om", "omf", "omo", "oq", "osh", "oth", "ov", "oz", "ozh"], # 12
    'p': ["po", "pr", "pz"],
    'q': ["oq", "ok"],
    'r': ["ro", "ros", "rush"],
    's': ["se", "sek", "sh", "shk", "so", "sof", "sol", "sov"],
    't': ["ta", "tak", "th", "tho"],
    'u': ["uch", "uth", "ul"],
    'v': ["vo", "vot", "voth", "vr", "vro"],
    'w': ["wr"],
    'y': ["yi"],
    'z': ["zh"]
}

oz_phoneme_mapping = {
'izhai': ["IY", "ZH", "AA", "Y"],
'ozkavosh': ["UH", "ZH", "K", "AA", "V", "UH", "SH"],
'sa': ["S", "AA"],
'vu': ["V", "UH"],
'doq': ["D", "UH", "K"],
'roq': ["R", "UH", "K"],
'doz': ["D", "UH", "K"],
'ahm': ["AA", "H", "M"],
'ashm': ["AA", "SH", "M"],
'vo': ["V", "UH"],
'vom': ["V", "UH", "M"],
'acha': ["AA", "K", "H", "AA"],
'icha': ["IY", "ZH", "AA"],
'ucha': ["UW", "ZH", "AA"],
'hollom': ["H", "UH", "L", "UH", "M"],
'wroth': ["W", "R", "UH", "TH"],
'lash': ["L", "AA", "SH"],
'alatho': ["AA", "L", "AA", "TH", "UH"],
'ulatho': ["UW", "L", "AA", "TH", "UH"],
'tho': ["TH", "UW"],
'sek': ["S", "EH", "K"],
'thok': ["TH", "UW", "K"],
'fek': ["F", "EH", "K"],
'ses': ["S", "EH", "S"],
'hahsh': ["H", "AA", "SH"],
'eyik': ["EH", "Y", "IY", "K"],
'zomfa': ["Z", "UH", "M", "F", "AH"],
'domosh': ["D", "UH", "M", "UH", "SH"],
'arkosh': ["AA", "R", "K", "UH", "SH"],
'voth': ["V", "UH", "TH"],
'hedoq': ["H", "EH", "D", "UH", "K"],
'nith': ["N", "IY", "TH"],
'gluth': ["G", "L", "UH", "TH"],
'omoz': ["UH", "M", "UH", "S"],
'nesh': ["N", "EH", "SH"],
'safras': ["S", "AA", "F", "R", "AA", "S"],
'poz': ["P", "UH", "Z"],
'irush': ["IY", "R", "UW", "SH"],
'groth': ["G", "R", "UH", "TH"],
'greesh': ["G", "R", "IY", "SH"],
'lieyev': ["L", "IY", "EH", "EH", "V"],
'chron': ["K", "R", "UH", "N"],
'rast': ["R", "AA", "S", "T"],
'miskath': ["M", "IH", "S", "K", "AA", "TH"],
'fol': ["F", "AO", "L"],
'ensh': ["EH", "N", "SH"],
'ov': ["AO", "V"],
'sav': ["S", "AA", "V"],
'sol': ["S", "AO", "L"],
'sovoz': ["S", "AO", "V", "AO", "S"],
'kish': ["K", "IY", "SH"],
'ac': ["AA", "K"],
'ach': ["AA", "K", "H"],
'ah': ["AA", "H"],
'ahm': ["AA", "H", "M"],
'al': ["AA", "L"],
'ar': ["AA", "R"],
'as': ["AA", "S"],
'ash': ["AA", "SH"],
'ath': ["AA", "TH"],
'atho': ["AA", "TH", "UH"],
'ch': ["CH"],
'cha': ["CH", "AA"],
'do': ["D", "UH"],
'dom': ["D", "UH", "M"],
'ek': ["EH", "K"],
'en': ["EH", "N"],
'ey': ["EH", "Y"],
'fa': ["F", "AA"],
'fe': ["F", "EH"],
'fek': ["F", "EH", "K"],
'fi': ["F", "IY"],
'fo': ["F", "AO"],
'gl': ["G", "L"],
'glu': ["G", "L", "UH"],
'gr': ["G", "R"],
'gro': ["G", "R", "OH"],
'ha': ["H", "AA"],
'hag': ["H", "AA", "G"],
'has': ["H", "AA", "SH"],
'he': ["H", "EH"],
'hm': ["H", "M"],
'ho': ["H", "UH"],
'hol': ["H", "UH", "L"],
'hro': ["H", "R", "UH"],
'ich': ["IH", "SH"],
'ik': ["IH", "K"],
'iru': ["IH", "R", "UH"],
'is': ["IH", "SH"],
'isk': ["IH", "SH", "K"],
'iz': ["IH", "Z"],
'izh': ["IH", "ZH"],
'ka': ["K", "AA", "H"],
'kala': ["K", "AA", "L", "AA"],
'kath': ["K", "AA", "TH"],
'ko': ["K", "UH"],
'lo': ["L", "UH"],
'lof': ["L", "UH", "F"],
'lom': ["L", "UH", "M"],
'mi': ["M", "IY"],
'mis': ["M", "IY", "S"],
'mo': ["M", "UH"],
'moz': ["M", "UH", "ZH"],
'ne': ["N", "EH"],
'ni': ["N", "IY"],
'ns': ["N", "SH"],
'of': ["UH", "F"],
'ok': ["UH", "K"],
'ol': ["UH", "L"],
'om': ["UH", "M"],
'omf': ["UH", "M", "F"],
'omo': ["UH", "M", "UH"],
'oq': ["UH", "K"],
'osh': ["UH", "SH"],
'oth': ["UH", "TH"],
'ov': ["UH", "V"],
'oz': ["UH", "Z"],
'ozh': ["UH", "ZH"],
'po': ["P", "AO"],
'pr': ["P", "R"],
'pz': ["P", "ZH"],
'ro': ["R", "AO"],
'ros': ["R", "AO", "SH"],
'rush': ["R", "UH", "SH"],
'se': ["S", "EH"],
'sek': ["S", "EH", "K"],
'sh': ["SH"],
'shk': ["SH", "K"],
'so': ["S", "AO"],
'sof': ["S", "AO", "F"],
'sol': ["S", "AO", "L"],
'sov': ["S", "AO", "V"],
'ta': ["T", "AH"],
'tak': ["T", "AH", "K"],
'th': ["TH"],
'tho': ["TH", "AO"],
'uch': ["UH", "CH", "SH"],
'ucha': ["UH", "CH", "AA"],
'uth': ["UH", "TH"],
'vo': ["V", "AO"],
'vot': ["VO", "AO", "T"],
'voth': ["VO", "AO", "TH"],
'vr': ["V", "R"],
'vro': ["V", "R", "AO"],
'wr': ["W", "R"],
'yi': ["Y", "IY"],
'zh': ["ZH"]
}

# from future import nicht uniforme zufallsvariable hier
####################################################
#    (alphabet:oz_sylls) : rand pick probability   #
####################################################
weight_mapping = {
    "a": [1, 2, 1, 2, 2, 2, 2, 3, 2, 2], # 9
    "c": [1, 2],
    "d": [1, 2],
    "e": [2, 3, 2],
    "f": [1, 2, 2, 3, 2],
    "g": [3, 2, 2, 2],
    "h": [1, 2, 2, 2, 2, 1, 2, 2], # 8
    "i": [2, 3, 3, 2, 2, 3, 2],
    "k": [1, 2, 2, 1],
    "l": [1, 2, 2],
    "m": [1, 1, 1, 2],
    "n": [2, 2, 1],
    "o": [2, 2, 3, 3, 2, 2, 2, 1, 2, 3, 3, 2], # 12
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
####################################################
#  letters don't appear in the wiki translations   #
####################################################
forbidden_letters = {'b': 'q', 'j': 'o', 'x': 'o'}
####################################################
#  check available audio files                     #
####################################################
audio_dir = "audio_input"
oz_available_audio = []
oz_sample_file = "./oz_audiolist.csv"
with open(oz_sample_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
        oz_available_audio.append(','.join(row))

# init vars

word_temp_id = 0
sentence_index = 0
# do this in order to not overwrite previously created sentence audio
path, dirs, files = next(os.walk("./training_audio"))
wav_count = len(files)
print(wav_count, "is number of files")
wav_export_id = wav_count
oz_sentence = []
kaldi_lexicon = {}
# init audio vars
# combined_word_audio = AudioSegment.empty()
combined_audio = AudioSegment.empty()

# load dataframes
df1 = pd.read_pickle('df_translation.pkl')
df2 = pd.read_pickle('df_training_kaldi.pkl')
df3 = pd.read_pickle('df_training_taco.pkl')
df4 = pd.read_pickle('df_lexicon_kaldi.pkl')
f = open('test.txt', 'r')
poem = f.readlines()

for lines in poem:
    lines = lines.lower()
    sentence = lines.split()
    # print(sentence)
    for en_word in sentence:
        en_word = [character for character in str.lower(en_word) if character.isalnum()]
        en_word = "".join(en_word)
        # if translation dataframe column english already contains an exact equal match of the word
        if df1['english'].eq(en_word).any():
            # get the stored syllables
            entry = df1.loc[df1['english'] == en_word]
            oz_word = entry.iloc[0].iloc[1]
            oz_sentence.append(oz_word)
            recombine_sylls = entry.iloc[0].iloc[2]
            # make sure audio file is there, append syllable segments and export the word
            audio_pathlist = []
            phonemes = []
            for i in recombine_sylls:
                audiostring = str(i)
                # print(audiostring, "is audio string")
                audio_filepath = './audio/' + audiostring + '.wav'
                audio_pathlist.append(audio_filepath)
                # print("searching for audio", audiostring, "in path", audio_filepath)
                oz_phoneme_pick = str(oz_phoneme_mapping.get(i))
                phonemes.append(oz_phoneme_pick)

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
            # make sure audio segment is empty for next word
            combined_audio = AudioSegment.empty()

            phonemes = str(phonemes).replace('[', '').replace(']', '').replace("'", '').replace('"', '').replace(',', '')
            print(phonemes)

            # update the lexicon dataframe if the word is not already known
            if not df4['oz_word'].eq(oz_word).any():
                df4.loc[len(df4.index)] = [oz_word, phonemes]

        else:
            # print(en_word, " - no translation found in dataframe")
            en_hyphens = hyphenate_word(en_word)
            trl_word = en_word
            trl_hyphens = en_hyphens
            temp_hyphens = []
            for hyphen in en_hyphens:
                for key in forbidden_letters.keys():
                    hyphen = hyphen.replace(key, forbidden_letters[key])
                temp_hyphens.append(hyphen)
            for key in forbidden_letters.keys():
                trl_word = trl_word.replace(key, forbidden_letters[key])
            # print(trl_word)
            hyphens = temp_hyphens
            if len(en_hyphens) == 1:
                word_len = len(str(en_word))
                hyphens_len = math.sqrt(len(trl_word))
                hyphens_rounded = int(hyphens_len)
                if hyphens_rounded == 0:
                    hyphens_rounded += 1
                hyphens = [trl_word[i:i + hyphens_rounded] for i in
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
            phonemes = []
            for chars in start_chars:
                char_map = oz_syllable_mapping.get(chars)
                weights_map = weight_mapping.get(chars)
                oz_syllable_pick = str(random.choices(population=char_map, weights=weights_map, k=1))
                # create clean string for syllable list
                oz_syllable_pick = str(re.sub(r'\W+', '', oz_syllable_pick))
                oz_syllables.append(oz_syllable_pick)
                oz_phonemes_pick = str(oz_phoneme_mapping.get(oz_syllable_pick))
                # oz_phonemes_pick = str(re.sub(r'\W+', '', oz_phonemes_pick))
                phonemes.append(oz_phonemes_pick)
                # create clean string to look for audio
                audio_name = str(re.sub(r'\W+', '', oz_syllable_pick))
                audio_filepath = './audio/' + audio_name + '.wav'
                # print("searching for audio name", audio_name, "in path", audio_filepath)
                audio_pathlist.append(audio_filepath)

            oz_word = str(oz_syllables)
            oz_word = [character for character in oz_word if character.isalnum()]
            oz_word = "".join(oz_word)
            oz_sentence.append(oz_word)
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
                    print("Sample", audio_name, "not found in translation loop")
            
            # update the translation dataframe
            df1.loc[len(df1.index)] = [en_word, oz_word, oz_syllables]
            # update the lexicon dataframe
            phonemes = str(phonemes).replace('[', '').replace(']', '').replace("'", '').replace('"', '').replace(',', '')
            print(phonemes)
            df4.loc[len(df4.index)] = [oz_word, phonemes]
            export_word()
            audio_pathlist = []
            combined_audio = AudioSegment.empty()
            oz_syllables = []
            phonemes = []
            # end translation loop
    # print("Exporting sentence audio to disk ...")
    combine_sentence()
    wav_export_id += 1
    wav_exp_id = str(wav_export_id)
    wav_exp_id = wav_exp_id.zfill(5)
    transcription = lines
    transcription = transcription.rstrip('\n')

    separator = ', '
    oz_sentence = separator.join(oz_sentence)
    oz_transcription = str(oz_sentence)
    oz_transcription = oz_transcription.replace(',', '')
    norm_oz_transcription = oz_transcription
    norm_transcription = lines
    norm_transcription = norm_transcription.rstrip('\n')
    newaudio = full_sentence_audio.set_frame_rate(48000)

    octaves = +0.666

    new_sample_rate = int(newaudio.frame_rate * (1.5 ** octaves))

    highpitch_sound = newaudio._spawn(newaudio.raw_data, overrides={'frame_rate': new_sample_rate})
    newaudio = full_sentence_audio.set_frame_rate(11025)
    highpitch_sound.export("./training_audio/" + "LJ001-" + wav_exp_id + ".wav", format="wav")
    taco_training_wav_path = "LJ001-" + wav_exp_id
    kaldi_file_id = wav_exp_id
    kaldi_wav_path = "./training_audio/" + wav_exp_id + ".wav"
    kaldi_speaker_id = 1
    kaldi_utt_id = wav_exp_id
    kaldi_utt_segment_start = 0
    kaldi_utt_segment_end = 1
    kaldi_segment_times = [kaldi_utt_segment_start, kaldi_utt_segment_end]
    delete_tempwords()
    word_temp_id = 0
    sentence_index = 0
    oz_sentence = []
    # update kaldi training df
    df2.loc[len(df2.index)] = [kaldi_file_id, kaldi_wav_path, kaldi_speaker_id, kaldi_utt_id, kaldi_segment_times, oz_transcription]
    # update taco training df
    df3.loc[len(df3.index)] = [taco_training_wav_path, oz_transcription, norm_oz_transcription]

print(df4)
# save the dataframes
df1.to_pickle('df_translation.pkl')
df2.to_pickle('df_training_kaldi.pkl')
df3.to_pickle('df_training_taco.pkl')
df4.to_pickle('df_lexicon_kaldi.pkl')
# replace (overwrite) csv
compression_opts = dict(method='infer', archive_name='metadata.csv')
df3.to_csv(r'metadata.csv', sep='|', index=False, compression=compression_opts)

# combine_all_sentences()

# torch_export = torch_training_audio.set_frame_rate(11025)
# torch_export.export("./training_audio/" + "torch" + ".wav", format="wav")
