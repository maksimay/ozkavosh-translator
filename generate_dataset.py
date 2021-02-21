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
    for filename in glob.glob('./audio/audio_input/' + audio_name + '.wav'):
        # print('FILENAME IS' + filename)
        rdm_audiopick_list.append(filename)
    for filename in glob.glob('./audio/audio_input/' + audio_name + '[0-9]' + '.wav'):
        rdm_audiopick_list.append(filename)
        # print('FILENAME IS' + filename)
        # print(rdm_audiopick_list)
    randompick = str(random.choices(rdm_audiopick_list)).replace('[', '').replace(']', '').replace("'", '')
    # print(randompick, "is random pick!")


def combine_syllables():
    global combined_audio
    src_audio = AudioSegment.from_wav(randompick)
    src_audio = match_target_amplitude(src_audio, -30.0)
    octaves = random.uniform(0, 0.123)
    newaudio = src_audio
    new_sample_rate = int(newaudio.frame_rate * (1.5 ** octaves))
    highpitch_sound = newaudio._spawn(newaudio.raw_data, overrides={'frame_rate': new_sample_rate})
    src_audio = highpitch_sound

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
    if not os.path.exists('./audio/TEMP'):
        os.makedirs('./audio/TEMP')
    word_temp_id += 1
    temp_id = str(word_temp_id)
    temp_id = temp_id.zfill(3)
    sentence_index += 1
    str_sentence_index = str(sentence_index)
    str_sentence_index = str_sentence_index.zfill(3)
    # print("Word", str_sentence_index, "exported")
    combined_audio.export("./audio/TEMP/" + str(str_sentence_index) + str(oz_word) + str(temp_id) + ".wav", format="wav")


def combine_sentence():
    global word_audio
    global full_sentence_audio
    global silence_duration
    full_sentence_audio = AudioSegment.empty()
    silence_duration = random.randrange(123, 321)
    silence = AudioSegment.silent(duration=silence_duration)
    for filename in glob.glob('./audio/TEMP/'+'*.wav'):
        word_audio = AudioSegment.from_wav(filename)
        word_audio = match_target_amplitude(word_audio, -20.0)
        full_sentence_audio += word_audio + silence
    full_sentence_audio = silence + full_sentence_audio


def combine_all_sentences():
    global sentence_audio
    global torch_training_audio
    torch_training_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=999)
    for filename in glob.glob('./audio/audio_output/'+'*.wav'):
        sentence_audio = AudioSegment.from_wav(filename)
        torch_training_audio += sentence_audio + silence


def delete_tempwords():
    for files in glob.glob('./audio/TEMP/'+'*.wav'):
        os.remove(files)


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


if not os.path.exists('./kaldi/data/local/lang/'):
    os.makedirs('./kaldi/data/local/lang/')

if not os.path.exists('./taco'):
    os.makedirs('./taco')

if not os.path.exists('./dataframes'):
    os.makedirs('./dataframes')


if not os.path.exists('./audio/audio_output'):
    os.makedirs('./audio/audio_output')


