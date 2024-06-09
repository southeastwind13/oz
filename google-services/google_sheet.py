import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

class GoogleSheetHelper():
    '''
    Helper class to handle Google sheet.
    
    - You can find more details about google sheet API from the link below.
    https://developers.google.com/sheets/api/guides/create
    - You can read about SCOPES of credentials in the link below.
    https://developers.google.com/sheets/api/scopes
    '''

    def __init__(self) -> None:
        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        self.credential = None

    def get_credential(self):
        '''
        Need google credential to authorize before using the Google API.
        '''

        try:
            if os.path.exists("token.json"):
                self.credential = Credentials.from_authorized_user_file("token.json", self.SCOPES)

            # If there are no (valid) credentials available, let the user log in.
            if not self.credential or not self.credential.valid:
                if self.credential and self.credential.expired and self.credential.refresh_token:
                    self.credential.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "Google/credentials.json", self.SCOPES
                )
                    self.credential = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open("token.json", "w", encoding="utf-8") as token:
                    token.write(self.credential.to_json())

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def create_spreadsheet(self, title:str):
        try:
            service = build(
                serviceName='sheets',
                version='v4',
                credentials=self.credential,
                cache_discovery=False).spreadsheets()
            
            body = {"properties": {"title": title}}
            spreadsheet = (
                service.create(body=body, fields="spreadsheetId")
                .execute())
            
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
            return spreadsheet.get("spreadsheetId")
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def read_data_from_sheet_single_range(self, sheet_id:str, range:str):
        # Create service
        service = build(
            serviceName='sheets',
            version='v4',
            credentials=self.credential,
            cache_discovery=False).spreadsheets()
        
        range = range # 'Sheet1!A:B'
        result = service.values().get(spreadsheetId=sheet_id, range=range).execute()
        data = result.get('values', [])
        df = pd.DataFrame(data[1:], columns=data[0])
        print(df.head())

    def read_data_from_sheet_multiple_ranges(self, sheet_id:str, ranges:list):
        # Create service
        service = build(
            serviceName='sheets',
            version='v4',
            credentials=self.credential,
            cache_discovery=False).spreadsheets()
        
        range = ranges # 'Sheet1!A:B'
        result = service.values().batchGet(spreadsheetId=sheet_id, ranges=range).execute()
        # data = result.get('valueRanges', [])
        # df = pd.DataFrame(data[0]['values'][1:], columns=data[0]['values'][0])
        # print(df.head())
        ranges = result.get("valueRanges", [])
        print(f"{len(ranges)} ranges retrieved")
        return result

    def write_data_to_sheet(self, sheet_id:str, range:str, data:pd.DataFrame):

        service = build(
            'sheets',
            'v4',
            credentials=self.credential,
            cache_discovery=False).spreadsheets()

        # [1: ] to exclude the header
        data_to_write: list = data.T.reset_index().values.T.tolist()[1:]

        service.values().clear(spreadsheetId=sheet_id,
                                            range=range).execute()
        
        service.values().update(spreadsheetId=sheet_id,
                                        range=range,
                                        valueInputOption="USER_ENTERED",
                                        body={"values": data_to_write}).execute()
        
    def append_values(self, sheet_id:str, range_name, _values, value_input_option):
        service = build(
            'sheets',
            'v4',
            credentials=self.credential,
            cache_discovery=False).spreadsheets()
            
        values =_values
        
        body = {"values": values}

        result = (
            service
            .values()
            .append(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute())