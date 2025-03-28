


# import streamlit as st
# from google.cloud import texttospeech
# import time
# import os
# import requests
# from dotenv import load_dotenv
# load_dotenv()
# # Google TTS Function
# def google_synthesize_speech(text, output_filename, credentials_path, language_code, voice_name):
#     """Synthesizes speech from the input string of text using Google TTS."""
#     start_time = time.time()
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
#     client = texttospeech.TextToSpeechClient()
#     input_text = texttospeech.SynthesisInput(text=text)
#     voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
#     audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
#     response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})
#     with open(output_filename, "wb") as out:
#         out.write(response.audio_content)
#     end_time = time.time()
#     time_taken = end_time - start_time
#     print(f'Audio content written to file "{output_filename}"')
#     print(f'Time taken to generate audio: {time_taken:.2f} seconds')
#     return time_taken

# # ElevenLabs TTS Function
# def elevenlabs_synthesize_speech(text, output_filename, api_key, voice_id):
#     """Synthesizes speech from the input string of text using ElevenLabs."""
#     start_time = time.time()
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
#     headers = {
#         "xi-api-key": api_key,
#         "Content-Type": "application/json",
#         "accept": "audio/mpeg"
#     }
#     data = {
#         "text": text,
#         "model_id": "eleven_monolingual_v1",
#         "voice_settings": {
#             "stability": 0.5,
#             "similarity_boost": 0.5
#         }
#     }
#     response = requests.post(url, json=data, headers=headers)
#     if response.status_code == 200:
#         with open(output_filename, "wb") as out:
#             out.write(response.content)
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f'Audio content written to file "{output_filename}"')
#         print(f'Time taken to generate audio: {time_taken:.2f} seconds')
#         return time_taken
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None

# # Streamlit UI Setup
# st.title("Text-to-Speech Synthesis Apps")

# tab1, tab2 = st.tabs(["Google TTS", "ElevenLabs TTS"])

# # Google TTS Tab
# with tab1:
#     st.header("Google Text-to-Speech")
#     text = st.text_area("Enter Text for Google TTS", "Hello, how are you today?")
#     credentials_path = "/Users/admin/Desktop/google-tts/train-453515-af30fa0916fd.json"
#     output_filename = "google_output_audio.mp3"
#     language_options = {"Hindi (India)": "hi-IN", "English (US)": "en-US", "Spanish (Spain)": "es-ES", "French (France)": "fr-FR"}
#     language_code = st.selectbox("Select Language (Google)", list(language_options.keys()))
#     selected_language_code = language_options[language_code]
#     voice_options = {}
#     if selected_language_code == "hi-IN":
#         voice_options = {"hi-IN-Wavenet-D": "hi-IN-Wavenet-D", "hi-IN-Standard-B": "hi-IN-Standard-B"}
#     elif selected_language_code == "en-US":
#         voice_options = {"en-US-Wavenet-D": "en-US-Wavenet-D", "en-US-Standard-B": "en-US-Standard-B"}
#     elif selected_language_code == "es-ES":
#         voice_options = {"es-ES-Wavenet-D": "es-ES-Wavenet-D", "es-ES-Standard-B": "es-ES-Standard-B"}
#     elif selected_language_code == "fr-FR":
#         voice_options = {"fr-FR-Wavenet-D": "fr-FR-Wavenet-D", "fr-FR-Standard-B": "fr-FR-Standard-B"}
#     voice_name = st.selectbox("Select Voice (Google)", list(voice_options.keys()))
#     selected_voice_name = voice_options[voice_name]
#     if st.button('Synthesize Speech (Google)'):
#         if text and credentials_path:
#             time_taken = google_synthesize_speech(text, output_filename, credentials_path, selected_language_code, selected_voice_name)
#             if time_taken is not None:
#                 st.success(f"Audio synthesized successfully! Time taken: {time_taken:.2f} seconds")
#                 st.audio(output_filename, format='audio/mp3')
#         else:
#             st.error("Please provide both text and credentials path.")

# # ElevenLabs TTS Tab
# with tab2:
#     st.header("ElevenLabs Text-to-Speech")
#     text_eleven = st.text_area("Enter Text for ElevenLabs TTS", "Hello, how are you today?")
#     # api_key_eleven = st.text_input("Enter ElevenLabs API Key", type="password")
#     api_key_eleven = os.environ.get('ELEVENLABS_API_KEY')
#     # voice_id_eleven = st.text_input("Enter ElevenLabs Voice ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice ID
#     voice_id_eleven = "21m00Tcm4TlvDq8ikWAM"
#     output_filename_eleven = "elevenlabs_output_audio.mp3"
#     if st.button('Synthesize Speech (ElevenLabs)'):
#         if text_eleven and api_key_eleven and voice_id_eleven:
#             time_taken_eleven = elevenlabs_synthesize_speech(text_eleven, output_filename_eleven, api_key_eleven, voice_id_eleven)
#             if time_taken_eleven is not None:
#                 st.success(f"Audio synthesized successfully! Time taken: {time_taken_eleven:.2f} seconds")
#                 st.audio(output_filename_eleven, format='audio/mp3')
#         else:
#             st.error("Please provide text, API key, and voice ID.")
            
            
import streamlit as st
from google.cloud import texttospeech
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Google TTS Function
def google_synthesize_speech(text, output_filename, credentials_path, language_code, voice_name):
    """Synthesizes speech from the input string of text using Google TTS."""
    start_time = time.time()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    end_time = time.time()
    time_taken = end_time - start_time
    print(f'Audio content written to file "{output_filename}"')
    print(f'Time taken to generate audio: {time_taken:.2f} seconds')
    return time_taken

