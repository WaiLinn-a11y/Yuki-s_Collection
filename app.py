import logging
import os  # 'os' import ပါရမယ်

from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    ContextTypes
)

# --- 1. GET YOUR SECRETS FROM THE "SECRET BOX" ---
# ဒါက 100% မှန်ပါတယ်
TOKEN = os.environ.get("BOT_TOKEN")
RENDER_APP_NAME = os.environ.get("RENDER_APP_NAME")


# =======================================================
# === 🎬 YOUR MOVIE DATABASE ===
# =======================================================
# ခင်ဗျားဖြည့်ထားတဲ့အတိုင်း မှန်ပါတယ်
MOVIE_DATABASE = {
    "spiderman_1": {
        "file_id": "BAACAgUAAxkBAAIBUGkVmRH-wYW6d0k0Cj6UxYeqQrwVAALIGwACHeOpVINIh_HeFxl_NgQ",
        "caption": """
🎬 Spider-Man 1 (2002)
🎥 Genre: Action / Adventure / Sci-Fi
📅 Duration: 2h 1m
✅ Enjoy your movie!
"""
    },
    "spiderman_3": {
        "file_id": "BAACAgUAAyEFAATG5gFlAAMEaRg66pXmoYLCQ5lSg1RACq0ezagAAk4bAAIE8sBU8AG68fxV2F42BA",
        "caption": """
🎬 Spider-Man 3 (2007)
🎥 Genre: Action / Sci-Fi / Adventure
📅 Duration: 2h 19m
✅ Enjoy your movie!
"""
    }
}
# --------------------------------------------------------


# --- 2. LOGGING SETUP (ဒါက ကျန်နေလို့ ပြန်ထည့်ထားပါတယ်) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- 3. BOT FUNCTIONS (ဒါတွေက အဓိကကျန်နေတာပါ) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'မင်္ဂလာပါ! ရုပ်ရှင်ရယူရန် ဒီလိုရိုက်ပါ:\n'
        '/movie <keyword>\n\n'
        'ဥပမာ: /movie spiderman_1'
    )

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    
    if not context.args:
        await update.message.reply_text(
            'မှားနေပါတယ်! Keyword ထည့်ဖို့မေ့နေပါတယ်။\n'
            'ဥပမာ: /movie spiderman_1'
        )
        return

    keyword = context.args[0].lower() 
    movie_data = MOVIE_DATABASE.get(keyword)

    if movie_data:
        try:
            await context.bot.send_video(
                chat_id=chat_id, 
                video=movie_data["file_id"],
                caption=movie_data["caption"]
            )
            logger.info(f"Video '{keyword}' sent to {chat_id}")
        except Exception as e:
            logger.error(f"Error sending video '{keyword}' to {chat_id}: {e}")
            await update.message.reply_text("Video ပို့ရာတွင် အမှားအယွင်းတစ်ခု ဖြစ်ပွားပါသည်။")
    else:
        await update.message.reply_text(
            f"'{keyword}' ဆိုတဲ့ ရုပ်ရှင် ကျွန်တော့်ဆီမှာ မရှိသေးပါဘူး။"
        )

# --- 4. MAIN FUNCTION (ဒါက မှန်ပါတယ်) ---

def main() -> None:
    # Check if the "secret box" variables are set
    if TOKEN is None:
        logger.error("FATAL: BOT_TOKEN environment variable is not set.")
        return
    if RENDER_APP_NAME is None:
        logger.error("FATAL: RENDER_APP_NAME environment variable is not set.")
        return

    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", send_movie)) 

    # --- THIS IS THE NEW PART FOR WEBHOOKS ---
    # ဒါက 100% မှန်ပါတယ်
    PORT = int(os.environ.get("PORT", 8443))
    webhook_url = f"https://{RENDER_APP_NAME}.onrender.com/{TOKEN}"
    
    logger.info(f"Starting webhook on port {PORT}")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN, # The path part of the URL
        webhook_url=webhook_url # The full, public URL
    )

if __name__ == '__main__':
    main()