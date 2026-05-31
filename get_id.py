from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update

BOT_TOKEN = "8858083030:AAF-3mthMQsjqdo2jbY8SBY0D7LVtnoOc4w"


async def get_file_id(update, context):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"file_id: {file_id}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, get_file_id))
print("Отправь фото боту!")
app.run_polling()

