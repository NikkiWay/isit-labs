from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from xml.dom import minidom
import os
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CNY", "TRY"]
CANCEL_BUTTON = "❌ Отменить"


def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        [[CANCEL_BUTTON]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# Обработчики сообщений
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите валюту:",
        reply_markup=get_currency_keyboard()
    )


def get_currency_keyboard():
    keyboard = []
    row = []
    for i, currency in enumerate(CURRENCIES, 1):
        row.append(currency)
        if i % 3 == 0 or i == len(CURRENCIES):
            keyboard.append(row)
            row = []

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_currency_data(currency_code: str, date: str) -> dict:
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    dom = minidom.parseString(response.text)
    dom.normalize()

    valutes = dom.getElementsByTagName("Valute")
    for valute in valutes:
        char_code = valute.getElementsByTagName("CharCode")[0].childNodes[0].nodeValue
        if char_code == currency_code:
            return {
                "name": valute.getElementsByTagName("Name")[0].childNodes[0].nodeValue.strip(),
                "value": valute.getElementsByTagName("Value")[0].childNodes[0].nodeValue.replace(',', '.'),
                "nominal": valute.getElementsByTagName("Nominal")[0].childNodes[0].nodeValue
            }

    return None


async def handle_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency_code = update.message.text

    if currency_code not in CURRENCIES:
        await update.message.reply_text(
            "Ошибка: выберите валюту из списка.",
            reply_markup=get_currency_keyboard()
        )
        return

    context.user_data["currency"] = currency_code
    await update.message.reply_text(
        f"Выбрана валюта: {currency_code}\nВведите дату в формате ДД.ММ.ГГГГ:",
        reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True)
    )


async def handle_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if "currency" not in context.user_data:
        await update.message.reply_text(
            "❌ Сначала выберите валюту через меню!",
            reply_markup=get_currency_keyboard()
        )
        return

    if user_text == CANCEL_BUTTON:
        await update.message.reply_text(
            "Действие отменено.",
            reply_markup=get_currency_keyboard()
        )
        context.user_data.pop("currency", None)
        return

    # Проверка формата даты с регулярным выражением
    if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', user_text):
        await update.message.reply_text(
            "❌ Неверный формат даты!\n"
            "Пожалуйста, введите дату в формате ДД.ММ.ГГГГ\n"
            "Пример: 11.03.2022",
            reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True)
        )
        return  # Остаемся в режиме ввода даты

    try:
        date = user_text.replace(".", "/")
        currency = context.user_data.get("currency")
        data = get_currency_data(currency, date)

        if not data:
            await update.message.reply_text(
                "❌ Курс не найден для выбранной даты",
                reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True)
            )
            return

        await update.message.reply_text(
            f"Курс {data['name']} на {user_text}:\n"
            f"{data['nominal']} {currency} = {data['value']} руб.",
            reply_markup=get_currency_keyboard()
        )
        context.user_data.pop("currency", None)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {e}\nПопробуйте ввести дату снова:",
            reply_markup=ReplyKeyboardMarkup([[CANCEL_BUTTON]], resize_keyboard=True)
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text([*CURRENCIES]), handle_currency))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date))

    app.run_polling()


if __name__ == "__main__":
    main()
