import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Google TTS Function
def google_synthesize_speech(text, output_filename, language_code, voice_name, speaking_rate=1.0, pitch=0.0):
    """Synthesizes speech from the input string of text using Google TTS."""
    start_time = time.time()
    try:
        # Use secrets for credentials instead of a file path
        credentials_dict = st.secrets["gcp_service_account"]
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )
        response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Audio content written to file "{output_filename}"')
        print(f'Time taken to generate audio: {time_taken:.2f} seconds')
        return time_taken
    except Exception as e:
        st.error(f"Error in Google TTS: {str(e)}")
        return None

# ElevenLabs TTS Function
def elevenlabs_synthesize_speech(text, output_filename, api_key, voice_id, model_id="eleven_monolingual_v1"):
    """Synthesizes speech from the input string of text using ElevenLabs."""
    start_time = time.time()
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(output_filename, "wb") as out:
            out.write(response.content)
        end_time = time.time()
        time_taken = end_time - start_time
        print(f'Audio content written to file "{output_filename}"')
        print(f'Time taken to generate audio: {time_taken:.2f} seconds')
        return time_taken
    else:
        st.error(f"Error with ElevenLabs API: {response.status_code}, {response.text}")
        return None

# Streamlit UI Setup
st.title("Text-to-Speech Synthesis Apps")

tab1, tab2 = st.tabs(["Google TTS", "ElevenLabs TTS"])

