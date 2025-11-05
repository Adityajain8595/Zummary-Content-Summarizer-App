from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from langchain.schema import Document
import os
from dotenv import load_dotenv
load_dotenv()

def extract_youtube_video_id(url):
    # Handles both long and short formats
    if "youtube.com" in url:
        return parse_qs(urlparse(url).query).get('v', [None])[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    return None

def get_transcript_as_document(url):
    video_id = extract_youtube_video_id(url)
    try:    
        # Create an instance and use the fetch method to get the transcript
        transcript_api = YouTubeTranscriptApi()
        transcript_data = transcript_api.list(video_id)  # First list available transcripts
        transcript = transcript_data.fetch()  # Then fetch the transcript
        
        # Format the transcript
        full_text = ""
        for entry in transcript:
            if isinstance(entry, dict) and 'text' in entry:
                full_text += entry['text'] + "\n"
            elif hasattr(entry, 'text'):
                full_text += entry.text + "\n"
            else:
                full_text += str(entry) + "\n"
        
        return [Document(page_content=full_text.strip())]
    
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")