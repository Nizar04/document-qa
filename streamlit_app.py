import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import openai
import re
import requests
from deep_translator import GoogleTranslator
from langdetect import detect


def get_video_metadata(video_id):
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(oembed_url)
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('title', 'Unknown Title'),
                'author': data.get('author_name', 'Unknown Channel'),
                'thumbnail': data.get('thumbnail_url', None)
            }
        return None
    except Exception:
        return None


def get_video_id(url):
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)',
        r'(?:youtube\.com\/v\/)([\w-]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id, target_language='en'):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript = transcript_list.find_transcript([target_language])
        except:
            # If target language not available, get first available and translate
            transcript = transcript_list.find_transcript(['en'])
            if target_language != 'en':
                transcript = transcript.translate(target_language)

        formatted_transcript = TextFormatter().format_transcript(transcript.fetch())
        return formatted_transcript
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")


def get_summary(text, api_key, style='concise', length='medium'):
    style_prompts = {
        'Concise': "Create a brief, to-the-point summary",
        'Detailed': "Create a comprehensive, detailed summary",
        'Bullet points': "Create a summary in bullet points highlighting key information",
        'Academic': "Create a formal, academic-style summary"
    }

    length_tokens = {
        'Short': 300,
        'Medium': 800,
        'Long': 1200
    }

    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that {style_prompts[style]}."},
            {"role": "user", "content": f"Please provide a {length} summary of the following transcript:\n\n{text}"}
        ],
        max_tokens=length_tokens[length]
    )

    return response.choices[0].message.content


def main():
    st.set_page_config(page_title="Video Summarizer",page_icon="images/logo.svg", layout="wide")

    # Add logo
    st.logo("images/logo.svg", size="large")

    st.title("Video Summarizer")
    st.write("Enter a YouTube URL to get a summary of the video content")

    # Sidebar for settings
    with st.sidebar:
        st.subheader("Settings")
        api_key = st.text_input("OpenAI API(GPT-3.5 TURBO) Key:", type="password")
        target_language = st.selectbox(
            "Summary Language:",
            ['en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'ja', 'ko', 'zh'],
            format_func=lambda x: {'en': 'English', 'es': 'Spanish', 'fr': 'French',
                                   'de': 'German', 'it': 'Italian', 'pt': 'Portuguese',
                                   'nl': 'Dutch', 'ru': 'Russian', 'ja': 'Japanese',
                                   'ko': 'Korean', 'zh': 'Chinese'}[x]
        )
        summary_style = st.selectbox(
            "Summary Style:",
            ['Concise', 'Detailed', 'Bullet points', 'Academic']
        )
        summary_length = st.selectbox(
            "Summary Length:",
            ['Short', 'Medium', 'Long']
        )

    # Main content
    url = st.text_input("Enter YouTube URL:")

    if st.button("Generate Summary") and url and api_key:
        try:
            video_id = get_video_id(url)
            if not video_id:
                st.error("Invalid YouTube URL. Please check the URL and try again.")
                return

            with st.spinner("Fetching video information..."):
                metadata = get_video_metadata(video_id)
                if metadata:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if metadata['thumbnail']:
                            st.image(metadata['thumbnail'])
                    with col2:
                        st.subheader(metadata['title'])
                        st.write(f"Channel: {metadata['author']}")

            with st.spinner("Fetching and processing transcript..."):
                transcript = get_transcript(video_id, target_language)

                detected_lang = detect(transcript)
                st.info(f"Detected transcript language: {detected_lang}")

                st.write("Generating summary...")
                summary = get_summary(transcript, api_key, summary_style, summary_length)

                st.subheader("Video Summary")
                st.write(summary)

                with st.expander("Full Transcript"):
                    st.write(transcript)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
