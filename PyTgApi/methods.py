import requests
from . import parsing
import json

r_s = requests.Session()

class sendMessage:
    def __init__(self, bot, chat_id, text, reply_to=None, link_preview=None, buttons=None, parse_mode=None, **kwargs):
        self.bot = bot
        self.chat_id = parsing.ParseChat(chat_id, bot, getChatID=True)
        self.text = text
        self.reply_to = reply_to
        self.link_preview = link_preview or bot.link_preview
        self.buttons = buttons
        self.parse_mode = parse_mode or bot.parse_mode

        url = ''
        for kwarg in kwargs:
            url += f'&{kwarg}={kwargs[kwarg]}'
        self.extra_kwargs = url
        self.send_message()

    def send_message(self):
        url = f'/sendMessage?chat_id={self.chat_id}&text={self.text}&parse_mode={self.parse_mode}'
        url += self.extra_kwargs
        if self.reply_to:
            url += f'&reply_to_message_id={self.reply_to}&allow_sending_without_reply={self.bot.allow_sending_without_reply}'
        if self.buttons:
            btns = parsing.parse_buttons(self.buttons)
            btns = json.dumps({"inline_keyboard": btns})
            url += f'&reply_markup={btns}'
        if self.link_preview is not None:
            url += f'&disable_web_page_preview={self.link_preview}'
        r = r_s.get(self.bot.bot_url + url).json()
        if r['ok'] is False:
            self.bot.check_out_error(r, url)
        self.bot.total_sent['messages'] += 1
        result = r['result']
        returned_message = parsing.ParseMessage(data=result, bot=self.bot)
        return returned_message

class sendPhoto:
    def __init__(self, bot, photo, chat_id, caption, reply_to=None, link_preview=None, buttons=None, parse_mode=None, **kwargs):
        self.bot = bot
        self.photo = photo
        self.chat_id = parsing.ParseChat(chat_id, getChatID=True)
        self.caption = caption
        self.reply_to = reply_to
        self.link_preview = link_preview or bot.link_preview
        self.buttons = buttons
        self.parse_mode = parse_mode or bot.parse_mode
        url = ''
        for kwarg in kwargs:
            url += f'&{kwarg}={kwargs[kwarg]}'
        self.extra_kwargs = url
        self.send_photo()

    def send_photo(self):
        url = f'/sendPhoto?chat_id={self.chat_id}&caption={self.caption}&parse_mode={self.parse_mode}'
        url += self.extra_kwargs
        if self.reply_to:
            url += f'&reply_to_message_id={self.reply_to}&allow_sending_without_reply={self.bot.allow_sending_without_reply}'
        if self.buttons:
            btns = parsing.parse_buttons(self.buttons)
            btns = json.dumps({"inline_keyboard": btns})
            url += f'&reply_markup={btns}'
        if self.link_preview is not None:
            url += f'&disable_web_page_preview={self.link_preview}'
        file = {'photo': self.photo}
        r = r_s.post(self.bot.bot_url + url, files=file).json()
        if r['ok'] is False:
            self.bot.check_out_error(r, url)
        self.bot.total_sent['messages'] += 1
        result = r['result']
        returned_message = parsing.ParseMessage(data=result, bot=self.bot)
        return returned_message