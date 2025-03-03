import requests

# Dailymotion credentials
DAILYMO_USER = "your_dailymotion_username"
DAILYMO_PASS = "your_dailymotion_password"
DAILYMO_API_KEY = "your_dailymotion_api_key"
DAILYMO_API_SECRET = "your_dailymotion_api_secret"

# Function to get Dailymotion access token
def get_dailymotion_token():
    url = "https://api.dailymotion.com/oauth/token"
    data = {
        'grant_type': 'password',
        'client_id': DAILYMO_API_KEY,
        'client_secret': DAILYMO_API_SECRET,
        'username': DAILYMO_USER,
        'password': DAILYMO_PASS,
        'scope': 'manage_videos'
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')

# Replace the upload logic
@app.on_message(filters.video)
async def upload_video(client, message):
    user_id = message.from_user.id
    try:
        language = get_language(user_id)
        video_path = await message.download()
        with open(CAPTION_FILE, "r", encoding="utf-8") as file:
            caption = file.read().strip()

        token = get_dailymotion_token()
        headers = {'Authorization': f'Bearer {token}'}

        # Upload the video
        upload_url = "https://api.dailymotion.com/file/upload"
        upload_response = requests.post(upload_url, headers=headers)
        upload_link = upload_response.json().get('upload_url')

        with open(video_path, 'rb') as video_file:
            files = {'file': video_file}
            video_response = requests.post(upload_link, files=files)
            video_url = video_response.json().get('url')

        # Post the video
        post_url = "https://api.dailymotion.com/me/videos"
        post_data = {
            'url': video_url,
            'title': caption,
            'tags': 'your_tags'
        }
        requests.post(post_url, headers=headers, data=post_data)

        if language == "fa":
            await message.reply("✅ ویدیو با موفقیت در Dailymotion آپلود شد.")
        else:
            await message.reply("✅ The video was successfully uploaded to Dailymotion.")
        await asyncio.sleep(30)
    except Exception as e:
        if language == "fa":
            await message.reply(f"⚠️ خطا: {e}")
        else:
            await message.reply(f"⚠️ Error: {e}")
            
