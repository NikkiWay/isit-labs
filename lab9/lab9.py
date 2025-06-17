from telebot import TeleBot, types
import threading
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(TELEGRAM_TOKEN)

image_urls = {
    # Европа
    "Лувр": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Louvre_Museum_Wikimedia_Commons.jpg",
    "Британский музей": "https://upload.wikimedia.org/wikipedia/commons/0/01/British_Museum_from_NE_2.JPG",
    "Прадо": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Madrid_-_Museo_del_Prado_1.jpg",
    "Рейксмюсеум": "https://upload.wikimedia.org/wikipedia/commons/2/27/Rijksmuseum.jpg",
    "Уффици": "https://upload.wikimedia.org/wikipedia/commons/5/59/Uffizi_Gallery.jpg",

    # Азия
    "Национальный музей Токио": "https://upload.wikimedia.org/wikipedia/commons/5/54/Tokyo_National_Museum_Honkan_2010.JPG",
    "Пекинский музей": "https://upload.wikimedia.org/wikipedia/commons/d/d0/National_Museum_of_China_2018.jpg",
    "Музей Искусств Гуггенхайма (Абу-Даби)": "https://upload.wikimedia.org/wikipedia/commons/0/03/Guggenheim_Abu_Dhabi_model.jpg",
    "Индийский музей": "https://upload.wikimedia.org/wikipedia/commons/3/3b/Indian_Museum_Kolkata.jpg",
    "Музей Исламского Искусства (Доха)": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Museum_of_Islamic_Art%2C_Doha%2C_Qatar.jpg",

    # Америка
    "Метрополитен-музей": "https://upload.wikimedia.org/wikipedia/commons/9/97/The_Metropolitan_Museum_of_Art_%28The_Met%29_-_New_York_City.jpg",
    "МоМА": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Museum_of_Modern_Art_%28MoMA%29_-_New_York_City.jpg",
    "Смитсоновский музей": "https://upload.wikimedia.org/wikipedia/commons/8/81/Smithsonian_Castle.JPG",
    "Художественный музей Чикаго": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Art_Institute_of_Chicago_facade.jpg",
    "Музей естественной истории (Нью-Йорк)": "https://upload.wikimedia.org/wikipedia/commons/e/e1/American_Museum_of_Natural_History.jpg",

    # Россия
    "Эрмитаж": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Hermitage_Museum%2C_St._Petersburg.jpg",
    "Третьяковская галерея": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Tretyakov_Gallery.jpg",
    "Пушкинский музей": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Pushkin_Museum.jpg",
    "Русский музей": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Russian_Museum_Saint_Petersburg.jpg",
    "Политехнический музей": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Polytechnic_Museum_Moscow.jpg"
}

descriptions = {
    "Лувр": "Крупнейший художественный музей мира, расположен в Париже.",
    "Британский музей": "Один из старейших музеев мира, находится в Лондоне.",
    "Прадо": "Главный художественный музей Испании, в Мадриде.",
    "Рейксмюсеум": "Национальный музей искусства Нидерландов, Амстердам.",
    "Уффици": "Знаменитая галерея во Флоренции с коллекцией Возрождения.",
    "Национальный музей Токио": "Старейший и крупнейший музей Японии.",
    "Пекинский музей": "Национальный музей Китая, на площади Тяньаньмэнь.",
    "Музей Искусств Гуггенхайма (Абу-Даби)": "Филиал знаменитой сети музеев Гуггенхайма.",
    "Индийский музей": "Один из старейших музеев Азии, расположен в Калькутте.",
    "Музей Исламского Искусства (Доха)": "Ведущий музей исламского искусства в Катаре.",
    "Метрополитен-музей": "Один из крупнейших музеев США, Нью-Йорк.",
    "МоМА": "Музей современного искусства в Нью-Йорке.",
    "Смитсоновский музей": "Комплекс музеев в Вашингтоне.",
    "Художественный музей Чикаго": "Крупный художественный музей в США.",
    "Музей естественной истории (Нью-Йорк)": "Один из крупнейших научных музеев мира.",
    "Эрмитаж": "Крупнейший художественный и культурно-исторический музей России.",
    "Третьяковская галерея": "Главный музей русского изобразительного искусства.",
    "Пушкинский музей": "Музей изобразительных искусств в Москве.",
    "Русский музей": "Первый в стране государственный музей русского искусства.",
    "Политехнический музей": "Крупнейший технический музей России."
}

