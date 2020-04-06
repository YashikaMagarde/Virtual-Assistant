# This is a virtual assistant program that gets the date, current time, responds back with a random greeting
#              and returns information on a person.

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# For ignoring all the warnings
warnings.filterwarnings('ignore')

# Record audio and return audio as a string
def recordAudio():

    #Record the audio

    # Creating a recognizer object
    r = sr.Recognizer()

    #Open the microphone and start recording
    with sr.Microphone() as source:
        print("Say something! ")
        audio = r.listen(source)

    #Use Googles Speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: '+data)
    except sr.UnknownValueError:
        print('Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error '+e)

    return data

# Function to get the virtual assistant response
def assistantResponse(text):

    print(text)

    #Convert the text to Speech
    myobj = gTTS(text=text , lang='en', slow=False)

    #Save text converted audio to a file
    myobj.save('assistant_response.mp3')

    #Play the Converted file
    os.system('start assistant_response.mp3')

# A Function for wake word(s) or phrase
def wakeWord(text):
    WAKE_WORDS = ['hi sir' ,'okay sir']

    #Converting the text to all lower case words
    text = text.lower()

    #Check to see if the users comments or text contains a woke wors or phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True


    return False

# For getting Current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    # A list of months
    month_names = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' , 'October' , 'November' , 'December']
    ordinalNumbers = ['1st' , '2nd' , '3rd' , '4th' , '5th' , '6th' , '7th' , '8th' , '9th' , '10th' , '11th' , '12th' , '13th' , '14th' , '15th' ,
                      '16th' , '17th' , '18th' , '19th' , '20th' , '21st' , '22nd' , '23rd' , '24th' ,'25th' , '26th' , '27th' , '28th' , '29th' , '30th' , '31st']


    return 'Today is '+weekday+' '+ month_names[monthNum - 1]+' the '+ ordinalNumbers[dayNum -1]+'. '

# To return Greeting response
def greeting(text):

    GREETING_INPUTS = ['hi' , 'hey' , 'greetings' , 'wassup' , 'hello']
    GREETING_RESPONSES = ['how do you do' , 'whats good' , 'hello' , 'hey there']

    #if the users input is greeting then return a randomly choosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) +'. '

    return ''

# Function to get a first and last name from a text
def getPerson(text):

    wordList = text.split()

    for i in range(0, len(wordList)):
        if i+3 <= len(wordList) -1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]


while True:
    text = recordAudio()
    response = ''

    if(wakeWord(text) == True):

        response = response + greeting(text)

        if('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date

        if('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >=12:
                meridiem = 'p.m'
                hour = now.hour -12
            else:
                meridiem ='a.m'
                hour = now.hour

            if now.minute < 10:
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)

            response = response + '  ' + 'It is '+ str(hour) + ':' + minute + ' '+ meridiem + '. '

        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + ' ' + wiki


        assistantResponse(response)
