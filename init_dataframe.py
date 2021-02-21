import numpy as np
import pandas as pd
from nltk.corpus import wordnet


def get_synonym_key(val):
    for k, v in DictWikiSyns.items():
        if val in v:
            return k
    return "key doesn't exist"


def get_synonyms_wordnet():
    global templist
    templist = []
    for key, value in DictWikiSyns.items():                                     # for each key value pair item:
        for i in value:                                                         # for each value:
            # print(i)
            for syn in wordnet.synsets(i):                                      # for each synonyms in wordnet:
                for k in syn.lemmas():                                          # for each lemma (synonym list word element):
                    templist.append(k.name())                                   # stash the synonym into a temp list!

        templist = np.unique(templist).tolist()                                 # remove duplicates from templist!
        for i in templist:                                                      # for each element in the stashed synonym list:
            # print(templist, "i")                                              # for each word in list, print the list (lul)
            i = [character for character in str.lower(i) if character.isalnum()]
            i = "".join(i)
            value.append(i)                                                     # append each temp element to value list in the dict!


# init translation dataframe from wiki direct translations and synonyms
DictWikiSyns = {
                "ozh": ["Self", "I", "me", "my", "mine"],
                "izh": ["you", "him", "her"],
                "izhai": ["group", "they", "them"],
                "ozkavosh": ["demon", "demons", "spirit", "spirits"],
                "sa": ["this", "concept"],
                "vu": ["that", "the"],
                "doq": ["upon", "ontop", "above", "ground"],
                "roq": ["far", "distant", "remote", "reach"],
                "doz": ["below", "beneath", "underneath", "burrowed"],
                "ahm": ["very", "super"],
                "ashm": ["more", "additional", "much"],
                "vo": ["not", "negative", "exclude"],
                "vom": ["less", "fewer", "deplete", "exhaust"],
                "acha": ["am", "be", "now", "is"],
                "icha": ["could", "will", "possibility", "maybe"],
                "ucha": ["was", "existed"],
                "hollom": ["without", "nothing", "hollow"],
                "tak": ["take", "have", "own", "grab"],
                "wroth": ["again", "repeated", "iterative"],
                "lash": ["part", "segment", "share"],
                "alatho": ["forward", "ahead"],
                "ulatho": ["Back", "backwards"],
                "tho": ["at", "local", "position"],
                "sek": ["introspection", "meditate", "meditation"],
                "thok": ["move", "go", "walk", "run", "teleport"],
                "fek": ["stop", "cease", "die", "halt"],
                "ses": ["hide", "unseen", "concealed", "smoked"],
                "hahsh": ["feel", "touch", "sense"],
                "eyik": ["look", "view", "see", "witness", "behold"],
                "zomfa": ["leisure", "happiness", "happy", "glad", ],
                "domosh": ["reign", "domination", "dominion", "kingship"],
                "arkosh": ["master", "king"],
                "voth": ["war", "battle", "fight", "slaughter"],
                "hedoq": ["desirable", "delicious", "wanted", "objective"],
                "nith": ["land", "earth", "ground", "kingdom"],
                "gluth": ["eat", "devour", "consume"],
                "omoz": ["darkness", "abyss", "blackness", "hell"],
                "nesh": ["home", "sanctuary", "safety"],
                "safras": ["pain", "suffer", "wound"],
                "poz": ["power", "ability", "skill", "action", "spell", "ultimate"],
                "irush": ["Illness", "common cold", "plague"],
                "groth": ["spread", "widen", "open", "welcome"],
                "greesh": ["debt", "lack", "need"],
                "lieyev": ["payment", "gift", "tithe", "taxes", "tax"],
                "chron": ["time", "duration", "period"],
                "rast": ["toys", "puppets", "amusement", "entertainment"],
                "miskath": ["failure", "incomplete", "unfinished"],
                "fol": ["weakling", "whelp", "peasant", "fool", "greg", "fools"],
                "ensh": ["know", "learn"],
                "ov": ["one", "once", "singular"],
                "sav": ["seven", "seventh"],
                "kish": ["excrement", "waste"],
                "sol": ["hope", "light", "brightness", "sun", "fire"],
                "sovoz": ["sandwich", "snack"],
                }
