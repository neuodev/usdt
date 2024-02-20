import os
import telebot
from store import Store, UserStore
from telebot import types
from telebot import formatting
from telebot.types import InputFile
from plot import plot_price
from snapshot import MarketSnapshot
import threading

token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(token)
store = Store("data.json")
user_store = UserStore("users.json")


@bot.message_handler(commands=['start', 'hello', 'add'])
def send_welcome(message: types.Message):
    user_store.add_unique(message.chat.id)
    bot.reply_to(message, "Welcome to Dinaro!")


@bot.message_handler(commands=['price'])
def send_price(message: types.Message):
    snapshots = store.load()
    text = format_usd_price_message(snapshots)
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


#! disabled for now
# @bot.message_handler(commands=['binance'])
# def send_snapshot(message: types.Message):
#     snapshots = store.load()
#     if len(snapshots) == 0:
#         return bot.send_message(message.chat.id, "Currently, there is no data.")

#     snapshot = snapshots[len(snapshots) - 1]
#     bot.send_photo(
#         message.chat.id, InputFile(snapshot.screenshot))


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


def format_usd_price_message(snapshots: list[MarketSnapshot]):
    if len(snapshots) == 0:
        return 'Currently, there is no prices.'

    snapshot = snapshots[-1]
    max_trader = snapshot.traders[0]

    return formatting.format_text(
        "Max USD Price: {} EGP with supply ${}".format(
            max_trader.price, max_trader.supply),
        "Avg. USD Price: {} EGP".format(snapshot.avg_price),
        "Captured At: {}".format(snapshot.date),
        separator="\n\n"
    ),


class ThreadJob(threading.Thread):
    def __init__(self, callback, event, interval):
        self.callback = callback
        self.event = event
        self.interval = interval
        super(ThreadJob, self).__init__()

    def run(self):
        while not self.event.wait(self.interval):
            self.callback()


event = threading.Event()


def broadcast_prices():
    users = user_store.load()
    snapshots = store.load()
    message = format_usd_price_message(snapshots)

    for user in users:
        bot.send_message(user, message, parse_mode="Markdown")


k = ThreadJob(broadcast_prices, event, 5 * 60)  # 5min
k.start()

print('Bot started...')
bot.infinity_polling()
