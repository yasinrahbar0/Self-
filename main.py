import os
import asyncio
import threading
from flask import Flask
from telethon import TelegramClient, events

# ======= خواندن API و Session از محیط (Recommended) =======
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "session")

# ======= استایل‌ها =======
styles = {
    "bold": False,
    "italic": False
}

# ======= تابع اعمال استایل =======
def apply_styles(text):
    if styles["bold"]:
        text = f"**{text}**"
    if styles["italic"]:
        text = f"__{text}__"
    return text

# ======= Telethon Client =======
client = TelegramClient(SESSION, API_ID, API_HASH)

# ======= هندلر دستورات و پیام =======
@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text

    # ---- استایل‌ها ----
    if text.lower().startswith(".bold "):
        if "on" in text.lower():
            styles["bold"] = True
            await event.reply("✅ Bold روشن شد")
        elif "off" in text.lower():
            styles["bold"] = False
            await event.reply("❌ Bold خاموش شد")
        return

    if text.lower().startswith(".italic "):
        if "on" in text.lower():
            styles["italic"] = True
            await event.reply("✅ Italic روشن شد")
        elif "off" in text.lower():
            styles["italic"] = False
            await event.reply("❌ Italic خاموش شد")
        return

    # ---- ذخیره فایل ----
    if text.lower().startswith(".save") and event.is_reply:
        reply = await event.get_reply_message()
        if reply and reply.media:
            file_path = await client.download_media(reply)
            await client.send_file("me", file_path)
            await event.reply("✅ فایل ذخیره شد")
        else:
            await event.reply("❌ هیچ فایل معتبری برای ذخیره وجود ندارد")
        return

    # ---- ارسال متن با استایل ----
    if not text.startswith("."):
        styled_text = apply_styles(text)
        await event.respond(styled_text)

# ======= Flask برای نگه داشتن Web Service =======
app = Flask("")

@app.route("/")
def home():
    return "Bot is running ✅"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# اجرای Flask در Thread جدا
threading.Thread(target=run_flask).start()

# ======= اجرای سلف‌بات =======
print("سلف‌بات روشن شد...")
client.start()
asyncio.get_event_loop().run_forever()