# Google TTS Tab
with tab1:
    st.header("Google Text-to-Speech")
    text = st.text_area("Enter Text for Google TTS", "Hello, how are you today?")
    output_filename = "google_output_audio.mp3"
    
    # Language options with display names and codes
    language_options = {
        "Hindi (India)": "hi-IN", 
        "English (US)": "en-US", 
        "English (India)": "en-IN",
        "Spanish (Spain)": "es-ES", 
        "French (France)": "fr-FR"
    }
    
    language_code = st.selectbox("Select Language (Google)", list(language_options.keys()))
    selected_language_code = language_options[language_code]
    
    # Voice type description for the UI
    voice_type_desc = {
        "Standard": "Basic voice with good quality",
        "Wavenet": "Higher quality, more natural sounding voice",
        "Neural2": "Latest neural network based voices with very natural intonation",
        "Studio": "Premium studio-quality voices (limited availability)",
        "Polyglot": "Voices trained for multiple languages"
    }
    
    # Helper function to create display names with descriptions
    def format_voice_name(voice):
        parts = voice.split('-')
        if len(parts) >= 4:
            voice_type = parts[2]
            voice_id = parts[3]
            gender = "Female" if voice_id in ["A", "C", "E", "G", "I", "O"] else "Male"
            return f"{voice} ({voice_type} - {gender})"
        return voice
    
    # Comprehensive voice options for each language
    if selected_language_code == "hi-IN":
        voice_options = {
            "hi-IN-Standard-A": "hi-IN-Standard-A",
            "hi-IN-Standard-B": "hi-IN-Standard-B",
            "hi-IN-Standard-C": "hi-IN-Standard-C",
            "hi-IN-Standard-D": "hi-IN-Standard-D",
            "hi-IN-Wavenet-A": "hi-IN-Wavenet-A",
            "hi-IN-Wavenet-B": "hi-IN-Wavenet-B",
            "hi-IN-Wavenet-C": "hi-IN-Wavenet-C",
            "hi-IN-Wavenet-D": "hi-IN-Wavenet-D",
            "hi-IN-Neural2-A": "hi-IN-Neural2-A",
            "hi-IN-Neural2-B": "hi-IN-Neural2-B",
            "hi-IN-Neural2-C": "hi-IN-Neural2-C",
            "hi-IN-Neural2-D": "hi-IN-Neural2-D"
        }
    elif selected_language_code == "en-US":
        voice_options = {
            "en-US-Standard-A": "en-US-Standard-A",
            "en-US-Standard-B": "en-US-Standard-B",
            "en-US-Standard-C": "en-US-Standard-C",
            "en-US-Standard-D": "en-US-Standard-D",
            "en-US-Standard-E": "en-US-Standard-E",
            "en-US-Standard-F": "en-US-Standard-F",
            "en-US-Standard-G": "en-US-Standard-G",
            "en-US-Standard-H": "en-US-Standard-H",
            "en-US-Standard-I": "en-US-Standard-I",
            "en-US-Standard-J": "en-US-Standard-J",
            "en-US-Wavenet-A": "en-US-Wavenet-A",
            "en-US-Wavenet-B": "en-US-Wavenet-B",
            "en-US-Wavenet-C": "en-US-Wavenet-C",
            "en-US-Wavenet-D": "en-US-Wavenet-D",
            "en-US-Wavenet-E": "en-US-Wavenet-E",
            "en-US-Wavenet-F": "en-US-Wavenet-F",
            "en-US-Wavenet-G": "en-US-Wavenet-G",
            "en-US-Wavenet-H": "en-US-Wavenet-H",
            "en-US-Wavenet-I": "en-US-Wavenet-I",
            "en-US-Wavenet-J": "en-US-Wavenet-J",
            "en-US-Neural2-A": "en-US-Neural2-A",
            "en-US-Neural2-B": "en-US-Neural2-B",
            "en-US-Neural2-C": "en-US-Neural2-C",
            "en-US-Neural2-D": "en-US-Neural2-D",
            "en-US-Neural2-E": "en-US-Neural2-E",
            "en-US-Neural2-F": "en-US-Neural2-F",
            "en-US-Neural2-G": "en-US-Neural2-G",
            "en-US-Neural2-H": "en-US-Neural2-H",
            "en-US-Neural2-I": "en-US-Neural2-I",
            "en-US-Neural2-J": "en-US-Neural2-J",
            "en-US-Studio-O": "en-US-Studio-O",
            "en-US-Studio-Q": "en-US-Studio-Q"
        }
    elif selected_language_code == "en-IN":
        voice_options = {
            "en-IN-Standard-A": "en-IN-Standard-A",
            "en-IN-Standard-B": "en-IN-Standard-B",
            "en-IN-Standard-C": "en-IN-Standard-C",
            "en-IN-Standard-D": "en-IN-Standard-D",
            "en-IN-Wavenet-A": "en-IN-Wavenet-A",
            "en-IN-Wavenet-B": "en-IN-Wavenet-B",
            "en-IN-Wavenet-C": "en-IN-Wavenet-C",
            "en-IN-Wavenet-D": "en-IN-Wavenet-D",
            "en-IN-Neural2-A": "en-IN-Neural2-A",
            "en-IN-Neural2-B": "en-IN-Neural2-B",
            "en-IN-Neural2-C": "en-IN-Neural2-C",
            "en-IN-Neural2-D": "en-IN-Neural2-D"
        }
    elif selected_language_code == "es-ES":
        voice_options = {
            "es-ES-Standard-A": "es-ES-Standard-A",
            "es-ES-Standard-B": "es-ES-Standard-B",
            "es-ES-Standard-C": "es-ES-Standard-C",
            "es-ES-Standard-D": "es-ES-Standard-D",
            "es-ES-Wavenet-A": "es-ES-Wavenet-A",
            "es-ES-Wavenet-B": "es-ES-Wavenet-B",
            "es-ES-Wavenet-C": "es-ES-Wavenet-C",
            "es-ES-Wavenet-D": "es-ES-Wavenet-D",
            "es-ES-Neural2-A": "es-ES-Neural2-A",
            "es-ES-Neural2-B": "es-ES-Neural2-B",
            "es-ES-Neural2-C": "es-ES-Neural2-C",
            "es-ES-Neural2-D": "es-ES-Neural2-D",
            "es-ES-Polyglot-1": "es-ES-Polyglot-1"
        }
    elif selected_language_code == "fr-FR":
        voice_options = {
            "fr-FR-Standard-A": "fr-FR-Standard-A",
            "fr-FR-Standard-B": "fr-FR-Standard-B",
            "fr-FR-Standard-C": "fr-FR-Standard-C",
            "fr-FR-Standard-D": "fr-FR-Standard-D",
            "fr-FR-Standard-E": "fr-FR-Standard-E",
            "fr-FR-Wavenet-A": "fr-FR-Wavenet-A",
            "fr-FR-Wavenet-B": "fr-FR-Wavenet-B",
            "fr-FR-Wavenet-C": "fr-FR-Wavenet-C",
            "fr-FR-Wavenet-D": "fr-FR-Wavenet-D",
            "fr-FR-Wavenet-E": "fr-FR-Wavenet-E",
            "fr-FR-Neural2-A": "fr-FR-Neural2-A",
            "fr-FR-Neural2-B": "fr-FR-Neural2-B",
            "fr-FR-Neural2-C": "fr-FR-Neural2-C",
            "fr-FR-Neural2-D": "fr-FR-Neural2-D",
            "fr-FR-Neural2-E": "fr-FR-Neural2-E",
            "fr-FR-Polyglot-1": "fr-FR-Polyglot-1"
        }
    
    # Format voice names for better UI display
    display_voice_options = {format_voice_name(k): v for k, v in voice_options.items()}
    
    voice_name = st.selectbox("Select Voice (Google)", list(display_voice_options.keys()))
    selected_voice_name = display_voice_options[voice_name]
    
    # Show voice type information
    voice_type = selected_voice_name.split('-')[2] if len(selected_voice_name.split('-')) >= 3 else ""
    if voice_type in voice_type_desc:
        st.info(f"**Voice Type:** {voice_type_desc[voice_type]}")
    
    # Voice modification controls for Google TTS
    st.subheader("Voice Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        speaking_rate = st.slider(
            "Speaking Rate", 
            min_value=0.25, 
            max_value=4.0, 
            value=1.0, 
            step=0.05,
            help="Controls how quickly the voice speaks. 1.0 is normal speed, 0.5 is half speed, 2.0 is double speed."
        )
    
    with col2:
        pitch = st.slider(
            "Pitch", 
            min_value=-20.0, 
            max_value=20.0, 
            value=0.0, 
            step=1.0,
            help="Raises or lowers the voice pitch. 0 is default, positive values increase pitch, negative values decrease it."
        )
    
    if st.button('Synthesize Speech (Google)'):
        if text:
            with st.spinner("Generating speech with Google TTS..."):
                time_taken = google_synthesize_speech(
                    text, 
                    output_filename, 
                    selected_language_code, 
                    selected_voice_name,
                    speaking_rate=speaking_rate,
                    pitch=pitch
                )
                if time_taken is not None:
                    st.success(f"Audio synthesized successfully! Time taken: {time_taken:.2f} seconds")
                    st.audio(output_filename, format='audio/mp3')
        else:
            st.error("Please enter text to synthesize.")

