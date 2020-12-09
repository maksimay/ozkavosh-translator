import csv
import random
import math
from random import choice
from hyphenate import hyphenate_word
import re
from pydub import AudioSegment
from pydub.playback import play
import os


FILEPATH_ENG = "./commonwords.txt"
FILEPATH_OZK = "./DemonWords.txt"
FILEPATH_TRL = "./EnglishWords.txt"
# direct translations from dotawiki (INCOMPLETE)
englist = [i.strip().split() for i in open(FILEPATH_TRL).readlines()]
ozklist = [i.strip().split() for i in open(FILEPATH_OZK).readlines()]
#3000 most common english words (INCOMPLETE, UNTAGGED)
BigList = [i.strip().split() for i in open(FILEPATH_ENG).readlines()]
#get random word from list
sequence = [i for i in range(len(BigList))]
for words in range(len(BigList)):
    selection = choice(sequence)
    Current_Word = str(BigList[selection])
    Current_Word = str.lower(Current_Word)
    Current_Word = [character for character in Current_Word if character.isalnum()]
    Current_Word = "".join(Current_Word) 
print("en word is",Current_Word)

########## HYPHENATION #############
hyphens = hyphenate_word(Current_Word)
#hyphens = Current_Word
print(hyphens)
####################################

### FORBIDDEN LETTERS ####
forbiddenletters = {'b':'q','j':'ia','x':'ks'}

for key in forbiddenletters.keys():
    Current_Word = Current_Word.replace(key, forbiddenletters[key])
#############

####### REPLACEMENT ##########

#number of characters in each syllable
#start character for each syllable
char_amt = []
start_chars = []
iterations = len(hyphens)
for i in range(iterations):
    char_amt.append(len(hyphens[i])) 
    start_chars.append(hyphens[i][:1])
    

dict_charpairs = {'a':["as","ath","ah","al","ar","af"],'c':["ch"],'d':["do"],'e':["es","ek"],'f':["fe","fa","fr","fo"],'g':["gr","gl"],'h':["ha","ho","hm"],'i':["iz","ir","it","ik","ish","isk"],'k':["ka","ko","ki"],'l':["la","lo","li","lu"],'m':["mo","mi"],'n':["ne","ni","ns"],'o':["om","oz","ot","osh"],'p':["po","pr","pz"],'q':["qo"],'r':["ro","ra","re","rk"],'s':["sas","ath","sah","sal","sar","saf"],'t':["th","tho","ta"],'u':["uch","ul","ush","uth"],'v':["vo","vu"],'w':["wr"],'y':["ye","yi"],'z':["zh","zk","zo"]}
weights_dict = {"a":[0.35,0.25,0.1,0.1,0.1,0.1],"c":[1],"d":[1],"e":[0.5,0.5],"f":[0.25,0.25,0.25,0.25],"g":[0.5,0.5],"h":[0.45,0.45,0.1],"i":[0.3,0.125,0.125,0.125,0.125,0.12],"k":[0.5,0.25,0.25],"l":[0.6,0.15,0.15,0.1],"m":[0.66,0.34],"n":[0.35,0.34,0.32],"o":[0.4,0.3,0.15,0.15],"p":[0.5,0.2,0.3],"q":[1],"r":[0.5,0.25,0.125,0.125],"s":[0.4,0.3,0.15,0.04,0.04,0.045],"t":[0.7,0.26,0.04],"u":[0.25,0.25,0.25,0.25],"v":[0.8,0.2],"w":[1],"y":[0.5,0.5],"z":[0.6,0.2,0.2]} 
oz_sample_file = 'oz_audiolist.csv'
oz_audiolist = []

with open(oz_sample_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
      oz_audiolist.append(','.join(row))



#weighted random pick to replace syllable depending on english start character
ozwordlist = []
pathlist = []
audionamelist = []
for i in start_chars:
    character_mapping = dict_charpairs.get(i)
    weightlist_mapping = weights_dict.get(i)
    result = str(random.choices(population=character_mapping,weights= weightlist_mapping,k=1))
    ozwordlist.append(result)
    audioname = str(re.sub(r'\W+', '', result))
    audio_filepath = "./audio/"+audioname+".wav"
    print( "searching for oz_audio in", audio_filepath)
    pathlist.append(audio_filepath)



###### REPLACEMENT END #############

ozwordlist = str(ozwordlist)
ozword = [character for character in ozwordlist if character.isalnum()]
ozword = "".join(ozword)
print("oz word is", ozword)


### REMOVING SILENCE FUNCTION####

def detect_silence(sound, silence_threshold=-50.0, chunk_size=10):

    #silence_threshold in dB
    #chunk_size in ms
    #iterate over chunks until you find the first one with sound
    trim_ms = 0 
    # to avoid infinite loop
    assert chunk_size > 0 
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

########## AUDIO TRIMMING / APPENDING ##########

audioisvalid = False
combined_audio = AudioSegment.empty()

for i in pathlist:
    wav_filepath = i
    print(i)
    audioname = wav_filepath.replace('.wav','').replace('./audio/','')
    print(audioname)
    if audioname in oz_audiolist:
        print("Samples found! Creating combined Audiosnippet...")
        audioisvalid = True
        src_audio = AudioSegment.from_wav(wav_filepath)
        print("Trimming Audiofiles..")
        duration = len(src_audio)    
        start_trim = detect_silence(src_audio)
        end_trim = detect_silence(src_audio.reverse())
        trimmed_audio = src_audio[start_trim:duration-end_trim]
        combined_audio += trimmed_audio
        #combined_audio += src_audio
    else:
        audioisvalid = False
        print("Couldn't find Samples for syllables")

### Make Directory for Combined audios if it doesnt exist yet###
if not os.path.exists('./combined'):
    os.makedirs('./combined')

#### FINAL EXPORT ####
if audioisvalid == True:
    print("Exporting audio to disk ...")
    combined_audio.export( "./combined/_" + ozword + "_" + Current_Word + "_combined.wav", format="wav")
    print("Exported succesfully!")