user_data = {}
lock = threading.Lock()


def init_user(user_id):
    with lock:
        if user_id not in user_data:
            user_data[user_id] = {
                'counter': {name: 0 for name in image_urls},
                'menu_message_id': None
            }

def main_menu():
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("Европа", callback_data="region_Европа"),
        types.InlineKeyboardButton("Азия", callback_data="region_Азия"),
        types.InlineKeyboardButton("Америка", callback_data="region_Америка"),
        types.InlineKeyboardButton("Россия", callback_data="region_Россия")
    ]
    keyboard.add(*buttons[:2])
    keyboard.add(*buttons[2:])
    return keyboard

def sub_menu(region):
    regions = {
        "Европа": ["Лувр", "Британский музей", "Прадо", "Рейксмюсеум", "Уффици"],
        "Азия": ["Национальный музей Токио", "Пекинский музей", "Музей Искусств Гуггенхайма (Абу-Даби)", "Индийский музей", "Музей Исламского Искусства (Доха)"],
        "Америка": ["Метрополитен-музей", "МоМА", "Смитсоновский музей", "Художественный музей Чикаго", "Музей естественной истории (Нью-Йорк)"],
        "Россия": ["Эрмитаж", "Третьяковская галерея", "Пушкинский музей", "Русский музей", "Политехнический музей"]
    }
    keyboard = types.InlineKeyboardMarkup()
    group = regions.get(region, [])
    for i in range(0, len(group), 3):
        row = group[i:i+3]
        keyboard.row(*[types.InlineKeyboardButton(m, callback_data=f"museum_{m}") for m in row])
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    init_user(message.chat.id)
    with lock:
        if user_data[message.chat.id]['menu_message_id']:
            try:
                bot.delete_message(message.chat.id, user_data[message.chat.id]['menu_message_id'])
            except:
                pass

    msg = bot.send_message(
        message.chat.id,
        "Выберите регион и музей:",
        reply_markup=main_menu()
    )
    with lock:
        user_data[message.chat.id]['menu_message_id'] = msg.message_id

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    init_user(user_id)

    try:
        if call.data.startswith("region_"):
            region = call.data.split("_")[1]
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=f"Регион: {region}",
                reply_markup=sub_menu(region)
            )

        elif call.data.startswith("museum_"):
            museum = call.data.split("_", 1)[1]
            with lock:
                user_data[user_id]['counter'][museum] += 1

            try:
                bot.edit_message_media(
                    chat_id=user_id,
                    message_id=call.message.message_id,
                    media=types.InputMediaPhoto(
                        media=image_urls[museum],
                        caption=f"🏛️ {museum}\n📊 Просмотров: {user_data[user_id]['counter'][museum]}\nℹ️ {descriptions.get(museum, 'Описание отсутствует')}"
                    )
                )
            except:
                bot.edit_message_text(
                    chat_id=user_id,
                    message_id=call.message.message_id,
                    text=f"🏛️ {museum}\n📊 Просмотров: {user_data[user_id]['counter'][museum]}\nℹ️ {descriptions.get(museum, 'Описание отсутствует')}"
                )

            msg = bot.send_message(
                user_id,
                "Выберите регион и музей:",
                reply_markup=main_menu()
            )
            with lock:
                user_data[user_id]['menu_message_id'] = msg.message_id

            bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.answer_callback_query(call.id, "Произошла ошибка. Попробуйте снова.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
