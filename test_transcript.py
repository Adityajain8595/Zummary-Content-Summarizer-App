from youtube_transcript_api import YouTubeTranscriptApi

def test_transcript():
    # Rick Astley - Never Gonna Give You Up (test video)
    video_id = "dQw4w9WgXcQ"
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print("Success! Transcript received.")
        print("First few lines:")
        for line in transcript[:3]:
            print(line['text'])
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_transcript()