from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
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
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        proxy_url = os.getenv("HTTPS_PROXY")
        if proxy_url:
            os.environ["HTTPS_PROXY"] = proxy_url
            
        transcript = YouTubeTranscriptApi.fetch(video_id) 

        full_text = "\n".join([entry["text"] for entry in transcript])
        return [Document(page_content=full_text)]
    except Exception as e:
        msg = str(e)
        if "407" in msg or "ProxyError" in msg or "Tunnel connection failed" in msg:
            raise RuntimeError(
                "Transcript fetch failed due to a proxy authentication error (HTTP 407). "
            )
        raise RuntimeError(f"Transcript fetch failed! Exception: {e}")