# Importing necessary libraries
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

# Initialize voice engine and other global variables
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = ""  # Placeholder for News API key
wolfram = ""  # Placeholder for WolframAlpha API key

# Model for generating responses using LLaMA 3.2
model_name = "meta-llama/Llama-3.2-3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to speak text aloud
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

# Function to generate response using the LLaMA model
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Greet the user based on the time of the day
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("Hello? How may I help you?")

# Write a note and optionally add the current time
def write_note():
    speak("What should I write, sir?")
    note = takeCommand()
    
    if note:
        with open('jarvis.txt', 'w') as file:
            speak("Sir, should I include the date and time?")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(f"{strTime} :- {note}\n")
            else:
                file.write(f"{note}\n")
        speak("Note has been written successfully.")
    else:
        speak("I couldn't hear the note properly.")

# Send an email with specified details
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

# Function to fetch email details using voice input
def get_email_details():
    try:
        speak("Who should I send the email to?")
        recipient_email = takeCommand()

        speak("What should be the subject?")
        subject = takeCommand()

        speak("What should be the content of the email?")
        body = takeCommand()

        return recipient_email, subject, body
    except Exception as e:
        speak("I couldn't understand that. Please try again.")
        print(f"Error: {e}")
        return None, None, None

# Tell the current day of the week
def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    
    if day in Day_dict:
        speak(f"The day is {Day_dict[day]}")

# Tell the current time
def tellTime():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    hour = time[0:2]
    minute = time[3:5]
    speak(f"The time is {hour} hours and {minute} minutes.")

# Fetch news headlines using the NewsAPI
def fetch_news():
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    if r.status_code == 200:
        articles = r.json().get("articles", [])
        if articles:
            for i, article in enumerate(articles[:5], 1):  # Limit to 5 headlines
                headline = article['title']
                print(f"{i}. {headline}")
                speak(f"Headline {i}. {headline}")
        else:
            speak("No news found.")
    else:
        speak("Failed to fetch the news.")

# Process the recognized command and map it to specific functions
def processCommand(command):
    command = command.lower()
    
    # Basic commands for opening websites
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "news" in command:
        speak("Fetching the latest news...")
        fetch_news()
    elif "day" in command:
        tellDay()
    elif "time" in command:
        tellTime()
    elif "search for" in command:
        speak("Checking Wikipedia")
        query = command.replace("search for", "").strip()
        try:
            result = wikipedia.summary(query, sentences=4)
            speak(f"According to Wikipedia: {result}")
        except wikipedia.exceptions.DisambiguationError:
            speak("The query is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any results.")
        except Exception:
            speak("There was a problem connecting to Wikipedia.")
    elif "send an email" in command:
        sender_email = "tech4earthh@gmail.com"
        sender_password = "ItsDump13*"  # Use app-specific password if using Gmail
        recipient_email, subject, body = get_email_details()

        if recipient_email and subject and body:
            send_email(sender_email, sender_password, recipient_email, subject, body)
        else:
            speak("Couldn't get the email details properly.")
    
    # LLaMA model response for unhandled queries
    else:
        response = generate_response(command)
        speak(response)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    greet()

# Main loop: waits for the activation word 'hello'
while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)

        if word.lower() == "hello":
            speak("Yes sir?")
            # Capture the actual command after activation
            with sr.Microphone() as source:
                print("Jarvis Active...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                print(command)
                processCommand(command)

    except Exception as e:
        print(f"Error: {e}")
