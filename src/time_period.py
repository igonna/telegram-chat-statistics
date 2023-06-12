from day import Day
from typing import List

class TimePeriod:
    def get_msg_len(self):
        sum = 0
        for day in self.days:
            sum += day.total_msg_len
        return sum
    
    def get_msg_count(self):
        sum = 0
        for day in self.days:
            sum += day.total_msg_count
        return sum
    
    def get_words_count(self):
        sum = 0
        for day in self.days:
            sum += day.total_words_count
        return sum
    
    def get_days_msg_count(self):
        days_date_msg = {}
        for day in self.days:
            days_date_msg[day.date] = day.total_msg_count
        return days_date_msg
    
    def __init__(self, days):
        self.days: List[Day] = sorted(days, key=lambda day: day.date)