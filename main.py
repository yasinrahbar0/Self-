import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ====== تنظیمات (Settings) ======
# Read from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

if not all([API_ID, API_HASH, SESSION]):
    raise ValueError("لطفاً API_ID، API_HASH و SESSION را در متغیرهای محیطی تنظیم کنید.")

API_ID = int(API_ID)

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# ====== وضعیت استایل‌ها (Styles State) ======
styles = {
    "bold": False,
    "italic": False
}

# ====== تابع اعمال استایل (Apply Style Function) ======
def apply_styles(text):
    if styles["bold"]:
        text = f"**{text}**"
    if styles["italic"]:
        text = f"__{text}__"
    return text

# ====== هندل کردن دستورات (Handle Commands) ======
@client.on(events.NewMessage)
async def handler(event):
    # فقط به پیام‌هایی که خودمان می‌فرستیم واکنش نشان می‌دهیم (Self-bot)
    if not event.out:
        return

    text = event.raw_text.lower()

    # ===== استایل‌ها (Styles) =====
    if text.startswith(".bold "):
        if "on" in text:
            styles["bold"] = True
            await event.reply("Bold روشن شد ✅")
        elif "off" in text:
            styles["bold"] = False
            await event.reply("Bold خاموش شد ❌")
        return

    if text.startswith(".italic "):
        if "on" in text:
            styles["italic"] = True
            await event.reply("Italic روشن شد ✅")
        elif "off" in text:
            styles["italic"] = False
            await event.reply("Italic خاموش شد ❌")
        return

    # ===== ذخیره فایل (Save File) =====
    if text.startswith(".save") and event.is_reply:
        reply = await event.get_reply_message()
        if reply and reply.media:
            file_path = await client.download_media(reply)
            await client.send_file("me", file_path)
            await event.reply("فایل ذخیره شد ✅")
        else:
            await event.reply("هیچ فایل معتبری برای ذخیره وجود ندارد ❌")
        return

    # ===== متن با استایل (Styled Text) =====
    if not text.startswith("."):
        styled_text = apply_styles(event.raw_text)
        if styled_text != event.raw_text:
            # برای جلوگیری از حلقه و بهبود تجربه کاربری، پیام را ویرایش می‌کنیم
            await event.edit(styled_text)

# ====== اجرا (Run) ======
async def main():
    print("سلف‌بات روشن شد...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
