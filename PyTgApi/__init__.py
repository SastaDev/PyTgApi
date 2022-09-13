from . import exceptions
from . import methods
from . import parsing
import requests
import json
import time

r_s = requests.Session()

class TelegramBot:
    def __init__(self, bot_token):
        self.base_url = 'https://api.telegram.org/bot'
        self.bot_token = bot_token
        self.bot_url = f'https://api.telegram.org/bot{bot_token}'
        self.authorized = None
        self.parse_mode = 'markdown'
        self.allow_sending_without_reply = True
        self.link_preview = True
        self.run_forever = None
        self.commands_list = []
        self.commands_list_decorators = []
        self.GetUpdates = True
        self.total_sent = {
            'messages': 0,
            'photos': 0,
            'videos': 0
        }
        self.new_msg_update = []
        self.callback_query_update = []

    def start(self):
        auth = self.is_authorized(self.bot_token)
        if auth is True:
            self.authorized = False
            raise exceptions.UnAuthorizedBotToken('UnAuthorized Bot Token.')
        else:
            self.authorized = True

    def is_authorized(self, bot_token):
        r = requests.get(self.base_url + self.bot_token + '/getMe').json()
        if r['ok'] is False:
            return True
        else:
            return False

    def run_until(self, forever=True, time=None, polling_timeout=60):
        if forever is True:
            pass
        elif time:
            pass
        self.polling(timeout=polling_timeout)

    def polling(self, timeout=60):
        r = r_s.get(self.bot_url + '/getUpdates', data={})
        result = r.json()['result']
        if not result:
            offset = 1
        else:
            result = r.json()['result']
            old_updates = result
            offset = old_updates[-1]['update_id'] + 1
        while self.GetUpdates is True:
            d = {
                'offset': offset,
                'timeout': 60
            }
            r = r_s.get(self.bot_url + '/getUpdates', data=d, timeout=timeout)
            result = r.json().get('result')
            while not result:
                _d = {
                'offset': offset,
                'timeout': 60
                }
                r = r_s.get(self.bot_url + '/getUpdates', data=_d, timeout=timeout)
                result = r.json().get('result')
                _d['offset'] += 1
            self.send_update(update=result[-1])
            offset = result[-1]['update_id'] + 1

    def send_update(self, update):
        msg = parsing.ParseMessage(update, self)
        cb_q = self.callback_query_update
        for cb_q_ in cb_q:
            c = msg.get('callback_query')
            if not c:
                c = msg if msg.get('callback_query_id') else None
            if c:
                if cb_q_['data'] == c['data']:
                    cb_q_['function'](msg)
                    return
        cmds_list = self.commands_list_decorators
        for i in self.commands_list:
            cmds_list.append(i)
        for command in cmds_list:
            text = str(update['message'].get('text'))
            cmds = command['command']
            if not isinstance(cmds, list):
                cmds = [cmds]
            for cmd in cmds:
                cmd.pop(0) if cmd[0] == '/' else None
                text = text[1:] if text[0] == '/' else text
                s_text = text.split()
                if cmd == s_text[0]:
                    command['function'](msg)
        for function in self.new_msg_update:
            function['function'](msg)

    def add_command(self, command, function, add=True):
        d = {
            'command': str(command),
            'function': function
        }
        if add == False:
            return d
        self.commands_list.append(d)

    def getMe(self):
        r = requests.get(self.base_url + self.bot_token + '/getMe').json()
        if r['ok'] is False:
            self.unknown_exception(r)
        result = r.get(result)
        data = {
            'first_name': result.get('first_name'),
            'username': result.get('username'),
            'bot_id': result.get('id'),
            'is_bot': result.get('is_bot'),
            'can_join_groups': result.get('can_join_groups'),
            'can_read_all_group_messages': result.get('can_read_all_group_messages'),
            'supports_inline_queries': result.get('supports_inline_queries')
        }
        return data

    def unknown_exception(self, data):
        e = data['description'][13:] if data['description'] else data
        raise exceptions.UnKnownException(e)

    def check_out_error(self, data, url):
        m = parsing.parse_url(url)
        des = data['description'][13:]
        if des == 'chat not found':
            raise exceptions.ChatNotFound(f'Chat was not found: {m["chat_id"]}')
        elif des == 'message text is empty':
            raise exceptions.MessageTextEmpty('Empty message text is not allowed.')
        elif des == 'unsupported parse_mode':
            raise exceptions.UnSupportedParseMode(f'UnSupported Parse Mode: {m["parse_mode"]}')
        elif des == 'there is no photo in the request':
            raise exceptions.NoPhoto('No photo was found.')
        elif des == 'file must be non-empty':
            raise exceptions.FileMustBeNonEmpty('You must provide a valid, non-empty file.')
        elif des == 'IMAGE_PROCESS_FAILED':
            raise exceptions.ImageProcessFailed('Image Processing got failed.')
        else:
            self.unknown_exception(data)

    def on_update(self, command=None, new_message=False, callback_query=False):
        def update(func, command=command, new_message=new_message):
            if command:
                cmds = []
                if not isinstance(command, list):
                    command = [command]
                for cmd in command:
                    d = self.add_command(cmd, func, add=False)
                    cmds.append(d)
                for i in cmds:
                    self.commands_list_decorators.append(i)
            if new_message == True:
                d = self.add_new_msg_update(func, add=False)
                self.new_msg_update.append(d)
            if callback_query:
                d = self.add_callback_query(callback_query, func, add=False)
                self.callback_query_update.append(d)
        return update

    def add_new_msg_update(self, function, add=True):
        d = {
            'function': function
        }
        if add == False:
            return d
        self.new_msg_update.append(d)

    def add_callback_query(self, data, function, add=True):
        d = {
            'data': data,
            'function': function
        }
        if add == False:
            return d
        self.callback_query_update.append(d)

    def send_message(self, chat_id, text, reply_to=None, link_preview=None, buttons=None, parse_mode=None, **kwargs):
        return methods.sendMessage(self, chat_id=chat_id, text=text, reply_to=reply_to, link_preview=link_preview, buttons=buttons, parse_mode=parse_mode, **kwargs)

    def send_photo(self, photo, chat_id, caption, reply_to=None, link_preview=None, buttons=None, parse_mode=None, **kwargs):
        return methods.sendPhoto(self, photo=photo, chat_id=chat_id, caption=caption, reply_to=reply_to, link_preview=link_preview, buttons=buttons, parse_mode=parse_mode, **kwargs)

    def __repr__(self):
        return 'TelegramBot-Object.'

# from PyTgApi import buttons
from . import buttons
Button = buttons.Button

__version__ = '0.0.1'
__credits__ = '''
© Sasta Dev.

GitHub-Repo: https://github.com/SastaDev/PyTgApi.

PyTgApi support group on telegram: https://telegram.dog/HelpSupportChat.
'''