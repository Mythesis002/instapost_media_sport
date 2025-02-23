import requests
import re
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont
import cloudinary
import cloudinary.uploader
import cloudinary.api
import io
import numpy as np
import os
import time
import schedule
import datetime
import base64



# 🔹 Instagram Credentials
ACCESS_TOKEN = "EAAWYAavlRa4BO8OE7Ho6gtx4a85DRgNMc59ZCpAdsHXNJnbZABREkXovZCKnbo9AlupOjbJ5xYSTBrMIMTVtu9n530I3ZC2JZBuZBpCDzHyjI7ngh8EtCrSvUho9VGZB9Xdxt5JLGNrHwfDsSIqtvxFjefG2t2JsgJpqfZAMCjO8AURp79mU0WAaLA7R"
INSTAGRAM_ACCOUNT_ID = "17841468918737662"
INSTAGRAM_NICHE_ACCOUNT = "thetrendingindian"

def post_reel():
    """Uploads and posts an Instagram Reel automatically."""
    print(f"📅 Running at: {datetime.datetime.now()}")

    # 🔹 1. Get Instagram Caption
    url = "https://instagram230.p.rapidapi.com/user/posts"
    querystring = {"username": INSTAGRAM_NICHE_ACCOUNT}
    headers = {
        "x-rapidapi-key": "c66b66fd5fmsh2d1f2d4c5d0a073p17161ajsnb75f8dbbac1d",
        "x-rapidapi-host": "instagram230.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        # Check if 'items' is in data and it's not empty before accessing its elements
        if 'items' in data and data['items'] and isinstance(data['items'], list) and len(data['items']) > 0:
            # Access the caption text from the first item in the 'items' list
            caption_text = data['items'][0]['caption']['text']

            # Check if 'music_metadata' and 'music_canonical_id' exist
            if 'music_metadata' in data['items'][0] and data['items'][0]['music_metadata'] and 'music_canonical_id' in data['items'][0]['music_metadata']:
                music_canonical_id = data['items'][0]['music_metadata']['music_canonical_id']
            else:
                # Use the default ID if 'music_canonical_id' is missing or invalid
                music_canonical_id = "18149596924049565"

                print("Music Canonical ID:", music_canonical_id)
        else:
            # Handle the case where the expected structure is not found
            print("Error: Unexpected response structure or empty 'items' list.")
            print(data)  # Print the response for debugging
            return
        url = "https://instagram-scraper-api2.p.rapidapi.com/v1/audio_info"

        querystring = {"audio_canonical_id":music_canonical_id}

        headers = {
         	"x-rapidapi-key": "c4149d7f42msh169b1ac1d7c079ep17cebfjsn882b5a92dacd",
	        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        print(response.json())
        music_url = data['data']['download_url']
        print(music_url)
        cloudinary.config(
                cloud_name="dkr5qwdjd",
                api_key="797349366477678",
                api_secret="9HUrfG_i566NzrCZUVxKyCHTG9U"
            )
        upload_result = cloudinary.uploader.upload(music_url, resource_type="video")

    # 🔹 Print Public ID
        music_public_id = upload_result.get("public_id")
        print(f"✅ Uploaded Successfully! Public ID: {music_public_id}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch Instagram caption: {e}")

    # 🔹 2. Generate Headline & Image Prompt
    url = "https://chatgpt-42.p.rapidapi.com/gpt4"
    payload = {
        "messages": [
            {
                "role": "system",
                "content":
                "You are an AI assistant that specializes in generating high-quality Instagram post elements. "
                "For any given caption, you must return:\n"
                "1️⃣ **Keywords for Image Search**: A sentence of  5-7 words for searching images/videos about that event\n"
                "2️⃣ **Summarized Caption**: A concise and engaging summary of the caption in at least 2 line.\n\n"
                "Format your response **exactly** like this:\n"
                "**Keywords:** a shortest 5 word sentense \n"
                "**Summary:** Your concise and engaging summary here"
            },
            {
                "role": "user",
                "content": caption_text
            }
        ],
        "web_access": False
    }

    headers = {
        "x-rapidapi-key": "c66b66fd5fmsh2d1f2d4c5d0a073p17161ajsnb75f8dbbac1d",
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()

        # Extract the result text
        result_text = response_data.get("result", "").strip()

        # Define regex patterns to extract keywords and summary
        keywords_pattern = r'\*\*Keywords:\*\*\s*(.+)'
        summary_pattern = r'\*\*Summary:\*\*\s*(.+)'

        # Extract keywords and summary
        keywords_match = re.search(keywords_pattern, result_text)
        summary_match = re.search(summary_pattern, result_text, re.DOTALL)

        keywords = keywords_match.group(1).strip().split(", ") if keywords_match else []
        summary = summary_match.group(1).strip() if summary_match else "No summary found"

        # Print the results
        print("Keywords:", keywords)
        print("Summary:", summary)

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to generate keywords and summary: {e}")
        return

    # 🔹 3. Search for Images Using Keywords
    url = "https://google-api-unlimited.p.rapidapi.com/google/image"
    payload = {
        "query": " ".join(keywords),  # Use the extracted keywords for the search
        "num_images": "1",  # Fetch only 1 image for simplicity
        "lang": "en",
        "region": "IN"
    }
    headers = {
        "x-rapidapi-key": "c4149d7f42msh169b1ac1d7c079ep17cebfjsn882b5a92dacd",
        "x-rapidapi-host": "google-api-unlimited.p.rapidapi.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        image_data_list = response.json()  # Assuming the response is a list

        if image_data_list and 'image' in image_data_list[0]:  # Check if list is not empty and has 'image' key
            # Extract the base64 image data
            base64_data = image_data_list[0]['image'].split(',')[1]

            # Decode the base64 string into binary data
            image_data = base64.b64decode(base64_data)

            # Upload image to Cloudinary
            cloudinary.config(
                cloud_name="dkr5qwdjd",
                api_key="797349366477678",
                api_secret="9HUrfG_i566NzrCZUVxKyCHTG9U"
            )
            upload_result = cloudinary.uploader.upload(image_data, folder="Mythesis_images")

            # Get image URL from Cloudinary
            public_id = upload_result["public_id"].replace("/", ":")
            print("✅ Image URL:", public_id)

        else:
            print("❌ Error: 'image' key not found in the response or response list is empty.")
            return



    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to search for images: {e}")
        return
    music_id = music_public_id  # Removed the trailing comma

    video_url = cloudinary.CloudinaryVideo("bgvideo").video(transformation=[
        {'overlay': "black_bg_9_16"},
        {'flags': "layer_apply", 'width': 2200, 'crop': "fit"},
        {'overlay': public_id},
        {'flags': "layer_apply", 'width': 1920, 'crop': "fit"},
        {"overlay": f"audio:{music_id}", "start_offset": "40", "duration": "15"},
        {'flags': "layer_apply"},
        {'width': 500, 'crop': "scale"},
        # Corrected text overlay parameters
        {'overlay': {'font_family': "arial", 'font_size': 18, 'font_weight': "bold", 'text': summary}, 'color': "white", 'background': "black", 'width': 400, 'crop': "fit"},
        {'flags': "layer_apply", 'gravity': "north", 'y': 500},
        {'overlay': {'font_family': "arial", 'font_size': 20, 'font_weight': "bold", 'text': "autoFeed_tech"}, 'color': "black", 'background': "skyblue", 'radius': 20, 'x': 20, 'y': 20, 'width': 400, 'crop': "fit"},
        {'flags': "layer_apply", 'gravity': "north", 'y': 110},
        {'overlay': {'font_family': "arial", 'font_size': 12, 'font_weight': "bold", 'text': "This page is totally handled by ai, which provides trending tech news faster than human!"}, 'color': "white", 'width': 300, 'crop': "fit"},
        {'flags': "layer_apply", 'gravity': "north", 'y': 160},
        {'overlay': {'font_family': "arial", 'font_size': 12, 'font_weight': "bold", 'text': "full details in caption"}, 'color': "white", 'width': 300, 'crop': "fit"},
        {'flags': "layer_apply", 'gravity': "south", 'y': 150}
    ])

    match = re.search(r'/webm"><source src="(.*\.mp4)"', str(video_url))
    mp4_url = match.group(1)
    print(mp4_url)
    upload_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "video_url": mp4_url,
        "caption": caption_text,
        "media_type": "REELS",
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
post_reel()





