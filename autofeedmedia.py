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
