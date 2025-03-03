from pydailymotion import Dailymotion

# Dailymotion credentials
DAILYMO_USER = "your_dailymotion_username"
DAILYMO_PASS = "your_dailymotion_password"
DAILYMO_API_KEY = "your_dailymotion_api_key"
DAILYMO_API_SECRET = "your_dailymotion_api_secret"

# Initialize Dailymotion client
dailymotion = Dailymotion()
dailymotion.set_grant_type(
    'password',
    api_key=DAILYMO_API_KEY,
    api_secret=DAILYMO_API_SECRET,
    scope=['manage_videos'],
    info={'username': DAILYMO_USER, 'password': DAILYMO_PASS}
)

# Replace insta_client.clip_upload with Dailymotion upload logic
@app.on_message(filters.video)
async def upload_video(client, message):
    user_id = message.from_user.id
    try:
        language = get_language(user_id)
        video_path = await message.download()
        with open(CAPTION_FILE, "r", encoding="utf-8") as file:
            caption = file.read().strip()

        url = dailymotion.upload(video_path)
        dailymotion.post('/me/videos', {
            'url': url,
            'title': caption,
            'tags': 'your_tags'
        })

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
            
