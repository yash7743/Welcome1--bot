import logging
import json
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ======================================================
# SETTINGS
# ======================================================

BOT_TOKEN = "8882413050:AAGbzgUFQkjNlr9W6ICzzpwAUJWkxY2PL1c"

ADMIN_CHAT_ID = 8686958443

PRIVATE_GROUP_LINK = "https://t.me/+dE0mrYkSOG0yZTE1"

# Images
DISPLAY_IMAGE_1 = "display1.jpg"
DISPLAY_IMAGE_2 = "display2.jpg"
PLAN_IMAGE = "plan.jpg"
PAYMENT_QR = "payment.jpg"

# Database File
DATA_FILE = "plans.json"

# ======================================================
# LOGGING
# ======================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ======================================================
# LOAD / SAVE DATA
# ======================================================

def load_data():

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r") as file:
                return json.load(file)

        except:
            return {}

    return {}


def save_data(data):

    with open(DATA_FILE, "w") as file:
        json.dump(data, file)


selected_plan = load_data()

# ======================================================
# PLANS
# ======================================================

PLANS = {

    "basic": {
        "name": "Basic Plan 1 month",
        "price": "₹99"
    },

    "premium": {
        "name": "Premium Plan 2 Month",
        "price": "₹199"
    },

    "vip": {
        "name": "VIP Plan lifeTime",
        "price": "₹499"
    }

}

