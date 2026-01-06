from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
import os

# --- Telegram bot token va kanal nomlari ---
TOKEN = "8144668632:AAEhWPr8scF3Ry5i0WVNnI-Q1IXQs7JN9P4"
CHANNELS = ["@alishern1_youtuber", "@UzAniVoice"]  # majburiy obuna bo'lishi kerak bo'lgan kanallar

# /start handler
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    for channel in CHANNELS:
        try:
            member = context.bot.get_chat_member(channel, user.id)
            if member.status in ["left", "kicked"]:
                update.message.reply_text(f"Iltimos, {channel} kanaliga obuna bo‘ling!")
                return
        except:
            update.message.reply_text(f"{channel} tekshirishda xatolik yuz berdi.")
            return

    update.message.reply_text("✅ Siz kanallarga obuna bo‘ldingiz! Endi matn yuboring, men uni ovozga aylantiraman.")

# Matnni ovozga aylantirish
def text_to_voice(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id

    if not text.strip():
        return

    filename = f"{chat_id}_output.mp3"

    # Google TTS bilan o'zbekcha ovoz
    tts = gTTS(text=text, lang='uz')
    tts.save(filename)

    context.bot.send_audio(chat_id=chat_id, audio=open(filename, "rb"))
    os.remove(filename)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_to_voice))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    not_subscribed = []

    for channel in CHANNELS:
        try:
            member = context.bot.get_chat_member(channel, user.id)
            # Agar foydalanuvchi kanalga obuna bo'lmagan bo'lsa
            if member.status in ["left", "kicked"]:
                not_subscribed.append(channel)
        except:
            update.message.reply_text(f"{channel} tekshirishda xatolik yuz berdi.")
            return

    if not_subscribed:
        # Agar biror kanalga obuna bo'lmagan bo'lsa
        update.message.reply_text(
            "❌ Iltimos, quyidagi kanallarga obuna bo‘ling:\n" +
            "\n".join(not_subscribed)
        )
        return

    # Agar foydalanuvchi hamma kanallarga obuna bo'lsa
    update.message.reply_text(
        "✅ Siz barcha kanallarga obuna bo‘ldingiz! Endi matn yuboring, men uni ovozga aylantiraman."
    )
