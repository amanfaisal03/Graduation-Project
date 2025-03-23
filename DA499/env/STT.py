import streamlit as st
import os
import tempfile
from moviepy.video.io.VideoFileClip import VideoFileClip
import base64
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

def extract_audio(video_path, output_format="mp3"):
    """Extract audio from a video file and save it as an audio file."""
    try:
        # Create a temporary directory to store the output
        temp_dir = tempfile.mkdtemp()
        
        # Generate output path
        video_filename = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(temp_dir, f"{video_filename}.{output_format}")
        
        # Load the video file
        video = VideoFileClip(video_path)
        
        # Get the audio from the video
        audio = video.audio
        
        if audio is None:
            return None, "No audio found in the uploaded video"
        
        # Save the audio
        audio.write_audiofile(output_path)
        
        # Close the video and audio objects to release resources
        audio.close()
        video.close()
        
        return output_path, None
    
    except Exception as e:
        return None, f"Error extracting audio: {str(e)}"

def speech_to_text(audio_path):
    """Convert speech in audio file to text using Google Speech Recognition."""
    try:
        # Convert to WAV format for compatibility with Google's recognizer
        sound = AudioSegment.from_file(audio_path)
        wav_path = os.path.join(tempfile.mkdtemp(), "temp.wav")
        sound.export(wav_path, format="wav")
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Process audio file
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            
            # Use Google's speech recognition
            text = recognizer.recognize_google(audio_data)
            
            return text, None
    
    except sr.UnknownValueError:
        return None, "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return None, f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return None, f"Error in speech recognition: {str(e)}"

def text_to_speech(text, language='en', output_format="mp3"):
    """Convert text to speech."""
    try:
        # Create temporary directory for output
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, f"synthesized_speech.{output_format}")
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_path)
        
        return output_path, None
    
    except Exception as e:
        return None, f"Error in text-to-speech conversion: {str(e)}"

def get_binary_file_downloader_html(file_path, file_label='File'):
    """Generate HTML code for a download link."""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    b64 = base64.b64encode(data).decode()
    filename = os.path.basename(file_path)
    file_ext = os.path.splitext(filename)[1][1:]
    
    mime_type = "audio/mp3" if file_ext == "mp3" else f"audio/{file_ext}"
    
    return f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {file_label}</a>'

