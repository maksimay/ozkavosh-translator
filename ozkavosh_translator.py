import random, os,

import csv

import speech_recognition as sr 

print("Translator initializing...")

d_file = 'DemonWords.csv'
e_file = 'EnglishWords.csv'

demon = []
eng = []
alatho = "alatho.mp3"

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
    print("SPEAK NOW…")
    r.adjust_for_ambient_noise(source)
    data = r.record(source, duration=1.5)
    text = r.recognize_google(data)
    print(text)

#Request the voice_input from dictionary 
translated_text = dict_oz.get(text)
print(translated_text)

#Play sound when we have the sound 
if translated_text == "alatho":
    os.system("mpg123 " + alatho)

else:
    print("sound not found on disk")


