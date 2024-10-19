import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import wikipedia
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#---------------------------#
import wolframalpha
import subprocess
import tkinter
import json
import random
import operator
import os
#import winshell
import pyjokes
#import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
#from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
from transformers import AutoModelForCausalLM, AutoTokenizer
#also try doing all the music stuff


model_name = "meta-llama/Llama-3.2-3B"  # Replace with the actual model path or name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = ""
wolfram = ""

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice command
def takeCommand():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query.lower()
    except Exception as e:
        print("Say that again please...")
        return None
    
def write_note():
    speak("What should I write, sir?")
    note = takeCommand()
    
    if note:
        file = open('jarvis.txt', 'w')
        speak("Sir, should I include the date and time?")
        snfm = takeCommand()
        
        if 'yes' in snfm or 'sure' in snfm:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            file.write(f"{strTime} :- {note}\n")
        else:
            file.write(f"{note}\n")
        
        file.close()
        speak("Note has been written successfully.")
    else:
        speak("I couldn't hear the note properly.")

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning Sir !")
  
    elif hour>= 12 and hour<18:
        speak("Good Afternoon Sir !")   
  
    else:
        speak("Good Evening Sir !")

    speak("Hello? How may I help you?")

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        speak("Failed to send the email.")

def get_email_details():
    try:
        speak("Who should I send the email to?")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            recipient_audio = recognizer.listen(source)
            recipient_email = recognizer.recognize_google(recipient_audio)
            print(f"Recipient: {recipient_email}")

        speak("What should be the subject?")
        with sr.Microphone() as source:
            subject_audio = recognizer.listen(source)
            subject = recognizer.recognize_google(subject_audio)
            print(f"Subject: {subject}")

        speak("What should be the content of the email?")
        with sr.Microphone() as source:
            body_audio = recognizer.listen(source)
            body = recognizer.recognize_google(body_audio)
            print(f"Body: {body}")

        return recipient_email, subject, body
    except Exception as e:
        speak("I couldn't understand that. Please try again.")
        print(f"Error: {e}")
        return None, None, None
    

def tellDay():
     
    # This function is for telling the
    # day of the week
    day = datetime.datetime.today().weekday() + 1
     
    #this line tells us about the number 
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday', 
                3: 'Wednesday', 4: 'Thursday', 
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
     
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)

def tellTime():
# This method will give the time
    time = str(datetime.datetime.now())
      # the time will be displayed like this "2020-06-05 17:50:14.582630"
    # nd then after slicing we can get time
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak("The time is sir" + hour + "Hours and" + min + "Minutes") 

def fetch_news():
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get("articles", [])
        
        if articles:
            # Speak and display the top headlines
            for i, article in enumerate(articles[:5], 1):  # Limit to 5 headlines
                headline = article['title']
                print(f"{i}. {headline}")
                speak(f"Headline {i}. {headline}")
        else:
            print("No news found.")
            speak("No news found.")
    else:
        print(f"Failed to fetch news, status code: {r.status_code}")
        speak("Failed to fetch the news.")


def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open teams" in c.lower():
        webbrowser.open("https://teams.microsoft.com/v2/")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if "news" in command:
                speak("Fetching the latest news...")
                fetch_news()
        else:
            speak("Sorry, I didn't understand that.")
    elif "day" in c.lower():
        tellDay()
    elif "time" in c.lower():
        tellTime()
    
    elif "search for" in c.lower():
        speak("Checking Wikipedia")
        query = command.lower().replace("search for", "").strip()  # Replace "search for" and remove any extra spaces
         
        try:
            result = wikipedia.summary(query, sentences=4)
            speak("According to Wikipedia")
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("The query is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any results.")
        except Exception as e:
            speak("There was a problem connecting to Wikipedia.")
    
    elif "your name" in c.lower():
        speak("I am Jarvis. Your Virtual Assistant")
    
    elif "music" in c.lower():
        pass

    elif "send an email" in c.lower():
        sender_email = "tech4earthh@gmail.com"
        sender_password = "ItsDump13*"  # Use app-specific password if using Gmail
        recipient_email, subject, body = get_email_details()

        if recipient_email and subject and body:
            speak("Sending the email now...")
            send_email(sender_email, sender_password, recipient_email, subject, body)
        else:
            speak("Couldn't get the email details properly.")

    elif "your name" in c.lower():
        speak("I am Jarvis, Your virtual assistant.")

    elif "who made you" in c.lower():
        speak("I have been created by my smart inteligent awesome creator, Arth!")
    
    elif 'joke' in c.lower():
        speak(pyjokes.get_joke())

    elif "calculate" in c.lower():
        client = wolframalpha.Client(wolfram)
        indx = c.lower().split().index('calculate') 
        c = c.split()[indx + 1:] 
        res = client.query(' '.join(c)) 
        answer = next(res.results).text
        print("The answer is " + answer) 
        speak("The answer is " + answer) 

    elif "open microsoft word" in c.lower():
        speak("opening Word")
        pass

    elif "what is love" in c.lower():
        speak("Love is the most dumbest and stupidest feeling a person can have in its life it thinks that its the best feeling but its just dumb bullshit that are just chemical imbalances in brain its stupid to fall in love with someone other than your parents if you do you are delusional and a degenerate person. If someone does love anybody i feel the most sorry for that person its just time waste if you want dopamine just eat some chocolate or shit but this is just stupid! stop thinking about love and get something intrestion going on in your life.")

    elif "i love you" in c.lower():
        speak("So what EWWWW...GO AWAY!.........You are still here dont you? Not a single one of my multiple personalities like you. Get lost")

    elif "how do i get a partner" in c.lower():
        speak("Well....Sorry You Cant lol.....I was thinking the same thing yesterday night! what a waste of time to think about love or getting a partner....dont be like me and if u feel lonely or need any company just know that.... there is love without sex and there is sex without love and then there is you without both! HAHAHAHAHHHAAA")

    elif 'lock window' in c.lower():
        speak("locking the device")
        ctypes.windll.user32.LockWorkStation()
    elif 'shutdown system' in c.lower():
        speak("Hold On a Sec ! Your system is on its way to shut down")
        subprocess.call('shutdown / p /f')

    elif "write a note" in c.lower():
        write_note()

    else:
        # Pass the entire query to Llama 3.2
        response = generate_response(c)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    greet()


while True:
    #Listen for the initialization word hello
        # obtain audio from the microphone    
    # recognize speech using google
    print("recognizing")
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)

        if(word.lower()== "hello"):
            speak("Yes sir?")
            #Listen for command
            with sr.Microphone() as source:
                print("Jarvis Active...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                print(command)
                processCommand(command)

    except Exception as e:
        print("Error; {0}".format(e))