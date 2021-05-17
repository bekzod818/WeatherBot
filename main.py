import requests
import telebot
from config import *
from telebot import types

bot = telebot.TeleBot(TOKEN)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('🔍 Search', 'ℹ️ About')

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.first_name
    msg = f"<b>Welcome {user}</b>"
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['search'])
def start(message):
    msg = f"<b>🔍 Enter a country or city name</b>"
    bot.send_message(message.chat.id, msg, parse_mode='html')

@bot.message_handler(content_types=['text'])
def weather(message):
    if message.text == '🔍 Search':
        msg = f"<b>🔍 Enter a country or city name</b>"
        bot.send_message(message.chat.id, msg, parse_mode='html')
    elif message.text == 'ℹ️ About':
        msg = f"""OpenWeather global services.
Weather forecasts, nowcasts and history in fast and elegant way.

We make hyper-local weather data open for any business.
For each point on the globe, we provide historical, current and forecasted weather data via light-speed APIs.

Creater: @Bekzod_Rakhimov"""
        bot.send_message(message.chat.id, msg, reply_markup=markup)

    else:
        try:
            CITY = message.text
            URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API}'
            response = requests.get(url=URL).json()
            city_info = {
                'city': CITY,
                'temp': response['main']['temp'],
                'humidity': response['main']['humidity'],
                'weather': response['weather'][0]['description'],
                'wind': response['wind']['speed'],
                'pressure': response['main']['pressure'],
            }
            msg = f"<b><u>{CITY.upper()}</u>\n\nWeather is {city_info['weather']}</b>\n------------------------------------\n🌡 Temperature: <b>{city_info['temp']} C</b>\n💨 Wind: <b>{city_info['wind']} m/s</b>\n💦 Humidity: <b>{city_info['humidity']} %</b>\n🧬 Pressure: <b>{city_info['pressure']} hPa</b>"
            bot.send_message(message.chat.id, msg, parse_mode='html')
        except:
            msg1 = f"<b>🙅‍♂️ Nothing found try again</b>"
            bot.send_message(message.chat.id, msg1, parse_mode='html')

bot.polling(none_stop=True)