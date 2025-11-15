import logging
import os
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# --- 1. GET YOUR SECRETS (Same as before) ---
TOKEN = os.environ.get("BOT_TOKEN")
RENDER_APP_NAME = os.environ.get("RENDER_APP_NAME")


# =======================================================
# === 🎬 YOUR MOVIE DATABASE (Same as before) ===
# =======================================================
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

# --- 3. LOGGING (Same as before) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- 4. "SMART" START COMMAND (Same as before) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    
    if context.args:
        # --- A. USER CLICKED A DEEP LINK ---
        keyword = context.args[0].lower()
        logger.info(f"Deep link clicked for keyword: {keyword}")
        
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
            logger.warning(f"Keyword '{keyword}' from deep link not found in DB.")
            await update.message.reply_text("Sorry, that movie link seems to be old or broken.")
            
    else:
        # --- B. USER JUST TYPED /start ---
        logger.info("User sent /start with no args.")
        await update.message.reply_text(
            'မင်္ဂလာပါ! \n\n'
            'This bot sends you movies.\n'
            'Please find the movie you want in our public channel and click its link!'
        )

# --- 5. HELPER FOR RANDOM TEXT (Same as before) ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Sorry, I only understand movie links from our channel. '
        'Please go to our public channel to get a movie.'
    )

# --- *** 6. NEW DEBUG COMMAND *** ---
# This is our test.
async def version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("User sent /version command.")
    await update.message.reply_text(
        "✅ Bot Version 2.0 (Deep Link Code is LIVE)"
    )

# --- 7. MAIN FUNCTION (Updated) ---

def main() -> None:
    if TOKEN is None:
        logger.error("FATAL: BOT_TOKEN environment variable is not set.")
        return
    if RENDER_APP_NAME is None:
        logger.error("FATAL: RENDER_APP_NAME environment variable is not set.")
        return

    application = Application.builder().token(TOKEN).build()
    
    # --- REGISTER HANDLERS ---
    
    # 1. The "smart" /start command
    application.add_handler(CommandHandler("start", start))
    
    # 2. *** OUR NEW TEST COMMAND ***
    application.add_handler(CommandHandler("version", version))
    
    # 3. A helper to catch all other text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # --- Run the bot (Same as before) ---
    PORT = int(os.environ.get("PORT", 8443))
    webhook_url = f"https://{RENDER_APP_NAME}.onrender.com/{TOKEN}"
    
    logger.info(f"Starting webhook on port {PORT}")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=webhook_url 
    )

if __name__ == '__main__':
    main()
