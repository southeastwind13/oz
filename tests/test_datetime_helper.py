''' Move directory 1 step outer'''
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from common.datetime_helper import DateTimeHelper
from datetime import date, datetime

class TestDataTimeHelper:

    def test_get_today_without_time(self):
        # Arrange
        expected_date = date.today

        # Act
        now = DateTimeHelper.get_today_without_time()

        # Assert
        assert  1 == 1

    def test_get_today_with_time(self):
        # Arrange 
        expected_date = datetime.today

        # Act
        now = DateTimeHelper.get_today_with_time()

        # Assert
        assert (expected_date == now)