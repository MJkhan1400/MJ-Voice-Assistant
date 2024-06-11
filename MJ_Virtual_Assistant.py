import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
from AppOpener import open, close
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

mj_engine = pyttsx3.init('sapi5')
my_voice = mj_engine.getProperty('voices')
mj_engine.setProperty('voice', my_voice[0].id)


def speak(audio):
    mj_engine.say(audio)
    mj_engine.runAndWait()


def MJ_wishme():
    time = int(datetime.datetime.now().hour)
    if 1 <= time < 12:
        speak("Hello and Good Morning Sir")

    elif 12 <= time < 16:
        speak("Hello and Good Afternoon Sir")

    else:
        speak("Hello and Good Evening Sir")


def takeCommand():
    recog = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        recog.pause_threshold = 1
        audio = recog.listen(source)

    try:
        print("Recognize")
        query = recog.recognize_google(audio, language="en-In")
        print("You said: ", query)

    except Exception as e:
        # print(e)
        print("Can you Repeat it please")
        speak("Can you Repeat it please")
        return "None"
    return query


def sentimentAnalysis(s):
    # TextBlob Sentiment Analysis
    sentiment = s
    blob = TextBlob(sentiment)
    textBlob_sentiment = blob.sentiment.polarity

    # Vader Sentiment Analysis
    vader = SentimentIntensityAnalyzer()
    vs = vader.polarity_scores(sentiment)
    vader_sentiment = vs["compound"]

    # Average of both sentiment scores
    average_sentiment = np.mean([textBlob_sentiment, vader_sentiment])
    print(vs)

    if average_sentiment > 0:
        return "Positive"
    elif average_sentiment < 0:
        return "Negative"
    else:
        return "Neutral"


if __name__ == "__main__":
    MJ_wishme()
    while True:
        query = takeCommand().lower()

        if 'name' in query:
            print('My name is MJ, I am a Virtual Assistant that incorporates NLP. '
                  'I was developed by Mohammad Jazib Khan and i can perform many task including opening apps, '
                  'perform sentiment analysis or search anything you want.')
            speak('My name is MJ, I am a Virtual Assistant that incorporates NLP. '
                  'I was developed by Mohammad Jazib Khan and i can perform many task including opening apps, '
                  'perform sentiment analysis or search anything you want.')

        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            output = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print("According to Wikipedia")
            print(output)
            speak(output)

        elif 'search' and 'website' in query:
            speak("Which website do you want me to open Sir.")
            print("Which website do you want me to open Sir.")
            w = takeCommand().lower()
            webbrowser.open(w+'.com')

        elif 'search' and 'youtube' in query:
            speak("What do you want me to search Sir.")
            print("What do you want me to search Sir.")
            y = takeCommand().lower()
            pywhatkit.playonyt(y)

        elif 'search' in query:
            speak("What do you want me to search Sir.")
            print("What do you want me to search Sir.")
            s = takeCommand().lower()
            pywhatkit.search(s)

        elif 'sentiment analysis' in query:
            print("Yes, Please tell me a sentence on which you want to perform sentiment analysis.")
            speak("Yes, Please tell me a sentence on which you want to perform sentiment analysis.")
            s = takeCommand().lower()
            sentiment = sentimentAnalysis(s)
            speak(sentiment)
            print("Sentiment:", sentiment)

        elif 'time' in query:
            now = datetime.datetime.now()
            Time = now.strftime("%H:%M:%S")
            speak(f"The current time is: {Time}")
            print(f"The current time is: {Time}")

        elif 'date' in query:
            date = datetime.date.today()
            speak(f"Today's date is: {date}")
            print(f"Today's date is: {date}")

        elif 'open' in query:
            speak("Opening the App")
            app_name = query.replace("open ", "")
            open(app_name, match_closest=True)  # App will be open be it matches little bit too

        elif 'close' in query:
            speak("Closing the App")
            app_name = query.replace("close ", "").strip()
            close(app_name, match_closest=True, output=False)

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'thank you' in query:
            speak("Happy to Help you anytime.")
            print("Happy to Help you anytime.")
            break
