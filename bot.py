from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

import urllib.parse

BOT_TOKEN = "8906062129:AAEZZXSCkkbRjSFU-Z7aBQHGtJ8Pzu3CC78"

# 👇 SECOND BUTTON FIX LINK
SECOND_GROUP = "https://t.me/Doremoncheck_bot"


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    # 👇 Current group username auto detect
    group_username = chat.username

    # 👇 Group public nahi hai to stop
    if not group_username:
        return

    # 👇 Jis group me bot hai uska auto link
    group_link = f"https://t.me/{group_username}"

    # 👇 Share link
    share_url = (
        "https://t.me/share/url?url="
        + urllib.parse.quote(group_link)
    )

    if update.message and update.message.new_chat_members:

        for member in update.message.new_chat_members:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "📢 Share Group[1/2]",
                        url=share_url
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔥 VIP GROUP",
                        url=SECOND_GROUP
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=chat.id,
                text=(
                    f"👋 Welcome {member.first_name}!\n\n"
                    "Join our VIP group below 👇"
                ),
                reply_markup=reply_markup
            )


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome
        )
    )

    print("✅ Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()