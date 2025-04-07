
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

OWNER_ID = 6956680309
CHANNEL_LINK = "https://t.me/+Zwx3Y0CHp_RmYzEy"

photo_messages = []
video_messages = []
stats = {"photo": 0, "video": 0}

captions = ["Here's a little something to brighten your day! ☀️", 'Caught this moment just for you 😄', 'Boom! Instant happiness 💥🐾', 'Smile! This one’s a good one 😍', 'Delivered with love 💌', 'Hope this makes your day 10x better 💫', 'Fresh from the cuteness factory 🐶📦']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📷 Send Photo", callback_data='photo')],
        [InlineKeyboardButton("🎥 Send Video", callback_data='video')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose what you'd like to receive:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'photo':
        if photo_messages:
            msg_id = random.choice(photo_messages)
            caption = random.choice(captions)
            await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=OWNER_ID, message_id=msg_id, caption=caption)
            stats["photo"] += 1
        else:
            await query.message.reply_text("No photos available yet.")
    elif query.data == 'video':
        if video_messages:
            msg_id = random.choice(video_messages)
            caption = random.choice(captions)
            await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=OWNER_ID, message_id=msg_id, caption=caption)
            stats["video"] += 1
        else:
            await query.message.reply_text("No videos available yet.")

    await query.message.reply_text(f"Join our channel: {CHANNEL_LINK}")

async def save_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.forward_from_chat and update.message.from_user.id == OWNER_ID:
        msg = update.message
        if msg.video:
            video_messages.append(msg.message_id)
            await msg.reply_text("Video saved.")
        elif msg.photo:
            photo_messages.append(msg.message_id)
            await msg.reply_text("Photo saved.")
        else:
            await msg.reply_text("Only photos and videos are supported.")

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == OWNER_ID:
        await update.message.reply_text(f"📊 Stats:\nPhotos sent: {stats['photo']}\nVideos sent: {stats['video']}")
    else:
        await update.message.reply_text("You don't have permission to view stats.")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        raise ValueError("Missing TOKEN environment variable")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_handler))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ALL, save_forward))

    app.run_polling()

if __name__ == '__main__':
    main()