# load dataframes
df1 = pd.read_pickle('./dataframes/df_translation.pkl')
df2 = pd.read_pickle('./dataframes/df_training_kaldi.pkl')
df3 = pd.read_pickle('./dataframes/df_training_taco.pkl')
df4 = pd.read_pickle('./dataframes/df_lexicon_kaldi.pkl')
df5 = pd.read_pickle('./dataframes/nonsilence_phones.pkl')

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
    'sav': ["S", "AA", "V"],
    'sovoz': ["S", "AO", "V", "AO", "S"],
    'kish': ["K", "IY", "SH"],
    'ac': ["AA", "K"],
    'ach': ["AA", "K", "H"],
    'ah': ["AA", "H"],
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
    'sh': ["SH"],
    'shk': ["SH", "K"],
    'so': ["S", "AO"],
    'sof': ["S", "AO", "F"],
    'sol': ["S", "AO", "L"],
    'sov': ["S", "AO", "V"],
    'ta': ["T", "AH"],
    'tak': ["T", "AH", "K"],
    'th': ["TH"],
    'uch': ["UH", "CH", "SH"],
    'ul': ["UH", "L"],
    'uth': ["UH", "TH"],
    'vot': ["VO", "AO", "T"],
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
audio_dir = "./audio/audio_input"
oz_available_audio = []
oz_sample_file = "./audio/oz_audiolist.csv"
with open(oz_sample_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
        oz_available_audio.append(','.join(row))

# init vars and create folders

kaldi_lexicon = {}
word_temp_id = 0
sentence_index = 0
# do this in order to not overwrite previously created sentence audio
path, dirs, files = next(os.walk("./audio/audio_output"))
wav_count = len(files)
print(wav_count, "is number of files")
wav_export_id = wav_count
oz_sentence = []

# init audio vars
# combined_word_audio = AudioSegment.empty()
combined_audio = AudioSegment.empty()


f = open('input_text.txt', 'r')
input_text = f.readlines()
for lines in input_text:
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
            df4.loc[len(df4.index)] = [oz_word, phonemes]
            export_word()
            audio_pathlist = []
            combined_audio = AudioSegment.empty()
            oz_syllables = []
            phonemes = []
            # end translation loop
    # print("Exporting sentence audio to disk soon...")
    combine_sentence()
    word_temp_id = 0
    sentence_index = 0
    # update counters and create clean sentence transcription for kaldi

    speaker_id = 1
    speaker_id = str(speaker_id)
    speaker_id = speaker_id.zfill(3)

    wav_export_id += 1
    wav_exp_id = str(wav_export_id)
    wav_exp_id = wav_exp_id.zfill(5)

    transcription = lines
    transcription = transcription.rstrip('\n')

    separator = ', '
    oz_sentence = separator.join(oz_sentence)
    oz_transcription = str(oz_sentence)
    oz_transcription = oz_transcription.replace(',', '')

    oz_sentence = []
    delete_tempwords()

    norm_oz_transcription = oz_transcription

    norm_transcription = lines
    norm_transcription = norm_transcription.rstrip('\n')

    taco_training_wav_path = "LJ001-" + wav_exp_id

    file_id = wav_exp_id
    wav_path = "./audio/audio_output/" + speaker_id + '_' + file_id + ".wav"
    utt_id = speaker_id + '_' + file_id
    utt_segment_start = silence_duration / 1000
    utt_segment_end = (len(full_sentence_audio) - silence_duration) / 1000


    # random audio pitch then export

    newaudio = full_sentence_audio.set_frame_rate(48000)
    octaves = random.uniform(0.322, 0.666)
    new_sample_rate = int(newaudio.frame_rate * (1.5 ** octaves))
    highpitch_sentence = newaudio._spawn(newaudio.raw_data, overrides={'frame_rate': new_sample_rate})
    highpitch_sentence = highpitch_sentence.set_frame_rate(22050)
    highpitch_sentence.export("./audio/audio_output/" + utt_id + ".wav", format="wav")

    # update kaldi training df
    df2.loc[len(df2.index)] = [file_id, wav_path, speaker_id, utt_id, utt_segment_start, utt_segment_end, oz_transcription]
    # update taco training df
    df3.loc[len(df3.index)] = [wav_path, oz_transcription, norm_oz_transcription]

# print(df4)
# save the dataframes
df1.to_pickle('./dataframes/df_translation.pkl')
df2.to_pickle('./dataframes/df_training_kaldi.pkl')
df3.to_pickle('./dataframes/df_training_taco.pkl')
df4.to_pickle('./dataframes/df_lexicon_kaldi.pkl')
# metadata.csv
compression_opts = dict(method='infer', archive_name='metadata.csv')
df3.to_csv(r'./taco/metadata_unclean.csv', sep='|', index=False, compression=compression_opts)

with open("./taco/metadata_unclean.csv", 'r') as f:
    with open("./taco/metadata.csv", 'w') as f1:
        next(f)
        for line in f:
            f1.write(line)
if os.path.exists("./taco/metadata_unclean.csv"):
    os.remove("./taco/metadata_unclean.csv")


# text.txt # right now blank line at end of file
np.savetxt(r'./kaldi/text.txt', df2[['utt_id', 'transcription']].values, fmt='%s')

# utt2spk # right now blank line at end of file
np.savetxt(r'./kaldi/utt2spk.txt', df2[['utt_id', 'speaker_id']].values, fmt='%s')

# spk2utt
# to do later:
# make dictionary
# iterate over items in df
# count amount of unique speaker_ids
# check if speaker_id is in last 3 characters of utt_id
# if it is, map that utt_id to the corresponding speaker id key in dict
# write dict to file
# but for now do this junk:
utt_ids = []
for column in df2[['utt_id']]:
    columnSeriesObj = df2[column]
    utt_ids.append(str(columnSeriesObj.values))
utt_ids = str(utt_ids).replace('[', '').replace(']', '').replace("'", '').replace('"', '')

f = open('./kaldi/spk2utt.txt', 'w')
L = "001 " + utt_ids
f.writelines(L)

f = open('./kaldi/spk2utt.txt', 'r')
line = f.readlines()
line = str(line).replace('\\n', '').replace("['", '').replace("']", '').replace('\\', '')

f = open('./kaldi/spk2utt.txt', 'w')
f.writelines(line)

# wav.scp
np.savetxt(r'./kaldi/wav.scp', df2[['file_id', 'wav_path']].values, fmt='%s')

# segments.txt utt_id file_id start_time end_time
np.savetxt(r'./kaldi/segments.txt', df2[['utt_id', 'file_id', 'utt_seg_start', 'utt_seg_end']].values, fmt='%s')

# silence_phones.txt
f = open('./kaldi/data/local/lang/silence_phones.txt', 'w')
L = ["SIL\n", "oov"]
f.writelines(L)

# nonsilence_phones.txt
nonsilence_phones = []
for key, value in oz_phoneme_mapping.items():
    for i in value:
        nonsilence_phones.append(i)
nonsilence_phones = np.unique(nonsilence_phones)
for i in nonsilence_phones:
    df5.loc[len(df5.index)] = [i]
np.savetxt(r'./kaldi/data/local/lang/nonsilence_phones.txt', df5['nonsilence_phones'].values, fmt='%s')

# optional_silence.txt
f = open('./kaldi/data/local/lang/optional_silence.txt', 'w')
L = ["SIL"]
f.writelines(L)

# lexicon.txt # right now blank line at end of file
np.savetxt(r'./kaldi/data/local/lang/lexicon.txt', df4[['oz_word', 'phonemes']].values, fmt='%s')


print(df2)

















####################################################################################
# T O R C H R N N / \ / \ / \ / \ U N U S E D / \ / \ / \ / \ / \ / \ / \ / \ / \ / \
######################################################################################
# combine_all_sentences()
# torch_export = torch_training_audio.set_frame_rate(11025)
# torch_export.export("./audio/audio_output/" + "torch" + ".wav", format="wav")
####################################################################################
