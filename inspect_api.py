from youtube_transcript_api import YouTubeTranscriptApi
import inspect

# Print all available methods
print("Available methods:")
for method in dir(YouTubeTranscriptApi):
    if not method.startswith('_'):  # Skip private methods
        print(f"- {method}")

# Print the module path
print("\nModule location:")
print(YouTubeTranscriptApi.__module__)

# Create an instance and check its methods
print("\nInstance methods:")
instance = YouTubeTranscriptApi()
for method in dir(instance):
    if not method.startswith('_'):  # Skip private methods
        print(f"- {method}")