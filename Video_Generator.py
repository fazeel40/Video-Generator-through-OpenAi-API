import re
import os
import openai
import urllib.request
from gtts import gTTS
from moviepy.editor import *
from moviepy.config import change_settings

# Specify the ImageMagick path
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\convert"})

key = "Your OpenAI API KEY"
openai.api_key = key

with open(r"D:\\Programming\\Python Files\\Python Projects\\Video Generator\\generated.txt", "r") as f:
    text = f.read()

paragraph = re.split(r"[,.]", text)

os.makedirs("audio", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("video", exist_ok=True)

i = 1
clips = []
for para in paragraph[:-1]:
    response = openai.Image.create(prompt=para.strip(), n=1, size="1024x1024")
    print("Generate New Ai Image From Paragraph...")
    image_url = response['data'][0]['url']
    urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")
    print("Generated Images Saved Img Folder.")

    tts = gTTS(text=para, lang="en", slow=False)
    tts.save(f"audio/voiceover{i}.mp3")
    print("Paragraphs Converted In VoiceOver and Saved In Audio Folder...")

    print("Extract VoiceOver And Get Duration...")

    audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
    audio_duration = audio_clip.duration

    image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)

    print("Customize the text clip...")

    text_clip = TextClip(para, fontsize=30, color="black")
    text_clip = text_clip.set_pos('center').set_duration(audio_duration)

    print("Concatenate Images, Audio and Text to create Final Video")
    clip = image_clip.set_audio(audio_clip)
    video = CompositeVideoClip([clip, text_clip])
    clips.append(video)
    print(f"The Video{i} has been created successfully.")
    i += 1

print("Concatenate all the clips to the final video")
final_video = concatenate_videoclips(clips, method="compose")
final_video.fps = 24  # Set the frames per second for the final video
final_video.write_videofile("final_video.mp4")
print("Final Video Has Been Created!")