DictWikiSylls = {
            "ozh": ["ozh"],
            "izh": ["izh"],
            "izhai": ["izhai"],
            "ozkavosh": ["ozh", "ka", "vo", "sh"],
            "sa": ["sa"],
            "vu": ["vu"],
            "doq": ["doq"],
            "roq": ["roq"],
            "doz": ["doz"],
            "ahm": ["ahm"],
            "ashm": ["ash", "hm"],
            "vo": ["vo"],
            "vom": ["vom"],
            "acha": ["ach", "ah"],
            "icha": ["ich", "ah"],
            "ucha": ["uch", "ah"],
            "hollom": ["hol", "lom"],
            "tak": ["tak"],
            "wroth": ["wr", "oth"],
            "lash": ["lash"],
            "alatho": ["al", "ah", "tho"],
            "ulatho": ["ul", "ah", "tho"],
            "tho": ["tho"],
            "sek": ["sek"],
            "thok": ["tho", "ok"],
            "fek": ["fe", "ek"],
            "ses": ["ses"],
            "hahsh": ["ha", "sh"],
            "eyik": ["ey", "ik"],
            "zomfa": ["zom", "fa"],
            "domosh": ["dom", "osh"],
            "arkosh": ["ar", "ko", "sh"],
            "voth": ["vo", "th"],
            "hedoq": ["he", "doq"],
            "nith": ["ni", "th"],
            "gluth": ["gl", "uth"],
            "omoz": ["om", "oz"],
            "nesh": ["ne", "sh"],
            "safras": ["safras"],
            "poz": ["po", "oz"],
            "irush": ["iru", "sh"],
            "groth": ["gr", "oth"],
            "greesh": ["greesh"],
            "lieyev": ["lieyev"],
            "chron": ["chron"],
            "rast": ["rast"],
            "miskath": ["mi", "is", "kath"],
            "fol": ["fol"],
            "ensh": ["en", "sh"],
            "ov": ["ov"],
            "sav": ["sav"],
            "kish": ["kish"],
            "sol": ["sol"],
            "sovoz": ["so", "vo", "oz"]
            }
Translation_Dictionary = {}
get_synonyms_wordnet()

for key, value in DictWikiSyns.items():
    for i in value:
        Translation_Dictionary.update({i: get_synonym_key(i)})

df = pd.DataFrame(list(Translation_Dictionary.items()), columns=['english', 'ozkavosh'], dtype='object')
df['syllables'] = ""

for i in range(len(df)):
    syllkey = df.iloc[i, 1]
    syllval = DictWikiSylls[syllkey]

    df.iat[i, 2] = syllval
    # print(syllval)
print(df)

df.to_pickle('./dataframes/df_translation.pkl')

# create an !empty! training dataframe with KALDI training formatting
# use data in this to:
# create text file containing utterance transcriptions              -> utt_id WORD1 WORD2 WORD3
# create a lexicon                                                  -> {word:[phonemes]}
# create a segments file containing                                 -> utt_id file_id start_time end_time
# create wav.scp file containing                                    -> file_id wav_path
# create utt2spk file containing map of utterance to speaker        -> utt_id spkr
# create spk2utt file containing map of speaker to utterance        -> spkr utt_id1 utt_id2 utt_id3


# already available data: transcription, file_id, wav_path, syllables
# wav file length generates utt_seg_start_end?
# wav_path generates utt_id
# speaker id is either always the same or a lot of stuff needs changing =)

# lexicon: generates from translation df + syll:phoneme dict

df2 = pd.DataFrame({'file_id': pd.Series([], dtype='object'),
                    'kaldi_wav_path': pd.Series([], dtype='object'),
                    'speaker_id': pd.Series([], dtype='object'),
                    'utt_id': pd.Series([], dtype='object'),
                    'utt_seg_start': pd.Series([], dtype='object'),
                    'utt_seg_end': pd.Series([], dtype='object'),
                    'transcription': pd.Series([], dtype='object'),
                    })


df2.to_pickle('./dataframes/df_training_kaldi.pkl')

# create an !empty! training dataframe with tacotron training formatting
df3 = pd.DataFrame({'wav_path': pd.Series([], dtype='object'),
                    'oz_transcription': pd.Series([], dtype='object'),
                    'oz_normalized_transcription': pd.Series([], dtype='object')
                    })

df3.to_pickle('./dataframes/df_training_taco.pkl')

df4 = pd.DataFrame({'oz_word': pd.Series([], dtype='object'),
                    'phonemes': pd.Series([], dtype='object'),
                    })

df4.to_pickle('./dataframes/df_lexicon_kaldi.pkl')

df5 = pd.DataFrame({'nonsilence_phones': pd.Series([], dtype='object')
                    })

df5.to_pickle('./dataframes/nonsilence_phones.pkl')
