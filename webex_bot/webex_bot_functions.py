from logging_functions import logger
from webex_bot.message_functions import messenger
from request_functions.request_functions import request_functions_base
from webex_bot.creds import apiKey
import time
from pprint import pprint
API_URL = 'https://webexapis.com/v1/'
FLEX_WEBEX_ORG_ID = 'Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi84MWRmNDA2MC0zNjU0LTRjZmYtYTNhYi05NDZkMDkxMDY4MGY'
DEFAULT_GROUP_TITLE = 'Network Automation Team'

class webex_bot_functions():

    def __init__(self):
        self.messenger = messenger(base_url=API_URL, api_key=apiKey)
        self.logger = logger.logger()
        self.headers = {
            "Authorization": f"Bearer {apiKey}"
        }
        self.requestsFuncs = request_functions_base(authDict=self.headers)

    def find_person_id(self, firstname, lastname):
        displayName = f'{firstname} {lastname}'
        url = f'{API_URL}people?displayName={displayName}&orgId={FLEX_WEBEX_ORG_ID}'
        res = self.requestsFuncs.get_request(url)
        self.person_id = res['items'][0]['id']
        self.person_email = res['items'][0]['emails'][0]

    def get_group_self(self):
        self.groupRooms = list()
        url = f'{API_URL}rooms?type=group'
        res = self.requestsFuncs.get_request(url)
        for group in res['items']:
            self.groupRooms.append({
                'id': group['id'],
                'title': group['title']
            })

    def send_message(self, text, personid=None, group=False, groupTitle=None, markdown=False):
        if personid is not None and groupTitle is not None:
            raise ValueError(
                "Please only use personid or groupTitle"
            )
        if groupTitle is not None:
            if not isinstance(groupTitle, str):
                raise ValueError(
                    "groupTitle must be a str!"
                )
            if not hasattr(self, 'groupRooms'):
                self.get_group_self()
            for idx, group in enumerate(self.groupRooms):
                if group['title'] == groupTitle:
                    roomId = self.groupRooms[idx]['id']
                    self.messenger.post_message(text, room_id=roomId, markdown=markdown)
        if group is True and groupTitle is None:
            if not hasattr(self, 'groupRooms'):
                self.get_group_self()
            for group in self.groupRooms:
                if group['title'] == DEFAULT_GROUP_TITLE:
                    roomId = self.groupRooms[0]['id']
                    self.messenger.post_message(text, room_id=roomId, markdown=markdown)
        if personid is not None:
            self.messenger.post_message(text, person_id=personid, markdown=markdown)

    def check_for_new_message(self, roomId=None):

        if roomId is None:

            if not hasattr(self, 'groupRooms'):
                self.get_group_self()
            for group in self.groupRooms:
                if group['title'] == DEFAULT_GROUP_TITLE:
                    roomId = self.groupRooms[0]['id']
            else:
                roomId = self.groupRooms[0]['id']
        
        url = f'{API_URL}messages?roomId={roomId}&mentionedPeople=me'
        resp = self.requestsFuncs.get_request(url)
        if hasattr(self, 'last_message_id'):


            try:
                if resp['items'][0]['id'] == self.last_message_id:
                    return None
                else:
                    return resp
            except KeyError:
                self.logger.log_error(f'could not hit API response: {resp}')
                return None
        
        return resp

    def get_latest_commands(self, roomId = None):

        self.allMessages = self.check_for_new_message(roomId)
        commandsToRunList = list()

        if self.allMessages is None:
            self.logger.log_info('no commands to process !')
            return None

        self.last_message_time = self.allMessages['items'][0]['created']
        self.last_message_id = self.allMessages['items'][0]['id']

        for message in self.allMessages['items']:
            commandsToRunList.append(
            (
            message['text'],
            message['personId']
            )
            )


            
            return commandsToRunList

    

