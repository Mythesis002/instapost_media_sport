import requests
import re
import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
import time

ACCESS_TOKEN = "EAAWYAavlRa4BO8OE7Ho6gtx4a85DRgNMc59ZCpAdsHXNJnbZABREkXovZCKnbo9AlupOjbJ5xYSTBrMIMTVtu9n530I3ZC2JZBuZBpCDzHyjI7ngh8EtCrSvUho9VGZB9Xdxt5JLGNrHwfDsSIqtvxFjefG2t2JsgJpqfZAMCjO8AURp79mU0WAaLA7R"
INSTAGRAM_ACCOUNT_ID = "17841468918737662"

url = "https://ai-deepsearch.p.rapidapi.com/api/search"

payload = {
    "query": "Find the most viral, trending, and controversial news today that is making waves on social media in india. Focus on shocking events, celebrity controversies, bizarre incidents, and highly engaging content that people love. Prioritize news from Instagram, Twitter, and YouTube trends, ensuring it's eye-catching and has maximum engagement. Format the response as follows: \n\n**Headline:** [Insert eye-catching headline]\n\n**Summary:** [Provide a concise summary explaining why it's viral, using engaging storytelling]\n\n**Music:** [Suggest a currently trending music title in India (only the music title, nothing else) that aligns with the mood of the news, based on viral Instagram trends in India. Respond in this format: Music: [song title].]\n\nEnsure the response is structured exactly in this format."
}
headers = {
    "x-rapidapi-key": "628e474f5amsh0457d8f1b4fb50cp16b75cjsn70408f276e9b",
    "x-rapidapi-host": "ai-deepsearch.p.rapidapi.com",
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    response_data = response.json()

    # Extract the result data
    result_data = response_data.get("result")

    # Check if result_data is a dictionary or a string
    if isinstance(result_data, dict):
        headline = result_data.get("Headline", "No headline found").strip()
        summary = result_data.get("Summary", "No summary found").strip()
        music = result_data.get("Music", "No music found").strip()

        print("Headline:", headline)
        print("Summary:", summary)
        print("Music:", music)

    elif isinstance(result_data, str):
        # If it's a string, assume it contains the entire response
        # and try to extract information using regex

        # Improved regex patterns to handle variations in the response format
        headline_match = re.search(r"Headline:\s*(.+?)\n", result_data)
        summary_match = re.search(r"Summary:\s*(.+?)\n", result_data, re.DOTALL)
        music_match = re.search(r"Music:\s*(.+?)\n", result_data)

        headline = headline_match.group(1).strip() if headline_match else "No headline found"
        summary = summary_match.group(1).strip() if summary_match else "No summary found"
        music = music_match.group(1).strip() if music_match else "No music found"

        print("Headline:", headline)
        print("Summary:", summary)
        print("Music:", music)

    else:
        print("Unexpected data type for 'result':", type(result_data))
        print("Raw response data:", response_data)  # Print for debugging
        headline, summary, music = "No headline found", "No summary found", "No music found"

except requests.exceptions.RequestException as e:
    print("Error:", e)
    headline, summary, music = "No headline found", "No summary found", "No music found"

url = "https://rocketapi-for-developers.p.rapidapi.com/instagram/audio/search"

payload = { "query": music}
headers = {
	"x-rapidapi-key": "628e474f5amsh0457d8f1b4fb50cp16b75cjsn70408f276e9b",
	"x-rapidapi-host": "rocketapi-for-developers.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)

    # Checking if "response" and "body" exist in JSON
    if "response" in data and "body" in data["response"] and "audios" in data["response"]["body"]:
        audios = data["response"]["body"]["audios"]
        # Check if 'audios' is not empty before accessing elements
        if audios:  
            first_audio_url = audios[0].get("fast_start_progressive_download_url", "URL Not Found")
            print("Fast Start Progressive Download URL:", first_audio_url)
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
            print("❌ Error: The 'audios' list is empty. No audio URL found.") 
    else:
        print("Error: Unexpected JSON structure. 'response', 'body', or 'audios' not found.")
else:
    print("Error fetching data:", response.status_code)
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
      {"overlay": f"audio:{music_public_id}", "start_offset": "45", "duration": "15"},
      {'flags': "layer_apply"},
      {'width': 500, 'crop': "scale"},

        # Corrected text overlay parameters
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
