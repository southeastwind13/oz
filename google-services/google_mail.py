import os.path
import base64
import mimetypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

class GoogleMailHelper():
    '''
    Helper class to handle Google mail.
    
    - You can find more details about google mail API from the link below.
    https://developers.google.com/gmail/api/guides/drafts
    - You can read about SCOPES of credentials in the link below.
    https://developers.google.com/gmail/api/auth/scopes
    - Read more about search parameters.
    https://support.google.com/mail/answer/7190
    '''

    def __init__(self) -> None:
        self.SCOPES = ["https://mail.google.com/"]
        self.credential = None

    def get_credential(self):
        '''
        Get the credential to handel the Google mail.
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
            with open("token.json", "w", encoding="utf-8") as token:
                token.write(self.credential.to_json())

    def get_labels(self):
        '''
        Get all labels in the specific email.

        :return: The list of labels.
        '''
        service = build("gmail", "v1", credentials=self.credential)

        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return

        return [label["name"] for label in labels]

    def create_draft_email(self, to_email:str, from_email:str, subject:str, content:str):
        service = build("gmail", "v1", credentials=self.credential)

        message = EmailMessage()

        message.set_content(content)
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message}}
        # pylint: disable=E1101
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')


    def send_email(self, to_email:str, from_email:str, subject:str, content:str, attachments:list):
        """
        Send an email using the Gmail API.

        Args:
            to_email (str): The email address to send the email to.
            from_email (str): The sender's email address.
            subject (str): The subject of the email.
            content (str): The content of the email.
            attachments (list): A list of file paths for attachments.

        Returns:
            None
        """
        service = build("gmail", "v1", credentials=self.credential)

        message = EmailMessage()

        message.set_content(content)
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = subject

        if attachments:
            for attachment in attachments:

                # attachment
                attachment_filename = attachment
                filename = GoogleMailHelper._get_file_name_from_path(attachment_filename)

                # guessing the MIME type
                type_subtype, _ = mimetypes.guess_type(attachment_filename)
                maintype, subtype = type_subtype.split("/")

                with open(attachment_filename, 'rb') as content_file:
                    type_subtype, _ = mimetypes.guess_type(attachment_filename)
                    maintype, subtype = type_subtype.split("/")

                    content = content_file.read()
                    message.add_attachment(content, maintype=maintype, subtype=subtype , filename=f"{filename}.{subtype}")

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        print(f'Message Id: {send_message["id"]}')

    def read_message(
            self, 
            email_from:str='', 
            after_time:str='', 
            label:str='',
            number_of_messages:int=2,
            is_download_attachment=False):
        service = build("gmail", "v1", credentials=self.credential)

        # Prepare query message
        query_message = 'is:unread'

        if email_from != '':
            query_message += f' from:{email_from}'
        
        if after_time != '':
            query_message += f' after:{after_time}'

        if label != '':
            query_message += f' label:{label}'

        results = service.users().messages().list(
            userId='me', 
            # labelIds=[''], 
            q=query_message 
            ).execute()
        
        messages = results.get('messages',[])

        mails = []

        for idx, message in enumerate(messages):
            if idx >= number_of_messages:
                break
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']

            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value'] 
                if name == 'Subject':
                    subject = values['value']
                if name == 'Date':
                    date = values['value']

            if 'parts' in msg['payload']:
                complete = False
                parts = msg['payload']['parts']

                # Get data content from the content-type text
                while not complete:

                    headers = parts[0]['headers']
                
                    for value in headers:
                        name = value['name']
                        if name == 'Content-Type':
                            content_type = value['value']
                            if 'text' in content_type:
                                complete = True
                                data = parts[0]['body']['data']
                            else:
                                parts = parts[0]['parts']
            else:
                data = data = msg['payload']['body']['data']

            
            byte_code = base64.urlsafe_b64decode(data)
            text = byte_code.decode("utf-8")

            if is_download_attachment:

                number_of_files = len(msg['payload']['parts']) - 1

                for idx in range(number_of_files):
                                        
                    attchment_id = msg['payload']['parts'][idx + 1]['body']['attachmentId']
                    file_name = msg['payload']['parts'][idx + 1]['filename']
                
                
                    # print(len(msg['payload']['parts']))
                
                    attachment = service.users().messages().attachments().get(
                        userId="me", messageId=message['id'], id=attchment_id
                    ).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

            
                    if file_data:
                        #do some staff, e.g.
                        path = f'Google/download/{file_name}'
                        print(path)
                        with open(path, 'wb') as f:
                            f.write(file_data)

            mails.append({
                'from': from_name,
                'subject': subject,
                'date': date,
                'content': text
            })
        return mails

    def _get_file_name_from_path(file_path:str):
        '''
        Private function for get filename without extension from the filepath.

        :param str file_path: The path of the file.
        :return: The file name without extension.

        e.g. 
        input /google/test/picture.png
        return picture
        '''
        if '/' in file_path:
            split_file_path = file_path.split('/')
            if '.' in split_file_path[-1]:
                split_file_name = split_file_path[-1].split('.')
                return(split_file_name[-2])
            else:
                return(split_file_path[-1])
        elif '.' in file_path:
            split_file_name = file_path.split('.')
            return(split_file_name[-2])
        else:
            return(file_path)