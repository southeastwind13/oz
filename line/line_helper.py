
import requests
from requests.models import Response, to_key_val_list
from requests.sessions import Request

class LineHelper():
    
    @classmethod
    def _line_notify(cls, token, payload, file=None):
        '''
        Send line notification with payload.

        :param str token: The token of line notification.
        :param dict payload: The object that send with line notification.
        :param file file: The file that send with line notification.

        :return: 
        '''
        url = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization':'Bearer '+token}
        result = requests.post(url, headers=headers , data = payload, files=file)
        if result.status_code != 200:
            print('*'*50)
            print(f'Have something go wrong: {result.content}')
            print('*'*50)
        return result

    @staticmethod
    def notify_message(token, msg):
        '''
        Send line notification with message.

        :param str token: The token of line notification.
        :param str msg: The message that send with line notification.
        '''

        payload = {'message': msg}
        LineHelper._line_notify(token, payload)

    @staticmethod
    def notify_image_file(token, msg, image_path):
        '''
        Send line notification with image from local.

        :param str token: The token of line notification.
        :param str msg: The message that send with line notification.
        :param str image_path: The path of image that send with line notification.
        '''

        file = {'imageFile':open(image_path,'rb')}
        payload = {'message': msg}
        LineHelper._line_notify(token, payload, file)

    @staticmethod
    def notify_image_url(token, msg, imge_url):
        '''
        Semd line notification with image from url

        :param str token: The token of line notification.
        :param str msg: The message that send with line notification.
        :param str image_url: The url of image that send with line notification.
        '''
        payload = {'message':msg,
                   'imageThumbnail':imge_url,
                   'imageFullsize':imge_url
                   }
        LineHelper._line_notify(token, payload)

    @staticmethod
    def notify_sticker(token, msg, sticker_id, sticker_package_id):
        '''
        Semd line notification with line sticker.
        https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions

        :param str token: The token of line notification.
        :param str msg: The message that send with line notification.
        :param int sticker_id: The sticker id
        :param int sticker_package_id: The sitcker package id
        '''
        payload = {'message':msg,
                   'stickerPackageId':sticker_package_id,
                   'stickerId':sticker_id
                   }
        LineHelper._line_notify(token, payload)