# ElevenLabs TTS Function
def elevenlabs_synthesize_speech(text, output_filename, api_key, voice_id):
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
        "model_id": "eleven_monolingual_v1",
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
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Streamlit UI Setup
st.title("Text-to-Speech Synthesis Apps")

tab1, tab2 = st.tabs(["Google TTS", "ElevenLabs TTS"])

# Google TTS Tab
with tab1:
    st.header("Google Text-to-Speech")
    text = st.text_area("Enter Text for Google TTS", "Hello, how are you today?")
    credentials_path = "/workspaces/streamlit_tts_app/creds.json"
    output_filename = "google_output_audio.mp3"
    language_options = {"Hindi (India)": "hi-IN", "English (US)": "en-US", "Spanish (Spain)": "es-ES", "French (France)": "fr-FR"}
    language_code = st.selectbox("Select Language (Google)", list(language_options.keys()))
    selected_language_code = language_options[language_code]
    voice_options = {}
    if selected_language_code == "hi-IN":
        voice_options = {"hi-IN-Wavenet-D": "hi-IN-Wavenet-D", "hi-IN-Standard-B": "hi-IN-Standard-B"}
    elif selected_language_code == "en-US":
        voice_options = {"en-US-Wavenet-D": "en-US-Wavenet-D", "en-US-Standard-B": "en-US-Standard-B"}
    elif selected_language_code == "es-ES":
        voice_options = {"es-ES-Wavenet-D": "es-ES-Wavenet-D", "es-ES-Standard-B": "es-ES-Standard-B"}
    elif selected_language_code == "fr-FR":
        voice_options = {"fr-FR-Wavenet-D": "fr-FR-Wavenet-D", "fr-FR-Standard-B": "fr-FR-Standard-B"}
    voice_name = st.selectbox("Select Voice (Google)", list(voice_options.keys()))
    selected_voice_name = voice_options[voice_name]
    if st.button('Synthesize Speech (Google)'):
        if text and credentials_path:
            time_taken = google_synthesize_speech(text, output_filename, credentials_path, selected_language_code, selected_voice_name)
            if time_taken is not None:
                st.success(f"Audio synthesized successfully! Time taken: {time_taken:.2f} seconds")
                st.audio(output_filename, format='audio/mp3')
        else:
            st.error("Please provide both text and credentials path.")

# ElevenLabs TTS Tab
with tab2:
    st.header("ElevenLabs Text-to-Speech")
    text_eleven = st.text_area("Enter Text for ElevenLabs TTS", "Hello, how are you today?")
    # api_key_eleven = os.environ.get('ELEVENLABS_API_KEY')
    api_key_eleven = 'sk_9c9bca1f2f1fa8d6b49fff377540fa15601eabc67a49bebd'

    # ElevenLabs Voice Selection
    elevenlabs_voice_options = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Clyde": "2EiwWnXFnvU5JabPnvhX",
        "Domi": "AZnzlk1XvdvUeBnZuKmr",
        "Bella": "EXAVTjldLCmjljKP351r",
        "Antoni": "ErXwobaYiN019PXIpEWx",
        "Josh": "TxGEqnHWyiGGUDrREhUu",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Sam": "yoZ06aetlK24chk0IIhk",
        "Glinda": "z9fAnlkpzvi1yqmWHvjz",
    }  # Add more voices as needed

    voice_name_eleven = st.selectbox("Select Voice (ElevenLabs)", list(elevenlabs_voice_options.keys()))
    selected_voice_id_eleven = elevenlabs_voice_options[voice_name_eleven]

    output_filename_eleven = "elevenlabs_output_audio.mp3"
    if st.button('Synthesize Speech (ElevenLabs)'):
        if text_eleven and api_key_eleven and selected_voice_id_eleven:
            time_taken_eleven = elevenlabs_synthesize_speech(text_eleven, output_filename_eleven, api_key_eleven, selected_voice_id_eleven)
            if time_taken_eleven is not None:
                st.success(f"Audio synthesized successfully! Time taken: {time_taken_eleven:.2f} seconds")
                st.audio(output_filename_eleven, format='audio/mp3')
        else:
            st.error("Please provide text, API key, and voice ID.")