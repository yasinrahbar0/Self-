import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import InputPeerUser
from flask import Flask

# ====== تنظیمات ======
API_ID = 123456              # مقدار API_ID خودت
API_HASH = "YOUR_API_HASH"   # مقدار API_HASH خودت
SESSION_STRING = "YOUR_SESSION_STRING"  # Session string خودت

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ====== حالت‌های استایل ======
bold_mode = False
italic_mode = False
underline_mode = False

# ====== Flask ======
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running ✅"

# ====== دستورات سلف‌بات ======
@client.on(events.NewMessage(pattern=r"\.bold (on|off)"))
async def toggle_bold(event):
    global bold_mode
    state = event.pattern_match.group(1)
    bold_mode = True if state == "on" else False
    await event.reply(f"Bold mode is now {state.upper()} ✅")

@client.on(events.NewMessage(pattern=r"\.italic (on|off)"))
async def toggle_italic(event):
    global italic_mode
    state = event.pattern_match.group(1)
    italic_mode = True if state == "on" else False
    await event.reply(f"Italic mode is now {state.upper()} ✅")

@client.on(events.NewMessage(pattern=r"\.underline (on|off)"))
async def toggle_underline(event):
    global underline_mode
    state = event.pattern_match.group(1)
    underline_mode = True if state == "on" else False
    await event.reply(f"Underline mode is now {state.upper()} ✅")

# ====== فرمان دانلود فایل و ذخیره تو Saved Messages ======
@client.on(events.NewMessage(pattern=r"\.save"))
async def save_file(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        if msg.media:
            saved = await client.send_file("me", msg.media)
            await event.reply("File saved to Saved Messages ✅")
        else:
            await event.reply("Reply to a media file to save it ❌")
    else:
        await event.reply("You must reply to a media file ❌")

# ====== پردازش متن با استایل ======
@client.on(events.NewMessage)
async def style_text(event):
    text = event.raw_text
    if text.startswith("."):  # فقط دستورات مدیریت استایل
        return
    if bold_mode:
        text = f"**{text}**"
    if italic_mode:
        text = f"_{text}_"
    if underline_mode:
        text = f"__{text}__"
    await event.reply(text)

# ====== اجرای سلف‌بات و Flask ======
def run():
    loop = asyncio.get_event_loop()
    loop.create_task(client.start())
    loop.create_task(client.run_until_disconnected())
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run()
