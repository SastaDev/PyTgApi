# callback_query_data.py
# Once the user send /start, bot will reply user with inline keyboard buttons to that '/start' sent message.
# Once user click on any inline keyboard button the callback query which matched the data in on_update(callback='our data') will be executed and user will reciever a message containing 'You've chosen yes (or no).*

# Import TelegramBot and Button.
from PyTgApi import TelegramBot, Button

bot_token = 'your bot token here.' # get it from @BotFather on telegram.

bot = TelegramBot(bot_token=bot_token)

@bot.on_update(command='start')
def on_start(message):
    buttons = [
        [Button.inline('Yes', 'yes')],
        [Button.inline('No', 'no')]
        ]
    message.reply('**Example of inline keyboard buttons with callback query data**', buttons=buttons)

@bot.on_update(callback_query='yes')
def on_yes(message):
    message.reply('**You\'ve clicked:** Yes.')

@bot.on_update(callback_query='no')
def on_no(message):
    message.reply('**You\'ve clicked:** No.')

bot.start()
bot.run_until(forever=True)
