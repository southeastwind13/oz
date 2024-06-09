# -------------------------------------------------------------------
# Title        : CSV Helper
# Description  : Use for work with CSV
# Writer       : Watcharapong Wongrattanasirikul
# Email        : w.wattcharapong@gmail.com
# Created date : 25 Jul 2021
# Updated date : 03 Oct 2021
# Version      : 0.0.2
# Remark       : Update logging and unit test
# -------------------------------------------------------------------
import os,sys,inspect
from types import prepare_class
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import csv
import pandas as pd

class CsvHelper():

    '''
    When use Pandas to read CSV. It use number of the first column to be 
    maximum expected columns of each rows then it will cause the tokenize error
    becuase some line has the number of columns more than expected. This class
    will help for read_csv with maximum columns in the file
    '''

    @staticmethod
    def read_complete_csv(path, separator=','):
        '''
        Read the csv file even number of the first row isn't match with number
        of maximum row.

        :param string path: The path of the csv file.
        :param string separator: The separator that use in the csv file.
        :return dataframe df: The data from the csv file.
        '''
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=separator)
            exsiting_data = [line for line in csv_reader]
            
            df = pd.DataFrame(exsiting_data)

            return df

    @staticmethod
    def get_maximum_columns(path, separator=','):
        '''
        Get the number of maximum columns from the csv file.

        :param string path: The path of the csv file.
        :return int max_columns: The number of maximum columns
        '''
        max_columns = 0
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=separator)

            for line in csv_reader:
                if len(line) > max_columns:
                    max_columns = len(line)

            return max_columns

    @staticmethod
    def generate_csv_from_dataframe(df, path, header=None):
        '''
        !!! Obsolete -> Change to use df.to_csv(file_path, index=None)
        Generate csv file from dataframe

        :param dataframe df: The data that use to generate csv file.
        :param string path: The path that use to save csv file.
        :param list header: The data that want to use to be header.
        '''
        with open(path, 'a') as f:
            w = csv.writer(f)
            
            if header is not None:
                w.writerow(header)
        
            w.writerows(df.values.tolist())