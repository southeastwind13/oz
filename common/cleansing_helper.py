# -------------------------------------------------------------------
# Title        : Cleansing data
# Description  : Use for cleaning data
# Writer       : Watcharapong Wongrattanasirikul
# Email        : w.wattcharapong@gmail.com
# Created date : 25 Jul 2021
# Updated date : 03 Oct 2021
# Version      : 0.0.2
# Remark       : Update logging and unit test
# -------------------------------------------------------------------


from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import itertools
import logging
import logging.config
import re

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(module)s %(funcName)s: %(message)s'

logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    format=log_format,
    level=logging.DEBUG
    )

class ClensingHelper():

    @staticmethod
    def calculate_age(birthdate):
        '''
        Calculate age from birthdate

        :param date birthdate: The date of birth
        
        :return int age: The age that calculate from the birthdate
        '''

        if (type(birthdate) is not date):

            error_message = f"The input type isn't datetime.date: {type(birthdate)}"
            
            logging.error(error_message)
            raise TypeError(error_message)

        today = date.today()

        if (birthdate.year > 2400):
            convert_be_to_fe = 543

            #* use relativedelta with get more accurate from timedelta
            birthdate = birthdate - relativedelta(years=convert_be_to_fe)

        if birthdate > today:

            error_message = f"Birth date can't be in the future: {birthdate}"

            logging.error(error_message)
            raise ValueError(error_message)

        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        logging.info(f"The birthday is {birthdate} then age is {age} years")

        return age

    @staticmethod
    def mapping(item, criteria):
        '''
        Mapping item with the criteria

        :param str item: The item that would like to map with criteria.
        :param dict criteria: The tuple of criteria mapping.
        
        :return int,str: The value from criteria when key is item.
        '''

        if item in criteria.keys():
            return criteria[item]
        else:
            logging.error(f"Can't mapping data: {item} with criteria: {criteria}.")
            return -1

    @staticmethod
    def dict_sort(dict, ascending=True):
        '''
        Sort the dictionary by value

        :param dict dict: The dictionary that would like to sort.
        :param bool ascending: Is it sort by ascending.

        :return dict: The sorted dict.
        '''
        if type(dict) != dict:
            logging.error(f"The input {dict} is not dictionary.")
        dict_sort = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=(not ascending))} 
        return dict_sort

    @staticmethod
    def dict_slice(dict_items, number):
        '''
        Make slicing of the dictionary

        :param dict dict_items: The dictionary that would like to slice.
        :return dict: The sliced dict.
        '''
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        
        if type(dict_items) != dict:
            logging.error(f"The input {dict_items} is not dictionary.")
        return dict(itertools.islice(dict_items.items(), number))
        
    @staticmethod
    def cleansing_text(text):
        '''
        Remove special character from text

        :param str text: The text that would like to remove special character.

        :return str: The text after remove special character.
        '''
        if(type(text) is not str):
            error_message = f"This input isn't string: {type(text)}"
            logging.error(error_message)
            raise TypeError(error_message)

        text = text.strip().lower()

        # Remvoe special character, number, space, dot
        text = re.sub('[\t\n\xa0\"\'!?\/\(\)%\:\=\-\+\*\_ๆ#$&,<>]', '', text)
        text = re.sub('[0-9]', ' ', text)
        text = re.sub('[\.]', ' ', text)
        text = re.sub('\u200b',' ', text)
        text = re.sub('\s+',' ',text)
        text = text.strip()

        return text

    def _atoi(text):
        return int(text) if text.isdigit() else text

    def _natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ClensingHelper._atoi(c) for c in re.split(r'(\d+)', text) ]

    @staticmethod
    def sort_text_with_number(items):
        '''
        Sort the list of text with number.

        :param list items: The list of the text with number.
        :return list: The sorted list
        '''
        items.sort(key=ClensingHelper._natural_keys)
        return(items)