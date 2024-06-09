import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveHelper():
    '''
    This is a helper class to handle the Google drive
    '''

    def __init__(self) -> None:
        '''
        We set 2 instant parameters during initial instance.
        1. SCOPES: The permission to handle Google drive.
        2. credential: The credential to handle Google drive.

        Remark:
        - We can checks more functionality in the link below.
        https://developers.google.com/drive/api/guides/about-sdk
        - We can checks other scope by the link below.
        https://developers.google.com/drive/api/guides/api-specific-auth
        '''
        
        self.SCOPES = ["https://www.googleapis.com/auth/drive"]
        self.credential = None

    def get_credential(self):
        '''
        Get the credential for the specific permission to handle a Google drive.

        Remark: The credential with permission is set to the instance parameter
        credential. 
        '''
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
            with open("token.json", "w") as token:
                token.write(self.credential.to_json())

    def get_file_lists(self, page_size=20, name=''):
        '''
        Print file name and file id base on the the filter name.

        :param page_size int: The maximum number of searching file.
        :param name str: The filter contains name.
    
        Remark: We can check more query from the link below.
        https://developers.google.com/drive/api/guides/search-files#examples
        '''
        try:
            service = build("drive", "v3", credentials=self.credential)

            # Call the Drive v3 API
            results = (
                service.files()
                .list(
                    pageSize=page_size, 
                    fields="nextPageToken, files(id, name)",
                    q=f'name contains "{name}"' 
                    ).execute()
            )
            items = results.get("files", [])

            if not items:
                print("No files found.")
                return
            print("Files:")
            for item in items:
                print(f"filename:{item['name']} (id:{item['id']})")
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f"An error occurred: {error}")

    def upload_file(self,filename:str, filepath:str, filetype:str):
        '''
        Upload file to the Google drive

        :param str filename: The filename for save to the Google drive.
        :param str filepath: The file path in the local 
        :param str filetype: The file type of the upload file.
        '''
        service = build("drive", "v3", credentials=self.credential)
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,
                        mimetype=filetype)

        file = service.files().create(body=file_metadata, media_body=media,
                              fields='id').execute()
        
    def delete_file_by_id(self, file_id:str):
        '''
        Delete file in the Google drive by specific file id.

        :param str file_id: The file id of the expected delete file.
        '''
        service = build("drive", "v3", credentials=self.credential)
        service.files().delete(fileId=file_id).execute()

    def retrieve_meta_from_file_id(self, file_id:str):
        '''
        Get meta data of the file by file id.

        :param str file_id: The file id of the file that need to get meta data.
        '''
        service = build("drive", "v3", credentials=self.credential)
        file_metadata = service.files().get(fileId=file_id).execute()
        return file_metadata
    
    def share_file_permission(self, file_id:str, email:str):
        '''
        Share file permission to specific user.

        :param str file_id: The file id of the expected sharing file.
        :param str email: The email of the use that would like to share too.

        Remark: We can check the permission list in the file below.
        https://developers.google.com/drive/api/reference/rest/v3/permissions#Permission
        '''
        service = build("drive", "v3", credentials=self.credential)
        new_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress' : email,
        }
        try:
            service.permissions().create(fileId=file_id, body=new_permission, 
                                         transferOwnership=False).execute()
        except (AttributeError, HttpError) as error:
            print(F'An error occurred: {error}')
        
    def download_non_google_file(self, file_id:str):
        '''
        Download non google file from the Google drive by file id.

        :param str file_id: The file id of the expected download file.
        '''
        service = build("drive", "v3", credentials=self.credential)

        try: 
            request_file = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request_file)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')

            file_retrieved: str = file.getvalue()
            with open(f"downloaded_file.csv", 'wb') as f:
                f.write(file_retrieved)
        except HttpError as error:
            print(F'An error occurred: {error}')
    
    def download_google_file(self, file_id):
        '''
        Download non google file from the Google drive by file id.

        :param str file_id: The file id of the expected download file.

        Remark: We can check the file type to convert from the google file 
        (doc/sheet/ppt) to be a normal format in the link below.

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
        '''
        service = build("drive", "v3", credentials=self.credential)
        request_file = service.files().export_media(fileId=file_id
                                                    ,mimeType='text/csv').execute()
        with open(f"downloaded_file.csv", 'wb') as f:
            f.write(request_file)

    def get_folderid_by_name(self, folder_name:str):
        '''
        Get folder id by folder name.

        :param str folder_name: The folder name in the Google drive that would 
        like to get folder id.
        '''
        service = build("drive", "v3", credentials=self.credential)

        results = (
                service.files()
                .list(
                    pageSize=1000, 
                    fields="nextPageToken, files(id, name)",
                    q= "mimeType =" + "'application/vnd.google-apps.folder'"
                    ).execute()
            )
        
        items = results.get("files", [])

        for folder in items:
            if (folder["name"] == folder_name):
                return folder['id']

    def get_files_modify_after(self, modify_time:str):
        '''
        Get files that modify after specific period.

        :param str modify_time: The time in the string format.
        e.g. 2024-04-12T12:00:00
        '''
        service = build("drive", "v3", credentials=self.credential)

        results = (
                service.files()
                .list(
                    pageSize=1000, 
                    fields="nextPageToken, files(id, name)",
                    q= f"modifiedTime > '{modify_time}'" 
                    ).execute()
            )
        
        items = results.get("files", [])

        for file in items:
            print(file['name'])

    def get_files_in_folder(self, folder_id:str):
        '''
        Get file list in the specific folder.

        :param str folder_id: The folder that we would like to get list of file
        inside.
        '''
        service = build("drive", "v3", credentials=self.credential)

        results = (
                service.files()
                .list(
                    pageSize=1000, 
                    fields="nextPageToken, files(id, name)",
                    q= f"'{folder_id}' in parents" 
                    ).execute()
            )
        
        items = results.get("files", [])

        for file in items:
            print(file['name'])

    def get_iframe_with_attached_item(self, item_id):
        '''
        Get the iframe with the attached item from Google drive.

        :param str item_id: The item that need to attached with the iframe.
        :return str: The html element of iframe with attached item.
        '''
        return f'<iframe src="https://drive.google.com/file/d/{item_id}/preview" width="640" height="480" allow="autoplay"></iframe>'

    def get_share_link(self, file_id:str):
        '''
        Get the shareable link from the specific file by file id.

        :param str file_id: The file id of the sharing file.
        :return: The urls of the sharing file.
        '''
        return f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'

    def get_link_share_spread_sheet(self, spread_sheet_id:str):
        '''
        Get the shareable link of spread sheet from the spread sheet id.

        :param str spread_sheet_id: The id of spread sheet that need to share.
        '''
        return f'https://docs.google.com/spreadsheets/d/{spread_sheet_id}/edit?usp=sharing'