# ElevenLabs TTS Tab
with tab2:
    st.header("ElevenLabs Text-to-Speech")
    text_eleven = st.text_area("Enter Text for ElevenLabs TTS", "Hello, how are you today?")
    
    # Get API key from secrets
    try:
        api_key_eleven = st.secrets["api_eleven_labs"]
    except Exception as e:
        st.error("ElevenLabs API key not found in secrets. Please add it to your Streamlit secrets.")
        api_key_eleven = None

    # ElevenLabs Voice Selection
    elevenlabs_voice_options = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Mark": "UgBBYS2sOqTuMpoF3BR0",
        "Cassidy": "56AoDkrOh6qfVPDXZ7Pt",
        "Thomas": "GBv7mTt0atIp3Br8iCZE",
        "Daniel": "onwK4e9ZLuTAKqWW03F9",
        "Josh": "TxGEqnHWrfWFTfGW9XjX",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Sam": "yoZ06aMxZJJ28mfd3POQ",
        "Antoni": "ErXwobaYiN019PkySvjV",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Bella": "EXAVITQu4vr4xnSDxMaL",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
        "Elli": "MF3mGyEYCl7XYWbV9V6O",
        "Freya": "jsCqWAovK2LkecY7zXl4",
        "Gigi": "jBpfuIE2acCO8z3wKNLl"
    }  # More voices added

    voice_name_eleven = st.selectbox("Select Voice (ElevenLabs)", list(elevenlabs_voice_options.keys()))
    selected_voice_id_eleven = elevenlabs_voice_options[voice_name_eleven]
    
    # ElevenLabs Model Selection with language support
    elevenlabs_model_options = {
        "Monolingual (English only)": "eleven_monolingual_v1",
        "Multilingual v1": "eleven_multilingual_v1",
        "Multilingual v2": "eleven_multilingual_v2"
    }
    
    # Language options for ElevenLabs
    elevenlabs_language_options = {
        "English": "en",
        "German": "de",
        "Polish": "pl",
        "Spanish": "es",
        "Italian": "it",
        "French": "fr",
        "Portuguese": "pt",
        "Hindi": "hi",
        "Arabic": "ar",
        "Chinese": "zh", 
        "Japanese": "ja",
        "Korean": "ko",
        "Indonesian": "id",
        "Dutch": "nl",
        "Russian": "ru",
        "Turkish": "tr",
        "Filipino/Tagalog": "fil",
        "Swedish": "sv",
        "Czech": "cs",
        "Danish": "da",
        "Finnish": "fi",
        "Norwegian": "no",
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        model_name_eleven = st.selectbox("Select Model", list(elevenlabs_model_options.keys()))
        selected_model_id_eleven = elevenlabs_model_options[model_name_eleven]
    
    with col2:
        language_eleven = st.selectbox("Select Language", list(elevenlabs_language_options.keys()), 
                                      disabled=selected_model_id_eleven == "eleven_monolingual_v1")
        selected_language_eleven = elevenlabs_language_options[language_eleven]
    
    # Display info about model capabilities
    if selected_model_id_eleven == "eleven_monolingual_v1":
        st.info("Monolingual model only supports English. For other languages, please select a multilingual model.")
    elif selected_model_id_eleven == "eleven_multilingual_v1":
        st.info("Multilingual v1 supports multiple languages but with lower quality than v2.")
    elif selected_model_id_eleven == "eleven_multilingual_v2":
        st.info("Multilingual v2 offers the best quality for non-English languages.")
    
    output_filename_eleven = "elevenlabs_output_audio.mp3"
    
    # Voice settings sliders
    st.subheader("Voice Settings")
    stability = st.slider("Stability", min_value=0.0, max_value=1.0, value=0.5, step=0.05, 
                         help="Higher values make the voice more stable and less varied")
    similarity_boost = st.slider("Similarity Boost", min_value=0.0, max_value=1.0, value=0.5, step=0.05,
                               help="Higher values make the voice sound more like the original voice")
    
    if st.button('Synthesize Speech (ElevenLabs)'):
        if text_eleven and api_key_eleven and selected_voice_id_eleven:
            with st.spinner("Generating speech with ElevenLabs..."):
                # Modify data based on model type and language
                if selected_model_id_eleven != "eleven_monolingual_v1":
                    # If it's a multilingual model and non-English is selected, add the language tag
                    if selected_language_eleven != "en":
                        text_eleven = f"[{selected_language_eleven}]{text_eleven}"
                
                time_taken_eleven = elevenlabs_synthesize_speech(
                    text_eleven, 
                    output_filename_eleven, 
                    api_key_eleven, 
                    selected_voice_id_eleven,
                    model_id=selected_model_id_eleven
                )
                
                if time_taken_eleven is not None:
                    st.success(f"Audio synthesized successfully! Time taken: {time_taken_eleven:.2f} seconds")
                    st.audio(output_filename_eleven, format='audio/mp3')
        else:
            st.error("Please provide text and ensure API key is configured in secrets.")