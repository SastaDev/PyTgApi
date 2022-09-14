# Hello.py
# Once the user send /start, bot will reply 'hello.' to that '/start' sent message.

from PyTgApi import TelegramBot

bot_token = 'your bot token here.' # get it from @BotFather on telegram.

bot = TelegramBot(bot_token=bot_token)

@bot.on_update(command='start')
def on_start(message):
    message.reply('Hello.')

bot.start()
bot.run_until(forever=True)
