from pyrogram.types import InlineKeyboardButton
import config
from VILLAIN_MUSIC import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],  # ➕ Add Me
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],  # 💬 Support
                url=config.SUPPORT_CHAT
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],  # ➕ Add Me to Group
                url=f"https://t.me/{app.username}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"],  # 👤 Owner
                user_id=config.OWNER_ID
            ),
            InlineKeyboardButton(
                text="𝐒ᴜᴘᴘᴏʀᴛ 🍂",  # Fixed: static text, not language key
                url="https://t.me/KafkaSupport"
            ),
            InlineKeyboardButton(
                text=_["S_B_6"],  # 📢 Channel
                url=config.SUPPORT_CHANNEL
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],  # ⚙️ Commands / Help
                callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons
