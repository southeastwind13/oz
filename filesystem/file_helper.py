# -------------------------------------------------------------------
# Title        : File Helper
# Description  : Use for work with normal file
# Writer       : Watcharapong Wongrattanasirikul
# Email        : w.wattcharapong@gmail.com
# Created date : 23 Aug 2022
# Updated date : 23 Oct 2022
# Version      : 0.0.1
# Remark       : Inintiate
# -------------------------------------------------------------------

from PIL import Image
import numpy as np
import os
import PyPDF2
import re
import requests
import inspect

class FileHelper():
    
    @staticmethod
    def create_blank_file(path, name):
        '''
        Create blank file for any file type.

        :param str path: The directory of the file that need to create.
        :param str name: The file name of the file that need to create.
        '''
        with open(path+name, 'w') as fp:
            pass

    @staticmethod
    def check_file_exists(path, name):
        '''
        '''

        is_exist = os.path.isfile(path+name)
        return is_exist

    @staticmethod
    def delete_file_from_directory(path,name):
        '''
        Delete file from specific directory and file name.

        :param str path: The directory of the file that need to delete.
        :param str name: The file name of the file that need to delete.
        '''
        os.remove(path + name)

    @staticmethod
    def get_file_names_from_directory(path):
        '''
        Get file names from specific directory.

        :param str path: The path of the directory that want to get file names
        :return list: The list of the file names in the directory
        '''
        filenames = next(os.walk(path), (None, None, []))[2]
        return filenames

    @staticmethod
    def get_file_extension_from_file(file_path:str):
        '''
        Get file extension from file.

        :param str file_path: The path of the file.
        :return str: The extension of the file.
        '''

        return os.path.splitext(file_path)[-1].lower()

    @staticmethod
    def save_image_from_url(directory, name, file_type, url):
        '''
        '''

        response = requests.get(url)

        file = open(directory + name + file_type, "wb")
        file.write(response.content)
        file.close()

    @staticmethod
    def create_pdf_from_images(images, directory, name):
    
        if images is np.NaN  or images == []:
            raise ValueError("The list of image can't be null or empty.")

        images_list = []

        for file in images:
            img = Image.open(directory + file)
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                images_list.append(rgb_img)
            else:
                images_list.append(img)

        img1 = images_list[0]
        img_oth = images_list[1:]
        
        img1.save(directory + name +".pdf", save_all=True, append_images=img_oth)

    @staticmethod
    def count_pdf_pages(directory, name):
        file = open(directory + name, 'rb')
        readpdf = PyPDF2.PdfFileReader(file)
        totalpages = readpdf.numPages
        return(totalpages)

    @staticmethod
    def get_directory_from_file(file:str):
        return os.path.dirname(os.path.realpath(file))

    @staticmethod
    def get_working_directory():
        return os.getcwd()