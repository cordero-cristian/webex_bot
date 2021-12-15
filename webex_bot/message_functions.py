import json
import requests
from logging_functions import logger
from request_functions.request_functions import request_functions_base


class messenger():
    def __init__(self, base_url, api_key):
        # print(base_url, api_key)
        if base_url is None or api_key is None:
            raise ValueError(
                "base_url or api_key was undefined "
            )
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}"
        }
        self.requestsFuncs = request_functions_base(authDict=self.headers)
        self.bot_id = self.requestsFuncs.get_request(
                                    f'{self.base_url}/people/me',
                                    ).get('id')
        self.logger = logger.logger()

    def get_message(self, message_id):
        """ Retrieve a specific message, specified by message_id """
        received_message_url = f'{self.base_url}/messages/{message_id}'
        self.message_text = requests.get(
                                        received_message_url,
                                        headers=self.headers
                                        ).get('text')

    def post_message(self, message, room_id=None, person_id=None, markdown=False):
        """ Post message to a Webex Teams space, specified by room_id  or person_id"""
        if room_id is not None and person_id is not None:
            raise ValueError(
                "Please only use room id or person id"
            )
        textOrMarkDown = "text"
        if markdown is True:
            textOrMarkDown = "markdown"
        if room_id is not None:
            data = {
                "roomId": room_id,
                textOrMarkDown: message,
                }
        else:
            data = {
                "toPersonId": person_id,
                textOrMarkDown: message,
                }
        post_message_url = f'{self.base_url}/messages'
        post_message = self.requestsFuncs.post_request(
                                    post_message_url,
                                    data=data
                                    )
        if post_message.status_code != 200:
            self.logger.log_error(
                                    'unable to send message \n'
                                    f'error code: {post_message.status_code}'
                                    f'{post_message.text}'
                                    )