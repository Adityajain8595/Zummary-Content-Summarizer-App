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
        proxy_url = os.getenv("PROXY_URL") or os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
        if proxy_url:
            os.environ["HTTPS_PROXY"] = proxy_url
            os.environ["HTTP_PROXY"] = proxy_url

        # youtube_transcript_api supports WebshareProxyConfig for Webshare proxy pools
        # If only username/password are provided, keep using WebshareProxyConfig.
        proxy_username = os.getenv("proxy_username")
        proxy_password = os.getenv("proxy_password")

        if proxy_username and proxy_password:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                proxies=WebshareProxyConfig(
                    proxy_username=proxy_username,
                    proxy_password=proxy_password,
                ).get_dict()
            )
        else:
            # Use get_transcript instead of fetch - it's the correct static method
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

        full_text = "\n".join([entry["text"] for entry in transcript])
        return [Document(page_content=full_text)]
    except Exception as e:
        # Detect common proxy auth errors and provide actionable guidance
        msg = str(e)
        if "407" in msg or "ProxyError" in msg or "Tunnel connection failed" in msg:
            raise RuntimeError(
                "Transcript fetch failed due to a proxy authentication error (HTTP 407). "
            )
        raise RuntimeError(f"Transcript fetch failed! Exception: {e}")