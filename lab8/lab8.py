import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Категории и блюда
image_urls = {
    # Итальянская кухня
    "Пицца": "https://upload.wikimedia.org/wikipedia/commons/0/05/Pizza_with_tomatoes.jpg",
    "Паста": "https://upload.wikimedia.org/wikipedia/commons/1/11/Spaghetti_al_Pomodoro.JPG",
    "Тирамису": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Tiramisu_-_Italian_Dessert.jpg",
    "Ризотто": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Risotto_ai_funghi.jpg",
    "Лазанья": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Lasagna_serving.jpg",

    # Японская кухня
    "Суши": "https://upload.wikimedia.org/wikipedia/commons/6/60/Sushi_platter.jpg",
    "Рамен": "https://upload.wikimedia.org/wikipedia/commons/1/15/Tonkotsu_ramen_by_ayustety_in_Tokyo.jpg",
    "Темпура": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Tendon.jpg",
    "Якитори": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Yakitori.jpg",
    "Моти": "https://upload.wikimedia.org/wikipedia/commons/3/34/Mochi.jpg",

    # Мексиканская кухня
    "Тако": "https://upload.wikimedia.org/wikipedia/commons/5/54/Tacos_de_carnitas.jpg",
    "Буррито": "https://upload.wikimedia.org/wikipedia/commons/0/05/Burrito.JPG",
    "Начос": "https://upload.wikimedia.org/wikipedia/commons/6/69/Nachos_with_beef_and_cheese.jpg",
    "Гуакамоле": "https://upload.wikimedia.org/wikipedia/commons/b/b2/Guacamole.jpg",
    "Кесадилья": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Quesadilla.jpg",

    # Французская кухня
    "Круассан": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Croissant-Petr-Kratochvil.jpg",
    "Суп-пюре": "https://upload.wikimedia.org/wikipedia/commons/6/64/Butternut_squash_soup.jpg",
    "Киш": "https://upload.wikimedia.org/wikipedia/commons/3/38/Quiche.jpg",
    "Крем-брюле": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Creme_brulee.jpg",
    "Рататуй": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Ratatouille_by_cookingangel.jpg"
}

user_data = {}

def init_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'counter': {dish: 0 for dish in image_urls},
            'history': []
        }

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Итальянская", "Японская", "Мексиканская", "Французская")
    return keyboard

def sub_menu(category):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dishes = {
        "Итальянская": ["Пицца", "Паста", "Тирамису", "Ризотто", "Лазанья"],
        "Японская": ["Суши", "Рамен", "Темпура", "Якитори", "Моти"],
        "Мексиканская": ["Тако", "Буррито", "Начос", "Гуакамоле", "Кесадилья"],
        "Французская": ["Круассан", "Суп-пюре", "Киш", "Крем-брюле", "Рататуй"]
    }
    keyboard.add(*dishes.get(category, []), "Назад")
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    init_user(message.chat.id)
    user_data[message.chat.id]['history'].clear()
    user_data[message.chat.id]['history'].append('main')
    bot.send_message(message.chat.id, "Выберите кухню мира:", reply_markup=main_menu())

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    init_user(user_id)

    if message.text == "Назад":
        if len(user_data[user_id]['history']) > 1:
            user_data[user_id]['history'].pop()
            prev = user_data[user_id]['history'][-1]
            if prev == "main":
                bot.send_message(user_id, "Главное меню:", reply_markup=main_menu())
            else:
                bot.send_message(user_id, f"Кухня: {prev}", reply_markup=sub_menu(prev))
        return

    if message.text in image_urls:
        user_data[user_id]['counter'][message.text] += 1
        try:
            bot.send_photo(
                user_id,
                photo=image_urls[message.text],
                caption=f"🍽️ {message.text}\n📊 Нажатий: {user_data[user_id]['counter'][message.text]}\nℹ️ {get_description(message.text)}"
            )
        except:
            bot.send_message(
                user_id,
                f"{message.text} (изображение недоступно)\n📊 Нажатий: {user_data[user_id]['counter'][message.text]}\nℹ️ {get_description(message.text)}"
            )
    elif message.text in ["Итальянская", "Японская", "Мексиканская", "Французская"]:
        user_data[user_id]['history'].append(message.text)
        bot.send_message(user_id, f"Вы выбрали: {message.text} кухня", reply_markup=sub_menu(message.text))

def get_description(dish):
    desc = {
        "Пицца": "Традиционное итальянское блюдо с сыром, томатами и начинкой",
        "Паста": "Макаронное блюдо, подаваемое с соусами",
        "Тирамису": "Слой десерта с маскарпоне, кофе и какао",
        "Ризотто": "Итальянское блюдо из риса на бульоне",
        "Лазанья": "Слоёное блюдо из пасты, соуса и сыра",
        "Суши": "Рис с рыбой, морепродуктами или овощами",
        "Рамен": "Японский суп с лапшой и мясом",
        "Темпура": "Обжаренные во фритюре морепродукты и овощи",
        "Якитори": "Шашлычки из курицы на шпажках",
        "Моти": "Сладкий рисовый десерт",
        "Тако": "Мексиканская лепёшка с начинкой",
        "Буррито": "Рулет из тортильи с мясом и овощами",
        "Начос": "Кукурузные чипсы с сыром и соусами",
        "Гуакамоле": "Паста из авокадо с луком и лаймом",
        "Кесадилья": "Жареная лепёшка с сыром и начинкой",
        "Круассан": "Слоёная булочка в форме полумесяца",
        "Суп-пюре": "Французский крем-суп из овощей",
        "Киш": "Несладкий пирог с начинкой и яичной заливкой",
        "Крем-брюле": "Сливочный десерт с карамельной коркой",
        "Рататуй": "Овощное рагу родом из Прованса"
    }
    return desc.get(dish, "Описание отсутствует")

if __name__ == '__main__':
    bot.polling(none_stop=True)
