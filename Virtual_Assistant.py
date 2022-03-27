# Description : This  is  a virtual assistant program that gets the date, current time, responds back with a random greeting,
#  and return information on a person.

#pip  install PyAudio
#pip install SpeechRecognition
#pip install  gTTS
#pip install wikipedia

#Import the libraries
import  speech_recognition  as  sr
import os
from gtts import  gTTS
import datetime
import warnings
import calendar
import  random
import wikipedia

#Ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return it as a string
def  recordAudio():
    #Record the audio
    r = sr.Recognizer()  #Creating  a recogniser object

    #Open the microphone and start recording
    with sr.Microphone()  as source:
        print('Say Something')
        audio = r.listen(source)

   #Use google speech recognition
        data = ' '
    try:
        data =r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError: #Check  for  unknown errors
        print('Google Speech Recognition could not  understand  the audio, unknown error')
    except sr.RequestError as e:
        print('Request  results from Google Speech Recognition service error '+ e)
    return data

# A Function to get the virtual assistant response
def assistantResponse(text):

    print(text)

    #Convert the text to speech
    myobj = gTTS(text=text,  lang='en',  slow=False)

    #Save the converted audio to a file
    myobj.save('assistant_response.mp3')

    #Play the converted file
    os.system('start assistant_response.mp3')

# A function for wake word (s) or phrase
def wakeWord(text):
    WAKE_WORDS = ('zelexa','ok hp','hi hp','hey hp','okay hp') # A list of wake words
    text = text.lower() # Converting the text to all lower case words

    #Check  to see if the users command /text contains a wake word/phrase
    for phrase in WAKE_WORDS:
        if  phrase in text:
            return True
    #If the wake word isn't found in the text from the loop and so it returns false
    return False

# A function to give the current date
def  getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    #A list of months
    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

    return 'Today is  '+weekday+ ' , ' +month_names[monthNum-1]+' the '+ str(dayNum)+'th .'

#A function to return a random greeting response
def greeting(text):

    #Greeting inputs
    GREETING_INPUTS = ['hi','hey','ram ram','namaste']

    #Greeting_responses
    GREETING_RESPONSES = ['howdy', 'whats good','hello','hey there']

    # If the users input is a greeting , then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)+'.'

    #If  the greeting was detected then return as empty string
    return ' '

# A function to get a persons first and last name from the text
def  getPerson(text):

    wordlist = text.split() #splitting the text into a list of words

    for i in range(0, len(wordlist)):
       if i+3 <= len(wordlist) -1 and wordlist[i].lower() ==  'who' and wordlist[i+1].lower() == 'is':
            return wordlist[i+2]+ ' '+ wordlist[i+3]

while True:

    #Record the audio
    text = recordAudio()
    response = ''

    #Check for the wake word/phrase
    if(wakeWord(text)  == True):

        #Check for greetings by the user
        response = response + greeting(text)

        #Check to see if the user said anything having to do with the date
        if('date' in text):
            get_date = getDate()
            response = response + ' '+get_date

        #Check to see if the user said 'who is'
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person,sentences=2)
            response = response +' '+wiki

        #Check to see if the user said anything having to do with the time
        if('time' in text):
            now = datetime.datetime.now()
            meridian = ''
            if now.hour >=12:
                meridian = 'p.m' # post Meridian (PM) after midday
                hour = now.hour -12
            else:
                meridian = 'a.m' #Anti Meridian (AM) before midday
                hour = now.hour

             #Convert minute into a proper string
            if now.minute <10:
                minute = '0'+str(now.minute)
            else :
                minute = str(now.minute)

            response = response + ' It is '+str(hour)+':'+minute+' '+meridian+' .'

        #Have the assistant response back using audio and the text from response
        assistantResponse(response)


