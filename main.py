import requests
from pyrogram import Client, filters  # Ensure you have imported the necessary modules

# Initialize the app object
app = Client("my_account", api_id=21572824, api_hash="cc88cfb3d1cc2d0c9baea879e0fc62b0", bot_token="7317390308:AAHFIilw1zu5kW1FkYFx70i09PuVAIAU__s")

# Dailymotion credentials
DAILYMO_USER = "akabarbabar8@gmail.com"
DAILYMO_PASS = "AYUSHRA5354N@"
DAILYMO_API_KEY = "4b8ebba0a67b86ead065"
DAILYMO_API_SECRET = "df6256d39ab33634919703751e792b9eda135087"

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
    response.raise_for_status()
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
        upload_response.raise_for_status()
        upload_link = upload_response.json().get('upload_url')

        with open(video_path, 'rb') as video_file:
            files = {'file': video_file}
            video_response = requests.post(upload_link, files=files)
            video_response.raise_for_status()
        video_url = video_response.json().get('url')

        # Post the video
        post_url = "https://api.dailymotion.com/me/videos"
        post_data = {
            'url': video_url,
            'title': caption,
            'tags': 'your_tags'
        }
        post_response = requests.post(post_url, headers=headers, data=post_data)
        post_response.raise_for_status()

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

# Run the app
app.run()
