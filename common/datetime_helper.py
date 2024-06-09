from datetime import datetime, date
import dateutil.relativedelta as relativedelta


class DateTimeHelper():
    ''' Get today without time. '''
    @staticmethod
    def get_today_without_time():
        ''' Get today without time. '''
        return date.today

    @staticmethod
    def get_today_with_time():
        ''' Get today without time. '''
        return datetime.today
    
    @staticmethod
    def add_period(date, diff_year=0, diff_month=0, diff_day=0, diff_hour=0, 
                   diff_minute=0, diff_second=0):
            ''' Get today without time. '''
       
            return date + relativedelta.relativedelta(
            years=diff_year,
            months=diff_month,
            days=diff_day,
            hours=diff_hour,
            minutes=diff_minute,
            second=diff_second
            )