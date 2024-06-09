from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

class GoogldAuthHelper():
    '''
    Helper for process Authentication with the google service.
    '''

    @staticmethod
    def get_authentication(client_secret_path:str, keep_auth=True, scopes=None):
        '''
        Get the credential for access G-Service by specific scopes.

        :param str client_secret_path: The path of create client_secret.json.
        :param bool keep_auth: 
        :param scopes list: List of services. 

        '''

        credentials:Credentials = None

        # set default scope
        if not scopes:
            scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

        # get authentication from existing token
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', scopes)

        if credentials and credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, scopes)
            credentials = flow.run_local_server(port=0)
                
        if keep_auth:
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        return credentials