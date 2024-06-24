# import libraries
import telebot
import requests
import json
import logging

# connecting to bot using it's token - ENTER YOUR TOKEN HERE !!!
bot = telebot.TeleBot('')
# Api key of weather site -
API = '5f55b6112bd972b12e094bbc8aeb91b6'
# url with weather data of current city
url = 'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'


# processing start button
@bot.message_handler(commands=['start'])
# function that will ask user to write city after he pressed start command
def start(message):
    bot.send_message(
        message.chat.id, 'Hello! Nice to meet you! Write city name:')


# processing text type(if user entered some text)
@bot.message_handler(content_types=['text'])
# function that shows weather depending on which city user entered
def get_weather(message):
    # saving city name into variable
    city = message.text.strip()
    # saving weather data from url in variable
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    # if request was succesfull
    if res.status_code == 200:
        # load() - converts json into text format
        data = json.loads(res.text)
        # getting temp value from data
        temp = data['main']['temp']
        # bot's reply to user which shows weather in current city
        bot.reply_to(message, f'The weather is now: {temp} C')
        # inserting different images depending on what temperature is right now
        image = 'sunny.png' if temp > 10.0 else 'cloudy.png'
        file = open('./' + image, 'rb')
        # after getting file bot sends photo to user
        bot.send_photo(message.chat.id, file)
    # if request was unsuccesfull
    else:
        # bot replies to user that there is no such city
        bot.reply_to(message, f'There is no such city')


# main function that runs bot
def main():
    bot.polling(none_stop=True)


# checks if file runs from main module
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
