import os
import telebot
from store import Store
from telebot import types
from telebot import formatting
from telebot.types import InputFile
from plot import plot_price

token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(token)
store = Store("data.json")


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['price'])
def send_price(message: types.Message):
    snapshots = store.load()
    if len(snapshots) == 0:
        return bot.send_message(message.chat.id, "Currently, there is no data.")

    snapshot = snapshots[len(snapshots) - 1]

    bot.send_message(message.chat.id,
                     formatting.format_text(
                         formatting.mbold(
                             "Avg. USD Price: {}".format(snapshot.avg_price)
                         ),
                         separator="\n"
                     ),
                     parse_mode="MarkdownV2")


@bot.message_handler(commands=['binance'])
def send_snapshot(message: types.Message):
    snapshots = store.load()
    if len(snapshots) == 0:
        return bot.send_message(message.chat.id, "Currently, there is no data.")

    snapshot = snapshots[len(snapshots) - 1]
    bot.send_photo(
        message.chat.id, InputFile(snapshot.screenshot))


@bot.message_handler(commands=['data'])
def send_data(message: types.Message):
    bot.send_document(
        message.chat.id,
        InputFile("data.json"),
        caption="All collected data"
    )

@bot.message_handler(commands=['graph'])
def send_plot(message: types.Message):
    snapshots = store.load()
    filename = "plot.png"
    plot_price(filename, snapshots)
    bot.send_photo(
        message.chat.id,
        InputFile(filename),
        caption="Price Hisotry"
    )
    os.remove(filename)



print('Bot started...')
bot.infinity_polling()
