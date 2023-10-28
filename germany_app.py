import streamlit as st
from gtts import gTTS
import os
import re
import sys
from pydub import AudioSegment
from pydub.playback import play

# Function to create the pronunciation audio file if it doesn't exist


def create_pronunciation_audio(text, filename):
    if not os.path.exists(filename):
        tts = gTTS(text, lang='de')
        tts.save(filename)

# Function to extract words from a sentence


def extract_words(sentence):
    return re.findall(r'\b\w+\b', sentence)

# Streamlit app


def main():
    st.title("German Pronunciation App")

    # Command-line argument for the input file
    input_file = st.text_input(
        "Enter the path to a file with German sentences:", sys.argv[1] if len(sys.argv) > 1 else "")

    if input_file:
        if not os.path.exists(input_file):
            st.error(f"The file '{input_file}' does not exist.")
            return

        # Read sentences from the specified file
        with open(input_file, 'r', encoding='utf-8') as file:
            sentences = file.readlines()

        # Display the sentences and allow users to click to listen
        st.subheader("Sentences and Word Pronunciation")

        key = 1
        for idx, sentence in enumerate(sentences):
            st.markdown(f"{idx + 1}. {sentence}")

            sentence_audio_file = f"audio/sentence_{idx + 1}.mp3"
            create_pronunciation_audio(sentence, sentence_audio_file)

            if st.button(f"Listen to Sentence {idx + 1}"):
                audio = AudioSegment.from_file(sentence_audio_file)
                play(audio)

#            # Extract words from the sentence and allow users to click to listen
#            words = extract_words(sentence)
#
#            word_buttons = st.empty()
#            for word in words:
#                word_audio_file = f"audio/word_{idx + 1}_{word}.mp3"
#                create_pronunciation_audio(word, word_audio_file)
#                if word_buttons.button(f"Listen to '{word}'", key=key):
#                    audio = AudioSegment.from_file(word_audio_file)
#                    play(audio)
#                key += 1


if __name__ == '__main__':
    if not os.path.exists("audio"):
        os.mkdir("audio")
    main()
