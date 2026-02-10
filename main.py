import asyncio
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ====== ENV ======
API_ID = int("123456")              # بهتره از os.environ بگیری
API_HASH = "YOUR_API_HASH"
SESSION_STRING = "YOUR_SESSION_STRING"

# ====== Telegram ======
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

bold_mode = False
italic_mode = False
underline_mode = False

# ====== Flask ======
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running ✅"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# ====== Commands ======
@client.on(events.NewMessage(pattern=r"\.bold (on|off)"))
async def toggle_bold(event):
    global bold_mode
    bold_mode = event.pattern_match.group(1) == "on"
    await event.reply(f"Bold mode {'ON' if bold_mode else 'OFF'} ✅")

@client.on(events.NewMessage(pattern=r"\.italic (on|off)"))
async def toggle_italic(event):
    global italic_mode
    italic_mode = event.pattern_match.group(1) == "on"
    await event.reply(f"Italic mode {'ON' if italic_mode else 'OFF'} ✅")

@client.on(events.NewMessage(pattern=r"\.underline (on|off)"))
async def toggle_underline(event):
    global underline_mode
    underline_mode = event.pattern_match.group(1) == "on"
    await event.reply(f"Underline mode {'ON' if underline_mode else 'OFF'} ✅")

@client.on(events.NewMessage(pattern=r"\.save"))
async def save_file(event):
    if event.is_reply:
        msg = await event.get_reply_message()
        if msg.media:
            await client.send_file("me", msg.media)
            await event.reply("Saved to Saved Messages ✅")
        else:
            await event.reply("Reply to a media file ❌")

@client.on(events.NewMessage)
async def style_text(event):
    if not event.out:
        return
    text = event.raw_text
    if text.startswith("."):
        return

    if bold_mode:
        text = f"**{text}**"
    if italic_mode:
        text = f"_{text}_"
    if underline_mode:
        text = f"__{text}__"

    await event.edit(text)

# ====== Main ======
async def main():
    await client.start()
    print("Self bot started ✅")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(main())
