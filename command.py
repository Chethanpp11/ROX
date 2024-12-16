import pyttsx3
import os
import speech_recognition as sr
import eel
import time
import datetime
import platform
import wikipedia
from newsapi import NewsApiClient

import requests

def fetch_weather_info(city_name):
    try:
        # Replace with your actual OpenWeatherMap API key
        API_KEY = "70aa0497454c86c412510a2a8405a661"  
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        
        # Construct the API URL
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"  # For temperature in Celsius
        }
        
        # Send a GET request to the weather API
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        # Parse the JSON response
        weather_data = response.json()
        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        # Construct the weather update message
        weather_info = (
            f"The current weather in {city_name} is {weather_desc} "
            f"with a temperature of {temp}°C. Humidity is at {humidity}% "
            f"and wind speed is {wind_speed} m/s."
        )
        return weather_info
    
    except requests.exceptions.HTTPError:
        return "Sorry, I couldn't retrieve the weather information. Please check the city name or try again later."
    except requests.exceptions.ConnectionError:
        return "Sorry, there seems to be a network issue. Please check your connection and try again."
    except KeyError:
        return f"Sorry, I couldn't find weather data for {city_name}. Please check the spelling or try a different city."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Initialize NewsApiClient with your API key
api_key = 'e40d52971aa140529cb2dc829c8153d6'  # Replace with your NewsAPI key
newsapi = NewsApiClient(api_key=api_key)

# Function to fetch the latest Indian news
def fetch_latest_news():
    try:
        # Fetch the top headlines from India
        top_headlines = newsapi.get_top_headlines(language='en', page_size=3)  # Adjust the number of articles as needed
        if top_headlines['status'] == 'ok' and top_headlines['articles']:
            news = ""
            for article in top_headlines['articles']:
                news += f"Title: {article['title']}\nDescription: {article['description']}\nSource: {article['source']['name']}\n\n"
            return news
        else:
            return "Sorry, I couldn't fetch the latest news at the moment."
    except Exception as e:
        return f"An error occurred: {e}"
    
def user_greetings():
    try:
        # Get the current hour
        current_hour = datetime.datetime.now().hour

        # Determine the appropriate greeting
        if 0 <= current_hour < 12:
            greeting = "Good Morning"
        elif 12 <= current_hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        # Construct the greeting message
        greeting_message = f"{greeting}! How can I assist you today?"

        # # Speak and print the greeting
        # speak(greeting_message)
        # print(greeting_message)

        return greeting_message
    except Exception as e:
        error_message = f"An error occurred while generating the greeting: {e}"
        speak(error_message)
        print(error_message)
        return error_message

# Function to fetch Wikipedia information
def fetch_wikipedia_info(query):
    try:
        # Fetch the summary from Wikipedia for the given query
        info = wikipedia.summary(query, sentences=1)  # Limit to 1 sentence for brevity
        return info
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation error if there are multiple meanings for the query
        return f"There's more than one option for '{query}'. Please specify further."
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Sorry, the Wikipedia server took too long to respond."
    except wikipedia.exceptions.RedirectError:
        return "Sorry, the page you are looking for has been redirected."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any page related to that."
    
def restart_system():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")  # Command for Windows
    except Exception as e:
        print(f"Error: {e}")

def shutdown_system():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")  # Command for Windows
    except Exception as e:
        print(f"Error: {e}")

def speak(text):
    # text = str(text)
    # engine = pyttsx3.init('sapi5')
    # voices = engine.getProperty('voices') 
    # engine.setProperty('voice', voices[0].id)
    # engine.setProperty('rate', 174)
    # eel.DisplayMessage(text)
    # engine.say(text)
    # eel.receiverText(text)
    # engine.runAndWait()
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)


    except Exception as e:
        return ""
    
    return query.lower()


@eel.expose
# def allCommands(message=1):

#     if message == 1:
#         query = takecommand()
#         print(query)
#         eel.senderText(query)
#     else:
#         query = message
#         eel.senderText(query)
#     try:

#         if "open" in query:
#             from engine.features import openCommand
#             openCommand(query)
#         elif "on youtube" in query:
#             from engine.features import PlayYoutube
#             PlayYoutube(query)
        
#         elif "send message" in query or "phone call" in query or "video call" in query:
#             from engine.features import findContact, whatsApp, makeCall, sendMessage
#             contact_no, name = findContact(query)
#             if(contact_no != 0):
#                 speak("Which mode you want to use whatsapp or mobile")
#                 preferance = takecommand()
#                 print(preferance)

#                 if "mobile" in preferance:
#                     if "send message" in query or "send sms" in query: 
#                         speak("what message to send")
#                         message = takecommand()
#                         sendMessage(message, contact_no, name)
#                     elif "phone call" in query:
#                         makeCall(name, contact_no)
#                     else:
#                         speak("please try again")
#                 elif "whatsapp" in preferance:
#                     message = ""
#                     if "send message" in query:
#                         message = 'message'
#                         speak("what message to send")
#                         query = takecommand()
                                        
#                     elif "phone call" in query:
#                         message = 'call'
#                     else:
#                         message = 'video call'
                                        
#                     whatsApp(contact_no, query, message, name)

#         elif "whats the date" in query:
#                         speak("It's "+str(datetime.datetime.now().date()))
#                         print("It's "+str(datetime.datetime.now().date()))

#         elif "whats the time" in query:
#                         speak("It's " + datetime.datetime.now().strftime("%I:%M:%S %p"))  # 12-hour format with AM/PM
#                         print("It's " + datetime.datetime.now().strftime("%I:%M:%S %p"))

