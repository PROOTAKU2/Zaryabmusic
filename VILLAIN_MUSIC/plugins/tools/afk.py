from pyrogram.enums import MessageEntityType
import re, time
from config import BOT_USERNAME
from VILLAIN_MUSIC import app
from VILLAIN_MUSIC.mongo.afkdb import is_afk, remove_afk
from VILLAIN_MUSIC.mongo.readable_time import get_readable_time
from pyrogram import filters

@app.on_message(~filters.me & ~filters.bot & ~filters.via_bot, group=1)
async def chat_watcher_func(_, message):
    if message.sender_chat or not message.from_user:
        return

    userid = message.from_user.id
    user_name = message.from_user.first_name

    # === RETURN FROM AFK ===
    verifier, afk_data = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            timeafk = afk_data["time"]
            reason = afk_data.get("reason")
            seenago = get_readable_time(int(time.time() - timeafk))

            return_msg = (
                f"**{user_name}** 𝗂𝗌 𝗇𝗈𝗐 𝖻𝖺𝖼𝗄 𝗈𝗇𝗅𝗂𝗇𝖾!\n\n"
                f"🕓 𝖶𝖺𝗌 𝖠𝖥𝖪 𝖿𝗈𝗋: {seenago}"
            )
            if reason:
                return_msg += f"\n\n📌 𝖱𝖾𝖺𝗌𝗈𝗇: `{reason}`"

            await message.reply_text(return_msg)
        except:
            await message.reply_text(f"**{user_name}** 𝗂𝗌 𝗇𝗈𝗐 𝖻𝖺𝖼𝗄 𝗈𝗇𝗅𝗂𝗇𝖾!")

    # === CHECK REPLIED USER ===
    msg = ""
    replied_user_id = 0

    if message.reply_to_message and message.reply_to_message.from_user:
        try:
            replied_user = message.reply_to_message.from_user
            replied_first = replied_user.first_name
            replied_user_id = replied_user.id
            verifier, data = await is_afk(replied_user_id)
            if verifier:
                timeafk = data["time"]
                reason = data.get("reason")
                seenago = get_readable_time(int(time.time() - timeafk))

                afkmsg = f"**{replied_first[:25]}** 𝗂𝗌 𝖠𝖥𝖪 𝗌𝗂𝗇𝖼𝖾 {seenago}"
                if reason:
                    afkmsg += f"\n\n📌 𝖱𝖾𝖺𝗌𝗈𝗇: `{reason}`"

                msg += afkmsg + "\n\n"
        except:
            pass

    # === CHECK MENTIONS & TEXT MENTIONS ===
    if message.entities:
        message_text = message.text or message.caption or ""
        for entity in message.entities:
            if entity.type == MessageEntityType.MENTION:
                try:
                    username = message_text[entity.offset + 1: entity.offset + entity.length]
                    user = await app.get_users(username)
                    if user.id == replied_user_id:
                        continue
                    verifier, data = await is_afk(user.id)
                    if verifier:
                        timeafk = data["time"]
                        reason = data.get("reason")
                        seenago = get_readable_time(int(time.time() - timeafk))
                        afkmsg = f"**{user.first_name[:25]}** 𝗂𝗌 𝖠𝖥𝖪 𝗌𝗂𝗇𝖼𝖾 {seenago}"
                        if reason:
                            afkmsg += f"\n\n📌 𝖱𝖾𝖺𝗌𝗈𝗇: `{reason}`"
                        msg += afkmsg + "\n\n"
                except:
                    continue

            elif entity.type == MessageEntityType.TEXT_MENTION:
                try:
                    user = entity.user
                    if user.id == replied_user_id:
                        continue
                    verifier, data = await is_afk(user.id)
                    if verifier:
                        timeafk = data["time"]
                        reason = data.get("reason")
                        seenago = get_readable_time(int(time.time() - timeafk))
                        afkmsg = f"**{user.first_name[:25]}** 𝗂𝗌 𝖠𝖥𝖪 𝗌𝗂𝗇𝖼𝖾 {seenago}"
                        if reason:
                            afkmsg += f"\n\n📌 𝖱𝖾𝖺𝗌𝗈𝗇: `{reason}`"
                        msg += afkmsg + "\n\n"
                except:
                    continue

    if msg.strip():
        try:
            await message.reply_text(msg.strip(), disable_web_page_preview=True)
        except:
            pass
