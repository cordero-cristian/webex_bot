import requests
import json
from logging_functions import logger

CERT_PATH = '/etc/pki/tls/certs/ca-bundle.crt'


class request_functions_session():

    def __init__(self, baseUrl, authTuple, pathToCert=CERT_PATH):
        # set our logger
        self.logger = logger.logger()
        # set our base URL
        self.baseUrl = baseUrl
        # init a session obj
        self.apiSession = requests.session()
        # define our auth header
        self.apiSession.auth = authTuple
        # define our cert
        self.apiSession.verify = pathToCert
        # add our content type to header
        self.apiSession.headers.update({'Content-Type': 'application/json'})

    def get_request(self, apiURI):
        apiUrl = f"{self.baseUrl}" + apiURI
        self.logger.log_debug(f"attempting to send a GET request to {apiUrl}")
        apiResponse = self.apiSession.get(apiUrl)
        self.statusCode = apiResponse.status_code
        return apiResponse.json()


class request_functions_base():

    def __init__(self, authDict, pathToCert=CERT_PATH):
        self.headers = dict()
        self.headers.update(authDict)
        self.headers.update({'Content-Type': 'application/json'})
        self.certPath = pathToCert

    def get_request(self, url):
        response = requests.get(url, headers=self.headers, verify=self.certPath)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            self.logger.log_debug('response from get request was invlaid json or None')
            return response

    def post_request(self, url, data):
        response = requests.post(
                        url,
                        headers=self.headers,
                        data=json.dumps(data),
                        verify=self.certPath
                        )
        return response




