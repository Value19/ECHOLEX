# ECHOLEX
# Communication Assistant for Dyslexia

Welcome to the **Communication Assistant for Dyslexia** project! This web aims to support users with dyslexia by providing tools for text correction, voice input, and daily activity tracking to enhance reading comprehension and communication skills. This project was developed during a hackathon ("Innovate for good" and utilizes Gemini's API, Streamlit, etc.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#Installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Description
The **Communication Assistant for Dyslexia** web is designed to help dyslexic users improve their reading comprehension and communication. The web offers functionalities such as:

- Real-time text correction tailored for dyslexia.
- Voice input for text entry.
- Language detection and tailored correction prompts.
- Daily reading activities to support language development.
- Visual feedback and tracking of progress through interactive charts.

## Features
- **Text Correction**: Text input correction using Gemini API.
- **Voice Recognition**: Converts speech to text for users who prefer voice input.
- **Language Detection**: Detects the input language to provide language-specific feedback.
- **Daily Activities and Tracking**: Offers reading activities and tracks daily progress to encourage continuous improvement.
- **Progress Visualization**: Displays daily practice completion with charts.

## Technologies Used
- Streamlit for the user interface.
- Gemini API for language and text processing.
- SpeechRecognition for voice-to-text functionality.
- Pyttsx3 for text-to-speech.
- Matplotlib and Pandas for data visualization and progress tracking.
  
## Installation
1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Value19/ECHOLEX.git

2. Navigate into the project directory:
   
   ```bash
   cd ECHOLEX
   
4. Create a virtual environment (optional but recommended):
   
   ```bash
   python -m venv venv

5. Activate the virtual environment:
   
   ```bash
   source venv/bin/activate
   
6. Install the required dependencies
   ```bash
   pip install streamlit
   pip install requests
   pip install google-generativeai
   pip install speechrecognition
   pip install langdetect
   pip install pyttsx3
   pip install matplotlib
   pip install pandas
   pip install pyaudio

7. Set your Gemini API key. Replace the API_KEY in the script with your actual Gemini API key.
8. Run the application:
   
   ```bash
   streamlit run app.py


## Usage

Run the application using Streamlit:
streamlit run app.py

In the application:

- Enter text manually or use the voice input option.
- Receive text correction and feedback.
- Track your progress with daily activities and view your statistics.
- Additional options include reading out the corrected text and choosing from different reading comprehension activities.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For questions or suggestions, please contact rodriguezvalery192004@gmail.com.
