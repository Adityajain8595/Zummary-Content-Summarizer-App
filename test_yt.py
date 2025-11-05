from youtube_transcript_api import YouTubeTranscriptApi

# Test video (use any YouTube video ID)
video_id = "dQw4w9WgXcQ"  # This is the "Never Gonna Give You Up" video

try:
    # Method 1
    print("Trying method 1...")
    transcript = YouTubeTranscriptApi().get_transcript(video_id)
    print("Method 1 succeeded!")
except Exception as e:
    print(f"Method 1 failed: {str(e)}")

try:
    # Method 2
    print("\nTrying method 2...")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print("Method 2 succeeded!")
except Exception as e:
    print(f"Method 2 failed: {str(e)}")

try:
    # Method 3
    print("\nTrying method 3...")
    transcripts = YouTubeTranscriptApi().get_transcripts([video_id])[0]
    print("Method 3 succeeded!")
except Exception as e:
    print(f"Method 3 failed: {str(e)}")