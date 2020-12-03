import random, os

import csv

import speech_recognition as sr 

print("Translator initializing...")

d_file = 'DemonWords.csv'
e_file = 'EnglishWords.csv'

demon = []
eng = []
alatho = "alatho.mp3"
ozkavosh = "ozkavosh.mp3"

#whats up git

#List to Tuple Function
def convert(list): 
    return tuple(list)

# Take row out of csv file and append to list 
with open(d_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
      demon.append(','.join(row))


with open(e_file) as csvfile:
    dictionary = csv.reader(csvfile, delimiter=' ')
    for row in dictionary:
      eng.append(','.join(row))

#Draw random samples
#a = (random.sample(demon, 1))
#b = (random.sample(demon, 1))   

#Convert the List to Tuples and combine it  
demon_tuple = convert(demon)
eng_tuple = convert(eng)
zipObj = zip(eng_tuple,demon_tuple)

##Make our Dictionary
dict_oz = dict(zipObj)

#Grab the Microphone 
r = sr.Recognizer()

with sr.Microphone() as source: 
    try:
        print("SPEAK NOW...")
        r.adjust_for_ambient_noise(source)
        data = r.record(source, duration=2)
        voice_input = r.recognize_google(data)
        print(voice_input)

    except:
        print("i couldn't understand you human creature... ")

#Request the voice_input from dictionary 
if voice_input != None: 
    translated_text = dict_oz.get(voice_input)

if translated_text != None:
    print(translated_text)

#Play sound when we have the sound 
if translated_text == "alatho":
    os.system("mpg123 " + alatho)

if translated_text != None and translated_text == "ozkavosh":
    os.system("mpg123 " + ozkavosh )
    
else:
    print("We couldnt translate your silly humanish!")




