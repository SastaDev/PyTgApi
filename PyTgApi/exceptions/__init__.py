class UnAuthorizedBotToken(Exception):
    pass

class UnKnownException(Exception):
    pass

class ChatNotFound(Exception):
    pass

class MessageTextEmpty(Exception):
    pass

class UnSupportedParseMode(Exception):
    pass

class NoPhoto(Exception):
    pass

class FileMustBeNonEmpty(Exception):
    pass

class ImageProcessFailed(Exception):
    pass