# ======================================================
# START COMMAND
# ======================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    try:

        # Image 1
        if os.path.exists(DISPLAY_IMAGE_1):

            with open(DISPLAY_IMAGE_1, "rb") as photo:

                await update.message.reply_photo(
                    photo=photo
                )

        # Image 2
        if os.path.exists(DISPLAY_IMAGE_2):

            with open(DISPLAY_IMAGE_2, "rb") as photo:

                await update.message.reply_photo(
                    photo=photo
                )

        keyboard = [
            [
                InlineKeyboardButton(
                    "⚡ Fast Access",
                    callback_data="fast_access"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        text = f"""
👋 Welcome {user.first_name}

Mallu
Ind lesbian 
Telugu recording dance 
Telugu tango 
Foringer long 
Models actress 
IND candid 
South Indian 
Jav
Savita bhabhi comics 
Hindi adult 
Mom son
Bro sis
Cp 
Rp
Hideen cam 
Family group
Tamil
Incest sleeping 
Rp
Mom son incest
Sleeping pills 
Pussy lover 
Tango 
Hidden 
Spy 
Pissing ind
Science class
School 
Flash and candid 
Tamil sis
Real spa
Doggy style 
Flashing 
Dick flash
doggy style 
All colaction 
⚡ Fast Access lene ke liye
neeche button par click karo.
"""

        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup
        )

    except Exception as e:

        logger.error(f"START ERROR: {e}")

        await update.message.reply_text(
            "❌ Error aaya. Dobara try karo."
        )

# ======================================================
# BUTTON HANDLER
# ======================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = str(query.from_user.id)

    try:

        # ==================================================
        # FAST ACCESS
        # ==================================================

        if query.data == "fast_access":

            keyboard = [

                [
                    InlineKeyboardButton(
                        "Basic ₹99",
                        callback_data="plan_basic"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "Premium ₹199",
                        callback_data="plan_premium"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "VIP ₹499",
                        callback_data="plan_vip"
                    )
                ]

            ]

            reply_markup = InlineKeyboardMarkup(
                keyboard
            )

            if os.path.exists(PLAN_IMAGE):

                with open(PLAN_IMAGE, "rb") as photo:

                    await query.message.reply_photo(
                        photo=photo,
                        caption="""
⚡ Subscription Plans

👇 Apna plan select karo
""",
                        reply_markup=reply_markup
                    )

            else:

                await query.message.reply_text(
                    "❌ plan.jpg file nahi mili."
                )

        # ==================================================
        # PLAN SELECT
        # ==================================================

        elif query.data.startswith("plan_"):

            plan_key = query.data.replace(
                "plan_",
                ""
            )

            if plan_key not in PLANS:

                await query.message.reply_text(
                    "❌ Invalid Plan"
                )

                return

            selected_plan[user_id] = plan_key

            save_data(selected_plan)

            plan = PLANS[plan_key]

            token_id = f"TOKEN-{user_id}"

            keyboard = [
                [
                    InlineKeyboardButton(
                        "✅ Verify Payment",
                        callback_data="verify_wait"
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(
                keyboard
            )

            text = f"""
✅ Plan Selected

📦 Plan:
{plan['name']}

💰 Amount:
{plan['price']}

🆔 Token ID:
{token_id}

📸 QR scan karke payment karo.

Payment ke baad screenshot bhejo.

⏳ Verification Time:
5-10 Minutes
"""

            if os.path.exists(PAYMENT_QR):

                with open(PAYMENT_QR, "rb") as qr:

                    await query.message.reply_photo(
                        photo=qr,
                        caption=text,
                        reply_markup=reply_markup
                    )

            else:

                await query.message.reply_text(
                    "❌ payment.jpg file nahi mili."
                )

        # ==================================================
        # VERIFY WAIT
        # ==================================================

        elif query.data == "verify_wait":

            await query.message.reply_text(
                """
📸 Payment screenshot bhejo.

⏳ Admin 5-10 minute me verify karega.
"""
            )

        # ==================================================
        # ADMIN VERIFY
        # ==================================================

        elif query.data.startswith("admin_verify_"):

            # Security Check
            if query.from_user.id != ADMIN_CHAT_ID:

                await query.answer(
                    "❌ Not Authorized",
                    show_alert=True
                )

                return

            target_user_id = int(
                query.data.replace(
                    "admin_verify_",
                    ""
                )
            )

            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"""
✅ Payment Verified

🔒 Private Group Link:

{PRIVATE_GROUP_LINK}

🎉 Welcome
"""
            )

            await query.message.reply_text(
                "✅ User Verified Successfully"
            )

    except Exception as e:

        logger.error(f"BUTTON ERROR: {e}")

        await query.message.reply_text(
            "❌ Error aaya."
        )

# ======================================================
# PHOTO HANDLER
# ======================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        user = update.effective_user

        user_id = str(user.id)

        if user_id not in selected_plan:

            await update.message.reply_text(
                "⚠️ Pehle plan select karo."
            )

            return

        plan_key = selected_plan[user_id]

        if plan_key not in PLANS:

            await update.message.reply_text(
                "❌ Invalid Plan"
            )

            return

        plan = PLANS[plan_key]

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Verify User",
                    callback_data=f"admin_verify_{user_id}"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        caption = f"""
💳 New Payment Request

👤 Name:
{user.first_name}

🆔 User ID:
{user_id}

📦 Plan:
{plan['name']}

💰 Amount:
{plan['price']}
"""

        # Send screenshot to admin
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption,
            reply_markup=reply_markup
        )

        # User Message
        await update.message.reply_text(
            """
✅ Screenshot Received

⏳ Verification Time:
5-10 Minutes

Please wait...
"""
        )

    except Exception as e:

        logger.error(f"PHOTO ERROR: {e}")

        await update.message.reply_text(
            "❌ Screenshot bhejne me error aaya."
        )

# ======================================================
# OTHER MESSAGES
# ======================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Use /start"
    )

# ======================================================
# ERROR HANDLER
# ======================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        msg="Exception while handling update:",
        exc_info=context.error
    )

# ======================================================
# MAIN
# ======================================================

def main():

    try:

        app = Application.builder().token(
            BOT_TOKEN
        ).build()

        # START
        app.add_handler(
            CommandHandler(
                "start",
                start
            )
        )

        # BUTTONS
        app.add_handler(
            CallbackQueryHandler(
                button_handler
            )
        )

        # PHOTOS
        app.add_handler(
            MessageHandler(
                filters.PHOTO,
                photo_handler
            )
        )

        # OTHER TEXT
        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                message_handler
            )
        )

        # ERROR HANDLER
        app.add_error_handler(
            error_handler
        )

        print("✅ BOT RUNNING...")

        app.run_polling()

    except Exception as e:

        logger.error(f"MAIN ERROR: {e}")

# ======================================================
# RUN
# ======================================================

if __name__ == "__main__":
    main()