#         elif "whats the day of week" in query:
#             now = datetime.datetime.now()
#             day_of_week = now.strftime("%A")  # Get the full name of the day (e.g., Monday)
#             speak("It's " + day_of_week)
#             print("It's " + day_of_week)

#         elif "whats the year" in query:
#             now = datetime.datetime.now()
#             year = now.year
#             speak("It's " + str(year))
#             print("It's " + str(year))

#         elif "whats the month" in query:
#             now = datetime.datetime.now()
#             month_name = now.strftime("%B")  # Get the full month name (e.g., December)
#             speak("It's " + month_name)
#             print("It's " + month_name)

#         elif "whats the day" in query:
#             now = datetime.datetime.now()
#             day = now.day
#             speak("It's " + str(day))
#             print("It's " + str(day))
#         # Checking for "from wikipedia" in query
#         elif "from wikipedia" in query:
#             topic = query.replace("from wikipedia", "").strip()  # Extract the topic from the query
#             if topic:  # If a topic is provided in the query
#                 wikipedia_info = fetch_wikipedia_info(topic)
#                 speak(f"Here is some information about {topic} from Wikipedia: {wikipedia_info}")
#                 print(f"Here is some information about {topic} from Wikipedia: {wikipedia_info}")
#             else:
#                 speak("Please provide a topic to search from Wikipedia.")
#                 print("Please provide a topic to search from Wikipedia.")

#         # Checking for "latest news" in the query
#         elif "latest news" in query:
#             latest_news = fetch_latest_news()
#             speak(f"Here are the latest news headlines: {latest_news}")
#             print(f"Here are the latest news headlines: {latest_news}")
        
#         elif "introduce yourself" in query:
#                         speak("Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")
#                         print("ROX: Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")
#         elif "tell us about yourself" in query:
#                         speak("Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")
#                         print("ROX: Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")
#         if "restart my computer" in query:
#             restart_system()
#             speak("Restarting the system.")
#             print("Restarting the system.")
#         elif "shutdown my computer" in query:
#             shutdown_system()
#             speak("Shutting down the system.")
#             print("Shutting down the system.")
#         elif "greet me" in query:
#             greeting = user_greetings()
#             speak(greeting)
#             print(greeting)
#         else:
#             from engine.features import chatBot
#             chatBot(query)
#     except:
#         print("error")
    
#     eel.ShowHood()

def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    try:
        # Normalize input
        query = query.lower().strip()  
        print(f"Processed query: {query}")  # Debugging log

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                message = ""
                if "send message" in query:
                    message = 'message'
                    speak("What message to send?")
                    query = takecommand()
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'

                whatsApp(contact_no, query, message, name)

        elif "whats the date" in query:
            speak("It's " + str(datetime.datetime.now().date()))
            print("It's " + str(datetime.datetime.now().date()))

        elif "whats the time" in query:
            speak("It's " + datetime.datetime.now().strftime("%I:%M:%S %p"))
            print("It's " + datetime.datetime.now().strftime("%I:%M:%S %p"))

        elif "whats the day of week" in query:
            now = datetime.datetime.now()
            day_of_week = now.strftime("%A")
            speak("It's " + day_of_week)
            print("It's " + day_of_week)

        elif "whats the year" in query:
            now = datetime.datetime.now()
            year = now.year
            speak("It's " + str(year))
            print("It's " + str(year))

        elif "whats the month" in query:
            now = datetime.datetime.now()
            month_name = now.strftime("%B")
            speak("It's " + month_name)
            print("It's " + month_name)

        elif "whats the day" in query:
            now = datetime.datetime.now()
            day = now.day
            speak("It's " + str(day))
            print("It's " + str(day))

        elif "from wikipedia" in query:
            topic = query.replace("from wikipedia", "").strip()
            if topic:
                wikipedia_info = fetch_wikipedia_info(topic)
                speak(f"Here is some information about {topic} from Wikipedia: {wikipedia_info}")
                print(f"Here is some information about {topic} from Wikipedia: {wikipedia_info}")
            else:
                speak("Please provide a topic to search from Wikipedia.")
                print("Please provide a topic to search from Wikipedia.")
        
        elif "weather in" in query:
            city_name = query.replace("weather in", "").strip()  # Extract the city name from the query
            if city_name:  # Check if a city name is provided
                weather_info = fetch_weather_info(city_name)
                speak(f"Here is the current weather for {city_name}: {weather_info}")
                print(f"Here is the current weather for {city_name}: {weather_info}")
            else:
                speak("Please provide the name of the city to get the weather update.")
                print("Please provide the name of the city to get the weather update.")


        elif "latest news" in query:
            latest_news = fetch_latest_news()
            speak(f"Here are the latest news headlines: {latest_news}")
            print(f"Here are the latest news headlines: {latest_news}")

        elif "introduce yourself" in query:
            speak("Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil, and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")
            print("ROX: Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil, and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")

        elif "tell us about yourself" in query:
            speak("Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil, and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")
            print("ROX: Hello! I'm ROX, your friendly AI voice assistant, built by the amazing trio: Kanva, Nikhil, and Chethan. My mission? To simplify your digital tasks and maybe, just maybe, become your favorite. Warning: I might be too cool for you to get addicted to me!")

        elif "restart my computer" in query:
            restart_system()
            speak("Restarting the system.")
            print("Restarting the system.")

        elif "shutdown my computer" in query:
            shutdown_system()
            speak("Shutting down the system.")
            print("Shutting down the system.")

        elif "greet me" in query:
            greeting = user_greetings()
            speak(greeting)
            print(greeting)

        else:
            from engine.features import chatBot
            chatBot(query)

    except Exception as e:
        print(f"Error occurred: {e}")

    eel.ShowHood()

