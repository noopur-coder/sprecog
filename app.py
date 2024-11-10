# Before using the code open terminal and install these packages


import streamlit as st
import speech_recognition as sr

# Create a dictionary to map language names to language codes
language_codes = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES"
}

def transcribe_speech(api="Google Web Speech API", saved='No', lang="English"):
    # Initialize recognizer class
    # Creating a Recognizer instance
    r = sr.Recognizer()
    
    # Creating an instance of the Microphone class
    mic = sr.Microphone()
    
    # Configure the language using language codes
    if api == "Google Web Speech API":
        language_code = language_codes[lang]
    else:
        language_code = None
    
    # Reading Microphone as source
    with mic as source:
        # Handle ambient noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        st.info("Speak now...")
        
        # listen for speech and store in audio_text variable
        recorded_audio = r.listen(source, timeout=None)  # Use timeout=None to listen indefinitely
        
        st.info("Transcribing...")

        if api=="Google Web Speech API":
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio_text)`
                text = r.recognize_google(recorded_audio, language=language_code)
                if saved=="Yes":
                    with open('my_speech.txt', 'w') as f:
                        f.write(text)
                return "Google Speech Recognition thinks you said :" + text
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Speech Recognition service; {e}"

        else:
            # recognize speech using Sphinx
            try:
                text = r.recognize_sphinx(recorded_audio, language=language_code)
                if saved=="Yes":
                    with open('my_speech.txt', 'w') as f:
                        f.write(text)
                return "Sphinx thinks you said :" + text
            except sr.UnknownValueError:
                return "Sphinx could not understand audio"
            except sr.RequestError as e:
                return f"Sphinx error; {e}"

def main():
    st.set_page_config(layout="wide")

    # Create a sidebar
    st.sidebar.title("Settings")
    
    # Choose Speech Recognition API
    api = st.sidebar.selectbox("Choose Speech Recognition API", ["Google Web Speech API", "CMU Sphinx"])
    st.sidebar.info("""
        There are more APIs like : Microsoft Bing Speech, Google Cloud Speech, Houndify by SoundHound, 
        IBM Speech to Text and Wit.ai but they all require authentication with either an API key 
        or a username/password combination.
    """)
    # Choose to save text output or not
    saved = st.sidebar.radio("Do you wish to save what you just have said ?", ["Yes", "No"])
    
    # Choose Language
    lang = st.sidebar.selectbox("Choose the language you speak with", list(language_codes.keys()))

    
    st.title("Speech Recognition App")
    st.write("Click on the microphone to start speaking:")

    # add a button to trigger speech recognition
    if st.button("Start Recording"):
        pause_state = False  # Ensure recognition is not paused
        text = transcribe_speech(api, saved)
        st.write(text)

if __name__ == "__main__":
    main()
