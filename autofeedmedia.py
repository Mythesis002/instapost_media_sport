import requests
import re
import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
import time

ACCESS_TOKEN = "EAAWYAavlRa4BO8OE7Ho6gtx4a85DRgNMc59ZCpAdsHXNJnbZABREkXovZCKnbo9AlupOjbJ5xYSTBrMIMTVtu9n530I3ZC2JZBuZBpCDzHyjI7ngh8EtCrSvUho9VGZB9Xdxt5JLGNrHwfDsSIqtvxFjefG2t2JsgJpqfZAMCjO8AURp79mU0WAaLA7R"
INSTAGRAM_ACCOUNT_ID = "17841468918737662"

# ✅ Step 2: Generate Audio using ElevenLabs
API_VOICE_KEY = "sk_dd5aedf32fb7898bf883a90f8a0b65c0c1f3c9c9076ff6e7"
VOICE_ID = "rvfywjas3inawggBGTqH"

url = "https://ai-deepsearch.p.rapidapi.com/api/search"

payload = {
    "query": "Find the most viral, trending, and controversial news today that is making waves on social media in India. Focus on shocking events, celebrity controversies, bizarre incidents, and highly engaging content that people love. Prioritize news from Instagram, Twitter, and YouTube trends, ensuring it's eye-catching and has maximum engagement. Format the response as follows: Headline: [Insert an eye-catching, bold, or sensational headline] Summary: [Provide a concise, punchy summary in Hindi, written in Varun Mayya’s style—casual, witty, and loaded with Gen-Z slang, emojis, and dramatic flair. Example: 'so,IT इंडस्ट्री में भूचाल आने वाला है!'] Music: [Suggest a currently trending music title in India (only the song name) that fits the mood of the news, based on viral Instagram/Reels trends. Format: Music: [song title].] Ensure the response is structured exactly like this, with the Hindi summary mimicking Varun Mayya’s tone—relatable, humorous, and attention-grabbing."
}
headers = {
    "x-rapidapi-key": "c4149d7f42msh169b1ac1d7c079ep17cebfjsn882b5a92dacd",
    "x-rapidapi-host": "ai-deepsearch.p.rapidapi.com",
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    response_data = response.json()

    # Extract result string directly
    result_string = response_data.get("result", "")

    # Extract headline, summary, and music using regex
    headline_match = re.search(r"Headline:\s*(.*?)\n", result_string)
    summary_match = re.search(r"Summary:\s*(.*?)\n", result_string, re.DOTALL)
    music_match = re.search(r"Music:\s*(.*?)(?=\n|$)", result_string)

    # Remove any unwanted `**` or extra formatting around the result
    headline = headline_match.group(1).strip().replace('**', '') if headline_match else "No headline found"
    summary = summary_match.group(1).strip().replace('**', '') if summary_match else "No summary found"
    music = music_match.group(1).strip().replace('**', '') if music_match else "No music found"

    print("Headline:", headline)
    print("Summary:", summary)
    print("Music:", music)

except requests.exceptions.RequestException as e:
    print("Error:", e)

url = "https://real-time-instagram-scraper-api1.p.rapidapi.com/v1/search_music"

querystring = {"search_query": music}

headers = {
    "x-rapidapi-key": "c4149d7f42msh169b1ac1d7c079ep17cebfjsn882b5a92dacd",
    "x-rapidapi-host": "real-time-instagram-scraper-api1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()

    # Check if the 'data' list is not empty before accessing elements
    if data.get("data", []):
        first_track = data.get("data", [])[0].get("track", {})
        first_audio_url = first_track.get("fast_start_progressive_download_url")
        print(first_audio_url)
        cloudinary.config(
                    cloud_name="dkr5qwdjd",
                    api_key="797349366477678",
                    api_secret="9HUrfG_i566NzrCZUVxKyCHTG9U"
        )
        upload_result = cloudinary.uploader.upload(first_audio_url, resource_type="video")

                # 🔹 Print Public ID
        music_public_id = upload_result.get("public_id")
        print(f"✅ Uploaded Successfully! Public ID: {music_public_id}")
    else:
        print("No matching music found.")  # Handle the case where the list is empty
else:
    print("Error:", response.status_code, response.text)
# Extract only the first 5 words from the headline
url = "https://google-search72.p.rapidapi.com/imagesearch"

querystring = {"q": headline, "gl": "in", "lr": "lang_en", "num": "1", "start": "0"}

headers = {
    "x-rapidapi-key": "628e474f5amsh0457d8f1b4fb50cp16b75cjsn70408f276e9b",
    "x-rapidapi-host": "google-search72.p.rapidapi.com"
}

try:
    response = requests.get(url, params=querystring, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes

    image_data_list = response.json().get("items", [])  # Extract "items" safely

    if image_data_list and "thumbnailImageUrl" in image_data_list[0]:
        # Extract the thumbnail image URL
        thumbnail_url = image_data_list[0]["thumbnailImageUrl"]
        print("✅ Thumbnail Image URL:", thumbnail_url)

        # Upload image to Cloudinary
        cloudinary.config(
            cloud_name="dkr5qwdjd",
            api_key="797349366477678",
            api_secret="9HUrfG_i566NzrCZUVxKyCHTG9U"
        )
        upload_result = cloudinary.uploader.upload(thumbnail_url, folder="Mythesis_images")

        # Get image URL from Cloudinary
        public_id = upload_result.get("public_id", "").replace("/", ":")
        print("✅ Uploaded Image URL:", public_id)

    else:
        print("❌ Error: 'thumbnailImageUrl' key not found in the response or response list is empty.")
        thumbnail_url = None

except requests.exceptions.RequestException as e:
    print(f"❌ Failed to search for images: {e}")
    thumbnail_url = None

# VOICE GENERATION
summar = summary;

headers = {
    "xi-api-key": API_VOICE_KEY,
    "Content-Type": "application/json"
}

data = {
    "text": summar,
    "voice_settings": {
        "speed": 1.2,
        "stability": 0.3,
        "similarity_boost": 0.8,
        "style_exaggeration": 0.7
      
    },
    "model_id": "eleven_multilingual_v2",
    "output_format": "mp3"
}

response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}", headers=headers, json=data)

if response.status_code == 200:
    print("✅ Audio Generated Successfully!")

    # ✅ Step 3: Upload Audio Directly to Cloudinary
    audio_file = response.content  # Get audio content

    upload_response = cloudinary.uploader.upload(
        file=audio_file,
        resource_type="video",  # Cloudinary treats audio files as "video"
        format="mp3",
    )
    cloudinary_url = upload_response["secure_url"]
    cloudinary_public_id = upload_response["public_id"]

    print(f"🌍 Cloudinary URL: {cloudinary_url}")
    print(f"📂 Cloudinary Public ID: {cloudinary_public_id}")
else:
    print("❌ Error Generating Audio:", response.text)


video_url = cloudinary.CloudinaryVideo("bgvideo1").video(transformation=[
    # Main Image Overlay (Product/Feature Image)
      {
      'overlay': public_id,
      'width': 400,
      'height': 400,
      'crop': "pad",
      'y': 130,
      'background': "#000000", 'gravity': "north"
      },
      {'background': "#000000", 'gravity': "north", 'height': 1920, 'width': 1080, 'crop': "pad"},
      {'effect': "gradient_fade:symmetric_pad", 'x': "0.5"},
      {'effect': 'gen_restore'},
      {'effect': "fade:2000"},
      {
      'flags': "layer_apply",
      'width': 1080,
      'crop': "pad",
      'gravity': "center",
      'y': -130  # Moves image 100 pixels up
      },
      
      {"overlay": f"audio:{cloudinary_public_id}",  "duration": "30"}, 
      {'effect':"volume:100"}, 
      {'flags': "layer_apply"},
      {'width': 500, 'crop': "scale"},
     
      {"overlay": f"audio:{music_public_id}", "start_offset": "45", "duration": "30"},
      {'effect':"volume:-85"},
      {'flags': "layer_apply"},
      {'width': 500, 'crop': "scale"},

      {
      'overlay': {
      'font_family': "georgia",
      'font_weight': "bold",
      'font_size': 30,
      'gravity': "center",
      'y': -30,
      'text_align': "center",
      'text': headline
      },
      'color': "white",
      'effect': "fade:2000",
      'text_align': "center",
      'width': 450,
      'crop': "fit",
      'gravity': "center",
      'y': 100,# Align text to the center
      }
    ])

match = re.search(r'/webm"><source src="(.*\.mp4)"', str(video_url))
mp4_url = match.group(1)
print(mp4_url)
upload_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
payload = {
        "video_url": mp4_url,
        "caption": summary,
        "media_type": "REELS",
	      "audio_name": "S.T.A.Y.",
        "access_token": ACCESS_TOKEN
    }

response = requests.post(upload_url, data=payload)
response_data = response.json()
print(response_data)

media_id = response_data.get("id")
print(media_id)

if media_id:
        print("⏳ Waiting for Instagram to process the video...")
        time.sleep(140)

        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_payload = {
            "creation_id": media_id,
            "access_token": ACCESS_TOKEN
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        print("✅ Reel Uploaded Successfully!", publish_response.json())
else:
        print("❌ Error: Failed to upload the video.")
