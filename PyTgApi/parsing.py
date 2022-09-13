import requests

def parse_url(url):
    query = requests.utils.urlparse(url).query
    params = dict(x.split('=') for x in query.split('&'))
    return params

def parse_buttons(buttons):
    try:
        buttons = buttons[0][0]
    except:
        buttons = [buttons]
    return buttons

def ParseMessage(data, bot, parse_to_object=True):
    if data.get('message'):
        original_data = data
        data = data.get('message')
    elif data.get('edited_message'):
        original_data = data
        data = data.get('edited_message')
    elif data.get('callback_query'):
        return ParseCallBackQuery(data, bot, parse_to_object=False)
    _from = data.get('from')
    msg = {
        'message': {
            'message_id': data.get('message_id'),
            'text': data.get('text'),
            'date': data.get('date'),
        },
        'from_user': {
            'first_name': _from.get('first_name'),
            'last_name': _from.get('last_name'),
            'username': _from.get('username'),
            'user_id': _from.get('id'),
            'is_bot': _from.get('is_bot'),
            'language_code': _from.get('language_code')
        },
        'entities': data.get('entities'),
        'reply_markup': data.get('reply_markup'),
        'chat_id': _from.get('user_id'),
        'sender_id': _from.get('user_id')
    }
    if data.get('chat'):
        chat = data.get('chat')
        if str(chat.get('id')).startswith('-100'):
            d = ParseChat(chat, bot, parse_to_object=False)
            msg['chat_id'] = d['chat']['chat_id']
        else:
            d = ParsePrivate(chat, bot, parse_to_object=False)
            msg['chat_id'] = d['chat']['user_id']
            msg['sender_id'] = d['chat']['user_id']
        msg.update(d)
    return Message(**msg, bot=bot) if parse_to_object else msg

class Message:
    def __init__(self, bot, **msg):
        self.bot = bot
        self.msg = msg
        self.__dict__.update(msg)

    def __repr__(self):
        return str(self.msg)

    def get(self, key_name):
        return self.__dict__.get(key_name)

    def reply(self, text):
        chat_id = self.msg['chat_id']
        self.bot.send_message(chat_id, text, reply_to=self.msg['message']['message_id'])

def ParsePrivate(data, bot, parse_to_object=True):
    d = {
        '_': 'private',
        'type': data.get('type'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'username': data.get('username'),
        'user_id': data.get('id')
    }
    d = {'chat': d}
    return d

def ParseChat(data, bot, parse_to_object=True, getChatID=False):
    if str(data.get('_')) == 'private' or str(data.get('type')) == 'private':
        d = data
        d['chat_id'] = data.get('user_id')
    else:
        chat = data.get('chat') if data.get('chat') else data
        d = {
            '_': 'chat',
            'type': chat.get('type'),
            'title': chat.get('title'),
            'chat_id': chat.get('id') or chat.get('chat_id')
        }
    d = {'chat': d}
    return d['chat'].get('chat_id') if getChatID else d

def ParseUser(data, bot, parse_to_object=True):
    original_data = data
    data = data.get('from') or data.get('from_user') or original_data
    msg = {
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'username': data.get('username'),
        'user_id': data.get('id'),
        'is_bot': data.get('is_bot'),
        'language_code': data.get('language_code')
    }
    d = {'from_user': msg}
    return d

def ParseCallBackQuery(data, bot, parse_to_object=True):
    original_data = data
    data = data.get('callback_query') or original_data
    msg = {
        'callback_query_id': data.get('id'),
        'from_user': ParseUser(data.get('from'), bot, parse_to_object=False)['from_user'],
        'message': {
            'message_id': data.get('message').get('message_id'),
            'from_user': ParseUser(data.get('from'), bot, parse_to_object=False)['from_user'],
            'chat': ParseChat(data['message'].get('chat'), bot, parse_to_object=False)
        },
        'chat_instance': data.get('chat_instance'),
        'data': data.get('data')
    }
    d = {'callback_query': msg}
    return d