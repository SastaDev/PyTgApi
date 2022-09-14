# inline_keyboard_buttons.py
# Once the user send /start, bot will reply user with inline and url keyboard buttons to that '/start' sent message.

# Import TelegramBot and Button.
from PyTgApi import TelegramBot, Button

bot_token = 'your bot token here.' # get it from @BotFather on telegram.

bot = TelegramBot(bot_token=bot_token)

@bot.on_update(command='start')
def on_start(message):
    buttons = [
        [Button.inline('Inline Button 1', 'callback_data')],
        [Button.url('Telegram', 'https://telegram.org'),
        Button.url('GitHub', 'https://github.com')],
        [Button.inline('Inline Button 2')]
        ]
    message.reply('**Example of inline and url keyboard buttons.**', buttons=buttons)

bot.start()
bot.run_until(forever=True)
