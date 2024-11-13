import os
import requests
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from langdetect import detect
import pyttsx3
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Streamlit
st.set_page_config(page_title="Dyslexia Communication Assistant", layout="centered")

# Gemini API key
API_KEY = "your API key"


# Function to correct text using Gemini API
def correct_text_gemini(text, language):
    try:
        if language == "es":
            prompt = f"Please correct the following text for dyslexia: {text}"
        elif language == "en":
            prompt = f"Please correct the following text for dyslexia: {text}"
        else:
            prompt = f"Please correct the following text for dyslexia in {language}: {text}"

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")  
        response = model.generate_content(prompt)
        if response:
            return response.text
        else:
            st.error("Error generating text correction.")
            return text
    except Exception as e:
        st.error(f"Error calling the Gemini API: {str(e)}")
    return text

# Function to capture text by voice
def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak now.")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='es-ES')
        st.write("Recognized text: ", text)
        return text
    except sr.UnknownValueError:
        st.error("Could not recognize the audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"Error with Google Speech Recognition service: {e}")
    return ""

# Function to read text aloud
def read_aloud(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 1)  
    engine.say(text)
    engine.runAndWait()

# Function to load progress data from a CSV file
def load_data():
    if os.path.exists("progress.csv"):
        return pd.read_csv("progress.csv")
    else:
        return pd.DataFrame(columns=["Date", "Exercises Completed"])

# Function to add daily practice data
def add_progress(exercises):
    current_date = datetime.now().strftime("%Y-%m-%d")
    st.session_state.data = st.session_state.data.append({"Date": current_date, "Exercises Completed": exercises}, ignore_index=True)

# Function to save progress data to a CSV file
def save_data():
    st.session_state.data.to_csv("progress.csv", index=False)

# Initial configuration of progress data
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Streamlit interface 
st.title("Dyslexia Communication Assistant")

# Dynamic style for buttons
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# choose between typing or speaking
option = st.selectbox("Choose how to enter the text:", ["Type", "Speak"])

if option == "Type":

    user_text = st.text_area("Type the text to correct", height=200, placeholder="Type your text here...")

elif option == "Speak":

    user_text = capture_voice()

# Detect the language of the text (default in Spanish)
if user_text:
    language = detect(user_text)
    st.write(f"Detected language: {language}")

    with st.spinner('Correcting the text...'):
        corrected_text = correct_text_gemini(user_text, language)
    
    # Display the result with visual feedback
    if corrected_text:
        st.success("Text corrected successfully.")
        st.markdown(f"### Corrected text: \n{corrected_text}")
        # Read the corrected text aloud
        if st.button("Listen to the corrected text"):
            read_aloud(corrected_text)
    else:
        st.error("There was a problem correcting the text.")
else:
    st.warning("Please enter a text to correct.")

# Customized activities to improve reading comprehension
st.subheader("Recommended Activity: Read Aloud")

activity = st.radio("Choose an activity to improve reading comprehension", 
                    ("Read the text aloud", "Answer questions about the text"))

if activity == "Read the text aloud":
    st.write("Please read the following text aloud to improve your reading fluency:")
    st.markdown(f"**Text to read:** {user_text}")
    if st.button("Listen to the text to practice"):
        read_aloud(user_text)
elif activity == "Answer questions about the text":
    st.write("What do you think the text you read means? Provide a brief reflection.")
    st.text_area("Write your reflection here:", height=100)

# Save progress daily
exercises = st.number_input("How many exercises did you complete today?", min_value=0, step=1)
if st.button("Record Progress"):
    add_progress(exercises)
    st.success("Progress recorded!")

# Display progress data
st.write("### Daily Progress")
st.write(st.session_state.data)

# Display the progress graph
fig, ax = plt.subplots()
ax.bar(st.session_state.data["Date"], st.session_state.data["Exercises Completed"])
ax.set_xlabel("Date")
ax.set_ylabel("Exercises Completed")
ax.set_title("Daily Exercise Progress")
plt.xticks(rotation=45)
st.pyplot(fig)

# Save data when closing the application
st.button("Save Progress", on_click=save_data)