def main():
    st.set_page_config(page_title="Audio Processing App", page_icon="🎵")
    
    st.title("Audio Processing App")
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["Extract Audio", "Speech to Text", "Text to Speech"])
    
    # Tab 1: Extract Audio from Video
    with tab1:
        st.header("Extract Audio from Video")
        st.write("Upload a video file and extract its audio")
        
        # File upload widget
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv", "flv", "wmv"], key="video_uploader")
        
        # Audio format selection
        audio_format = st.selectbox("Select output audio format", ["mp3", "wav", "ogg"], index=0)
        
        if uploaded_file is not None:
            # Display video info
            file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / (1024*1024):.2f} MB"}
            st.write("### File Details")
            for key, value in file_details.items():
                st.write(f"- {key}: {value}")
            
            # Save the uploaded video to a temporary file
            temp_video_path = os.path.join(tempfile.mkdtemp(), uploaded_file.name)
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract button
            if st.button("Extract Audio"):
                with st.spinner("Extracting audio..."):
                    output_path, error = extract_audio(temp_video_path, audio_format)
                    
                    if error:
                        st.error(error)
                    else:
                        st.success("Audio extracted successfully!")
                        
                        # Store the audio path in session state
                        if 'audio_paths' not in st.session_state:
                            st.session_state['audio_paths'] = []
                        st.session_state['audio_paths'].append(output_path)
                        st.session_state['last_audio_path'] = output_path
                        
                        # Display audio player
                        audio_filename = os.path.basename(output_path)
                        st.audio(open(output_path, 'rb').read(), format=f'audio/{audio_format}')
                        
                        # Display download link
                        st.markdown(get_binary_file_downloader_html(output_path, f"{audio_filename}"), unsafe_allow_html=True)
                        
                        # Show success message with file info
                        audio_size = os.path.getsize(output_path) / (1024 * 1024)  # in MB
                        st.write(f"### Audio File Info")
                        st.write(f"- Filename: {audio_filename}")
                        st.write(f"- Format: {audio_format}")
                        st.write(f"- Size: {audio_size:.2f} MB")

    # Tab 2: Speech to Text
    with tab2:
        st.header("Speech to Text")
        st.write("Convert speech from audio to text using Google Speech Recognition")
        
        # Option to upload audio directly or use the extracted audio
        option = st.radio("Choose audio source:", ["Upload Audio File", "Use Extracted Audio"])
        
        audio_path = None
        
        if option == "Upload Audio File":
            audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg"], key="audio_uploader")
            
            if audio_file is not None:
                # Save uploaded audio to temp file
                temp_audio_path = os.path.join(tempfile.mkdtemp(), audio_file.name)
                with open(temp_audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                
                audio_path = temp_audio_path
                st.audio(audio_file, format=f'audio/{os.path.splitext(audio_file.name)[1][1:]}')
        
        else:  # "Use Extracted Audio"
            if 'last_audio_path' in st.session_state and os.path.exists(st.session_state['last_audio_path']):
                audio_path = st.session_state['last_audio_path']
                st.success("Using previously extracted audio")
                with open(audio_path, 'rb') as f:
                    st.audio(f.read(), format=f'audio/{os.path.splitext(audio_path)[1][1:]}')
            else:
                st.warning("No extracted audio available. Please extract audio from a video first or upload an audio file.")
        
        if audio_path and st.button("Transcribe Audio"):
            with st.spinner("Transcribing audio to text... This may take a while depending on the audio length."):
                transcription, error = speech_to_text(audio_path)
                
                if error:
                    st.error(error)
                else:
                    st.success("Transcription completed!")
                    
                    # Display transcription
                    st.subheader("Transcription:")
                    st.text_area("", transcription, height=250)
                    
                    # Save to session state for TTS
                    st.session_state['transcribed_text'] = transcription
                    
                    # Download as text file option
                    st.download_button(
                        label="Download Transcription",
                        data=transcription,
                        file_name="transcription.txt",
                        mime="text/plain"
                    )

    # Tab 3: Text to Speech
    with tab3:
        st.header("Text to Speech")
        st.write("Convert text to spoken audio")
        
        # Option to enter text or use transcribed text
        option = st.radio("Choose text source:", ["Enter New Text", "Use Transcribed Text"])
        
        text_to_convert = ""
        
        if option == "Enter New Text":
            text_to_convert = st.text_area("Enter text to convert to speech:", height=150)
        else:  # "Use Transcribed Text"
            if 'transcribed_text' in st.session_state and st.session_state['transcribed_text']:
                text_to_convert = st.session_state['transcribed_text']
                st.text_area("Transcribed text:", text_to_convert, height=150)
            else:
                st.warning("No transcribed text available. Please transcribe audio first or enter new text.")
        
        # Language selection
        languages = [
            ("English", "en"), ("French", "fr"), ("Spanish", "es"), 
            ("German", "de"), ("Italian", "it"), ("Portuguese", "pt"),
            ("Russian", "ru"), ("Japanese", "ja"), ("Korean", "ko"),
            ("Chinese", "zh-CN"), ("Arabic", "ar")
        ]
        
        language = st.selectbox("Select language:", languages, format_func=lambda x: x[0])
        
        if text_to_convert and st.button("Convert to Speech"):
            with st.spinner("Converting text to speech..."):
                output_path, error = text_to_speech(text_to_convert, language[1])
                
                if error:
                    st.error(error)
                else:
                    st.success("Text converted to speech successfully!")
                    
                    # Display audio player
                    with open(output_path, 'rb') as f:
                        audio_bytes = f.read()
                        st.audio(audio_bytes, format='audio/mp3')
                    
                    # Display download link
                    st.markdown(get_binary_file_downloader_html(output_path, "synthesized speech"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()