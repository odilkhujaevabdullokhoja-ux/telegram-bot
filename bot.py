import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, filters, ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

NAME, PHONE, PRODUCT, QUANTITY, CONFIRM = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo="AgACAgIAAxkBAAMgahvcXjbnJZOsqbOXcA1cxfb42YsAAn0Xaxsk3eBIVZH37JzSFrYBAAMCAAN5AAM7BA",
        caption="👋 Привет! Это наш товар — Loro Piana 👜\nЦена: 230.000 сум\n\nНапиши /order чтобы сделать заказ!"
    )

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Шаг 1/4: Введите ваше имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 Шаг 2/4: Ваш номер телефона:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("🛍 Шаг 3/4: Что хотите заказать?")
    return PRODUCT

async def get_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    await update.message.reply_text("🔢 Шаг 4/4: Количество:")
    return QUANTITY

async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quantity"] = update.message.text
    keyboard = [["✅ Подтвердить", "❌ Отменить"]]
    await update.message.reply_text(
        f"📋 Ваш заказ:\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📞 Телефон: {context.user_data['phone']}\n"
        f"🛍 Товар: {context.user_data['product']}\n"
        f"🔢 Количество: {context.user_data['quantity']}\n\nВсё верно?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return CONFIRM

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "✅ Подтвердить":
        await update.message.reply_text("🎉 Заказ принят!", reply_markup=ReplyKeyboardRemove())
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🔔 НОВЫЙ ЗАКАЗ!\n\n"
                 f"👤 {context.user_data['name']}\n"
                 f"📞 {context.user_data['phone']}\n"
                 f"🛍 {context.user_data['product']}\n"
                 f"🔢 {context.user_data['quantity']}"
        )
    else:
        await update.message.reply_text("❌ Отменено.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("order", order_start)],
        states={
            NAME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PRODUCT:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_product)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity)],
            CONFIRM:  [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
