import json

class Button:
    def __init__():
        pass

    def inline(text, callback_data):
        d = {
            'text': text,
            'callback_data': callback_data
        }
        return d

    def url(text, url):
        d = {
            'text': text,
            'url': url
        }
        return d

def decode_buttons(buttons):
    btns = []
    for button in buttons:
        if isinstance(button, list):
            for b in button:
                print(b)
        else:
            btns.append(button)
    return btns