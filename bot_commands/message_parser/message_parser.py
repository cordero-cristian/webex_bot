from logging_functions.logger import logger

class webex_message_parser():
    def __init__(self):
        self.logger = logger()

    def parse_webex_message(self, message):
        returnDict = dict()
        messageParts = message.split()
        returnDict['botName'] = messageParts[0]
        returnDict['command'] = messageParts[1]
        try:
            returnDict['param1'] = messageParts[2]
        except IndexError:
            return returnDict
        if len(messageParts) == 3:
            return returnDict
        elif len(messageParts) == 4:
            returnDict['param2'] = messageParts[3]
            return returnDict
        elif len(messageParts) == 5:
            returnDict['param3'] = messageParts[4]
            return returnDict