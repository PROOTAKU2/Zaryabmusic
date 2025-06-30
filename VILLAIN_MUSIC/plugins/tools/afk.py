import time, re
from config import BOT_USERNAME
from pyrogram.enums import MessageEntityType
from pyrogram import filters
from pyrogram.types import Message
from VILLAIN_MUSIC import app
from VILLAIN_MUSIC.mongo.readable_time import get_readable_time
from VILLAIN_MUSIC.mongo.afkdb import add_afk, is_afk, remove_afk


@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return

    user = message.from_user
    user_id = user.id

    # If already AFK → remove AFK
    verifier, afk_data = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = afk_data["type"]
            timeafk = afk_data["time"]
            data = afk_data["data"]
            reasonafk = afk_data["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))

            caption = f"**{user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}"
            if reasonafk:
                caption += f"\n\nʀᴇᴀsᴏɴ: `{reasonafk}`"

            if afktype == "animation":
                await message.reply_animation(data, caption=caption)
            elif afktype == "photo":
                await message.reply_photo(photo=f"downloads/{user_id}.jpg", caption=caption)
            else:
                await message.reply_text(caption)

        except Exception:
            await message.reply_text(f"**{user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ")
        return

    # --- Now Set AFK ---
    details = {
        "type": "text",
        "time": time.time(),
        "data": None,
        "reason": None,
    }

    # =========== CASE 1: Just /afk ============
    if len(message.command) == 1 and not message.reply_to_message:
        pass  # Already default

    # =========== CASE 2: /afk [reason] ============
    elif len(message.command) > 1 and not message.reply_to_message:
        reason = (message.text.split(None, 1)[1].strip())[:100]

        # Block unwanted patterns (media/links/mentions)
        if re.search(r"@|https?://|\.com|\.in|t\.me|\.jpg|\.png|\.gif|\.mp4|\[.*\]\(.*\)", reason):
            await message.reply_text("❌ Only plain text is allowed in AFK reason.\nDon't send links, tags, or media.")
            return

        if message.entities:
            for entity in message.entities:
                if entity.type not in [MessageEntityType.BOLD, MessageEntityType.ITALIC, MessageEntityType.CODE, MessageEntityType.PRE]:
                    await message.reply_text("❌ Only plain text is allowed in AFK reason.\nFormatting or mentions are not supported.")
                    return

        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": reason,
        }

    # =========== CASE 3: /afk with replied animation ============
    elif message.reply_to_message and message.reply_to_message.animation:
        file_id = message.reply_to_message.animation.file_id
        if len(message.command) == 1:
            details = {
                "type": "animation",
                "time": time.time(),
                "data": file_id,
                "reason": None,
            }
        else:
            reason = (message.text.split(None, 1)[1].strip())[:100]
            if re.search(r"@|https?://|\.com|\.in|t\.me|\.jpg|\.png|\.gif|\.mp4|\[.*\]\(.*\)", reason):
                await message.reply_text("❌ Only plain text is allowed in AFK reason.\nDon't send links or mentions.")
                return
            details = {
                "type": "animation",
                "time": time.time(),
                "data": file_id,
                "reason": reason,
            }

    # =========== CASE 4: /afk with replied photo ============
    elif message.reply_to_message and message.reply_to_message.photo:
        await app.download_media(message.reply_to_message, file_name=f"{user_id}.jpg")
        if len(message.command) == 1:
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            reason = (message.text.split(None, 1)[1].strip())[:100]
            if re.search(r"@|https?://|\.com|\.in|t\.me|\.jpg|\.png|\.gif|\.mp4|\[.*\]\(.*\)", reason):
                await message.reply_text("❌ Only plain text is allowed in AFK reason.\nDon't send links or mentions.")
                return
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": reason,
            }

    # =========== CASE 5: Replied Sticker ============
    elif message.reply_to_message and message.reply_to_message.sticker:
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(message.reply_to_message, file_name=f"{user_id}.jpg")
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }

    # =========== Default fallback ============
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
    await message.reply_text(f"💤 {user.first_name} is now AFK!")
