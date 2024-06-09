# -------------------------------------------------------------------
# Title        : Logging Helper
# Description  : Use to log data to the file
# Writer       : Watcharapong Wongrattanasirikul
# Created date : 28 Jan 2022
# Updated date : -
# Version      : 0.0.1
# Remark       : Initiate
# -------------------------------------------------------------------

#! Under-developing

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import itertools
import logging
import logging.config
import re


class LoggingHelper():

    def __init__(self, filepath, filemode, format=None, level=logging.DEBUG) -> None:
         logging.basicConfig()


    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(module)s %(funcName)s: %(message)s'

    logging.basicConfig(
    filename='app.log', 
    filemode='a', 
    format=log_format,
    level=logging.DEBUG
    )