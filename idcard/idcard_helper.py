
#  install pcscd python-pyscard python-pil
import os
import io
import binascii
import sys
#import traits
import codecs
from PIL import Image
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes

'''
Declare common address of IDcard reader
'''
# Check card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
# CID
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
# TH Fullname
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
# EN Fullname
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
# Date of birth
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
# Gender
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
# Card Issuer
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]
# Issue Date
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]
# Expire Date
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]
# Address
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
# Photo_Part1/20
CMD_PHOTO1 = [0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF]
# Photo_Part2/20
CMD_PHOTO2 = [0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF]
# Photo_Part3/20
CMD_PHOTO3 = [0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF]
# Photo_Part4/20
CMD_PHOTO4 = [0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF]
# Photo_Part5/20
CMD_PHOTO5 = [0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF]
# Photo_Part6/20
CMD_PHOTO6 = [0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF]
# Photo_Part7/20
CMD_PHOTO7 = [0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF]
# Photo_Part8/20
CMD_PHOTO8 = [0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF]
# Photo_Part9/20
CMD_PHOTO9 = [0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF]
# Photo_Part10/20
CMD_PHOTO10 = [0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF]
# Photo_Part11/20
CMD_PHOTO11 = [0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF]
# Photo_Part12/20
CMD_PHOTO12 = [0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF]
# Photo_Part13/20
CMD_PHOTO13 = [0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF]
# Photo_Part14/20
CMD_PHOTO14 = [0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF]
# Photo_Part15/20
CMD_PHOTO15 = [0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF]
# Photo_Part16/20
CMD_PHOTO16 = [0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF]
# Photo_Part17/20
CMD_PHOTO17 = [0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF]
# Photo_Part18/20
CMD_PHOTO18 = [0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF]
# Photo_Part19/20
CMD_PHOTO19 = [0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF]
# Photo_Part20/20
CMD_PHOTO20 = [0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF]

# Thailand ID Smartcard
def thai2unicode(data):
    result = ''
    result = bytes(data).decode('tis-620').replace("#", " ")
    return result.strip();

def getData(cmd, connection, req = [0x00, 0xc0, 0x00, 0x00]):
    data, sw1, sw2 = connection.transmit(cmd)
    data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
    return [data, sw1, sw2];


class IdCardReader():

    def __init__(self, readers=None, reader=None, connect=None, req=None):
        self.readers = readers
        self.reader = reader
        self.connect = connect
        self.req = req

    def get_all_readers(self):
        self.readers = readers()
        print ('Available readers:')
        for readerIndex,readerItem in enumerate(self.readers):
            print(f"Number {readerIndex}: {readerItem}")

        
    def select_reader(self, index=0):
        
        if self.readers is None or self.readers == []:
            raise Exception("The readers is empty. Please call the get_all_readers first")
        
        self.reader = self.readers[index]

    def connect_to_the_reader(self):
        # Connect to reader
        self.connection = self.reader.createConnection()
        self.connection.connect()
        atr = self.connection.getATR()
        print ("ATR: " + toHexString(atr))
        if (atr[0] == 0x3B & atr[1] == 0x67):
            self.req = [0x00, 0xc0, 0x00, 0x01]
        else :
            self.req = [0x00, 0xc0, 0x00, 0x00]

    def check_card(self):
        data, sw1, sw2 = self.connection.transmit(SELECT + THAI_CARD)
        return ("Select Applet: %02X %02X" % (sw1, sw2))

    def get_cardid(self):
        data = getData(CMD_CID, self.connection, self.req)
        cid = thai2unicode(data[0])
        return (cid)

    def get_thai_fullname(self):
        data = getData(CMD_THFULLNAME, self.connection, self.req)
        return (thai2unicode(data[0]))

    def get_eng_fullname(self):
        data = getData(CMD_ENFULLNAME,self.connection, self.req)
        return(thai2unicode(data[0]))

    def get_dateofbirth(self):
        data = getData(CMD_BIRTH, self.connection, self.req)
        return(thai2unicode(data[0]))

    def get_gender(self):
        data = getData(CMD_GENDER, self.connection, self.req)
        return (thai2unicode(data[0])) # 1 = Male, 2 = Female

    def get_issuer(self):
        data = getData(CMD_ISSUER, self.connection, self.req)
        return(thai2unicode(data[0]))

    def get_issue_date(self):
        data = getData(CMD_ISSUE, self.connection, self.req)
        return(thai2unicode(data[0]))

    def get_expire_date(self):
        data = getData(CMD_EXPIRE, self.connection, self.req)
        return (thai2unicode(data[0]))

    def get_address(self):
        data = getData(CMD_ADDRESS, self.connection, self.req)
        return(thai2unicode(data[0]))

    def get_image(self, name):

        photo = getData(CMD_PHOTO1, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO2, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO3, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO4, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO5, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO6, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO7, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO8, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO9, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO10, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO11, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO12, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO13, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO14, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO15, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO16, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO17, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO18, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO19, self.connection, self.req)[0]
        photo += getData(CMD_PHOTO20, self.connection, self.req)[0]

        # Convert list to bytes
        data = bytes(photo)

        f = open(name + ".jpg", "wb")
        f.write(data)
        f.close()

        return True
