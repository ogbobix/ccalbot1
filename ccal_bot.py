import telebot
import json
from telebot import types

bot = telebot.TeleBot("5970030398:AAEzg76jIB5vWsFe45an6UciIuDJUg3xMGs")

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("Мужчина"), types.KeyboardButton("Женщина"))
    message_text = f"Привет, {message.from_user.first_name}! Я бот, с помощью которого можно узнать свой дневной рацион калорий и рассчитать БЖУ. Для подсчета используется формула Миффлина — Сан-Жеора. Чтобы начать работу, выберите ваш пол."
    bot.send_message(message.chat.id, message_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_gender(message):
    if message.text == "Мужчина" or message.text == "Женщина":
        ask_for_parameters(message, message.text)
    else:
        bot.send_message(message.chat.id, "Ошибка")

def ask_for_parameters(message, gender):
    try:
        bot.send_message(message.chat.id, "Введите 3 числа через пробел: возраст, рост в сантиметрах, вес в килограммах")
        bot.register_next_step_handler(message, ask_for_goals, gender)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def ask_for_goals(message, gender):
    try:
        age, height, weight = map(int, message.text.split())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton("Поддержание"), types.KeyboardButton("Сушка"), types.KeyboardButton("Набор массы"))
        bot.send_message(message.chat.id, "Выберите вашу цель:", reply_markup=markup)
        bot.register_next_step_handler(message, calculate_ccal, gender, age, height, weight)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def calculate_ccal(message, gender, age, height, weight):
    try:
        goal = message.text
        if gender == "Мужчина":
            ccal = ((10 * weight) + (6.25 * height) - (5 * age) + 5)
        else:
            ccal = ((10 * weight) + (6.25 * height) - (5 * age) - 161)

        protein, fats, crabs, ccal_goal = 0, 0, 0, 0

        if goal == "Поддержание":
            protein = weight * 1.3
            fats = weight * 0.8
            crabs = weight * 2
            ccal_goal = ccal
        elif goal == "Сушка":
            protein = weight * 1.5
            fats = weight * 0.8
            crabs = weight * 2
            ccal_goal = ccal * 0.8
        elif goal == "Набор массы":
            protein = weight * 2
            fats = weight * 1
            crabs = weight * 4
            ccal_goal = ccal * 1.2
        else:
            bot.send_message(message.chat.id, "Неизвестная цель. Пожалуйста, выберите одну из предложенных целей.")
            return

        with open("menu.json", "r", encoding="utf-8") as file:
            menu_data = json.load(file)

        if goal in menu_data:
            menu_items = menu_data[goal]
            
        else:
            menu = "Данные меню для выбранной цели отсутствуют."

        result_text = f"Ваш дневной рацион: {ccal_goal:.2f} калорий\n1) Ваш БЖУ:\n   - Белки: {protein:.2f} грамм\n   - Жиры: {fats:.2f} грамм\n   - Углеводы: {crabs:.2f} грамм\n\nМеню на сегодня (в зависимости от цели '{goal}'):\n{menu_data[goal]}"
        bot.reply_to(message, result_text)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректные данные. Пожалуйста, введите 3 числа.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()









