import random, os, time

import csv

import speech_recognition as sr 

import pyglet

# get mic input for english input


print("Translator initializing...")


microphones = sr.Microphone.list_microphone_names()

print(microphones)

time.sleep(3)

d_file = 'DemonWords.csv'
e_file = 'EnglishWords.csv'

demon = []
eng = []
alatho = "alatho.mp3"
ozkavosh = "ozkavosh.mp3"

ourdevice = str(sr.Microphone(device_index=4))

audios = ['alatho' , 'ozkavosh']

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
while 1 == 1:
    with sr.Microphone(device_index=4) as source: 
        try:
            #print("LISTENING on " + ourdevice )
            r.adjust_for_ambient_noise(source)
            data = r.record(source, duration=1.5)
            voice_input = r.recognize_google(data, language="en-US")
            print(voice_input)
            #time.sleep(3)


        #Request the voice_input from dictionary 
            if voice_input != None: 
                translated_text = dict_oz.get(voice_input)

            if translated_text != None:
                print(translated_text)
            
            
            
            #if translated_text != None and translated_text == "alatho":
            #    os.system("mpg123 " + alatho)


    #Play sound when we have the sound 

        except:
            print("i couldn't understand you human creature... ")


'''
if translated_text != None and translated_text == "ozkavosh":
    os.system("mpg123 " + ozkavosh )
else:
    print("We couldnt translate your silly humanish!")
'''



