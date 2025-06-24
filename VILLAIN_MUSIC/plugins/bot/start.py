import time
import random
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    InputMediaPhoto,
)
from youtubesearchpython.__future__ import VideosSearch

import config
from VILLAIN_MUSIC import app
from VILLAIN_MUSIC.misc import _boot_
from VILLAIN_MUSIC.plugins.sudo.sudoers import sudoers_list
from VILLAIN_MUSIC.utils.database import (
    get_served_chats,
    get_served_users,
    get_sudoers,
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from VILLAIN_MUSIC.utils.decorators.language import LanguageStart
from VILLAIN_MUSIC.utils.formatters import get_readable_time
from VILLAIN_MUSIC.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# Banner Image/Video
NEXI_VID = ["https://files.catbox.moe/luxd67.jpg"]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_video(
                random.choice(NEXI_VID),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                         f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                         f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return

        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)

            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ]
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                         f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                         f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )

    # Default /start (no parameters)
    out = private_panel(_)
    await message.reply_video(
        random.choice(NEXI_VID),
        caption=f"""
𝖧𝖾𝗅𝗅𝗈, {message.from_user.mention} 🎧  
➻ 𝖬𝗒𝗌𝖾𝗅𝖿 𝐏ᴏᴏᴋɪᴇ ✗ 𝐌ᴜsɪᴄ 🎶!  
𝖳𝗁𝖾 𝖬𝗈𝗌𝗍 𝖯𝗈𝗐𝖾𝗋𝖿𝗎𝗅 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖬𝗎𝗌𝗂𝖼 𝖡𝗈𝗍 𝖶𝗂𝗍𝗁 𝖠𝗐𝖾𝗌𝗈𝗆𝖾 𝖠𝗎𝖽𝗂𝗈 𝖺𝗇𝖽 𝖵𝗂𝖽𝖾𝗈 𝖲𝗍𝗋𝖾𝖺𝗆𝗂𝗇𝗀 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌.  
──────────────────────!

✨ 𝖶𝗁𝖺𝗍 𝖨 𝖢𝖺𝗇 𝖣𝗈:  
 • 𝖲𝗆𝗈𝗈𝗍𝗁 𝖫𝗂𝗏𝖾 𝖬𝗎𝗌𝗂𝖼 & 𝖵𝗂𝖽𝖾𝗈 𝖯𝗅𝖺𝗒𝗂𝗇𝗀  
 • 𝖲𝗎𝗉𝖾𝗋 𝖥𝖺𝗌𝗍 𝖰𝗎𝖾𝗎𝖾 & 𝖲𝗍𝗋𝖾𝖺𝗆 𝖢𝗈𝗇𝗍𝗋𝗈𝗅𝗌  
 • 𝖥𝗎𝗇 𝖠𝗎𝗍𝗈 𝖯𝗅𝖺𝗒𝗅𝗂𝗌𝗍 & 𝖢𝗎𝗌𝗍𝗈𝗆 𝖲𝗈𝗎𝗇𝖽𝖿𝗑  

📚 𝖭𝖾𝖾𝖽 𝖧𝖾𝗅𝗉?  
𝖢𝗅𝗂𝖼𝗄 𝗍𝗁𝖾 𝖧𝖾𝗅𝗉 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗀𝖾𝗍 𝖺𝗅𝗅 𝗍𝗁𝖾 𝖽𝖾𝗍𝖺𝗂𝗅𝗌 𝗈𝗇 𝗆𝗒 𝖬𝗎𝗌𝗂𝖼 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝖺𝗇𝖽 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌.
""",
        reply_markup=InlineKeyboardMarkup(out),
    )

    if await is_on_off(2):
        return await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                 f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                 f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_video(
        random.choice(NEXI_VID),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_video(
                    random.choice(NEXI_VID),
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
