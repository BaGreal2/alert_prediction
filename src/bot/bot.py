from dotenv import load_dotenv
import datetime as dt
import os
import telebot
import json

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

COMMANDS = [
    {
        "name": 'start',
        "description": 'Restart the bot'
    },
    {
        "name": 'predict',
        "description": 'Get prediction for today'
    },
    {
        "name": 'day_prediction',
        "description": 'Get prediction for selected day'
    }
]

bot.set_my_commands(
    commands=[telebot.types.BotCommand(
        command["name"], command["description"]) for command in COMMANDS]
)


with open('probability_week.json', 'r') as prob_file:
    prob_data = json.load(prob_file)


weekdays = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']


@bot.message_handler(commands=[command["name"] for command in COMMANDS])
def exchange_command(message):
    if (message.text == '/start'):
        bot.send_message(
            message.chat.id, 'Glory to Ukraine🇺🇦! I can predict air raid alerts in Kyiv for you!🥰')

        commands_str = ''
        for command in COMMANDS:
            if (command["name"] == "start"):
                continue
            commands_str += f'/{command["name"]} - <i>{command["description"]}</i>\n'

        bot.send_message(
            message.chat.id,
            f'Here are the list of commands:\n{commands_str}',
            parse_mode='HTML')

    elif (message.text == '/predict'):
        curr_weekday = dt.datetime.now().weekday()

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton(
                'Show for hours', callback_data=f'hour_day-{curr_weekday}')
        )

        day = weekdays[curr_weekday]
        day_prob = "{:.2f}".format(
            round(prob_data[curr_weekday]["day_prob"] * 100, 2))

        bot.send_message(message.chat.id,
                         f'Alert probability for {day}: <b>{day_prob}%</b>',
                         reply_markup=keyboard, parse_mode='HTML')

    elif (message.text == '/day_prediction'):
        keyboard = telebot.types.InlineKeyboardMarkup()

        for weekday in weekdays:
            keyboard.row(
                telebot.types.InlineKeyboardButton(
                    weekday, callback_data=f'day-{weekdays.index(weekday)}')
            )

        bot.send_message(message.chat.id, 'Select a day:',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    keyboard = telebot.types.InlineKeyboardMarkup()
    data = query.data
    if (data.startswith('day-')):
        day_id = int(data[-1])
        day = weekdays[day_id]
        day_prob = "{:.2f}".format(
            round(prob_data[day_id]["day_prob"] * 100, 2))

        keyboard.row(
            telebot.types.InlineKeyboardButton(
                'Show for hours', callback_data=f'hour_day-{day_id}')
        )

        bot.send_message(query.message.chat.id, f'Alert probability for {day}: <b>{day_prob}%</b>',
                         reply_markup=keyboard, parse_mode='HTML')

    elif (data.startswith('hour_day-')):
        day_id = int(data[-1])
        day = weekdays[day_id]

        bot.send_message(query.message.chat.id,
                         f'Alert probability for {day} hours: ')

        str_hours = ''
        cnt = 0
        for hour_prob in prob_data[day_id]["hours_prob"]:
            if (hour_prob == 0):
                cnt += 1
                continue
            hour_string = '{:02d}:00'.format(cnt)
            hour_prob_string = "{:.2f}".format(round(hour_prob * 100, 2))
            str_hours += hour_string + \
                f': <b>{hour_prob_string}%</b>\n'
            cnt += 1
        bot.send_message(query.message.chat.id,
                         str_hours, parse_mode='HTML')


bot.infinity_polling()
