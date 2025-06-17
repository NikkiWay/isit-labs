from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
import wikipedia
import logging
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMINS_IDS = list(map(int, os.getenv("ADMINS_IDS", "").split(",")))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WAITING_FOR_QUERY = 1
wikipedia.set_lang("ru")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Используйте /wiki чтобы найти статью в Википедии")


async def start_wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in ADMINS_IDS:
        await update.message.reply_text("❌ У вас нет доступа к использованию команды")
        return ConversationHandler.END

    await update.message.reply_text(
        "🔍 Введите ключевое слово для поиска статьи в Википедии\nОтмена: /cancel"
    )
    return WAITING_FOR_QUERY


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.message.text
        summary = wikipedia.summary(query, sentences=3)
        await update.message.reply_text(f"📘 Результат:\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        await update.message.reply_text(
            f"⚠️ Слишком много вариантов: {', '.join(e.options[:5])}...\nПопробуйте уточнить запрос."
        )
    except wikipedia.exceptions.PageError:
        await update.message.reply_text("❌ Статья не найдена. Попробуйте другой запрос.")
    except Exception as e:
        logger.exception("Ошибка при поиске в Wikipedia")
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Поиск отменён. Для начала заново используйте /wiki")
    return ConversationHandler.END


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("wiki", start_wiki_command)],
        states={
            WAITING_FOR_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
