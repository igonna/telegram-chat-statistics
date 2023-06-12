from day import Day

class User:
    def add_message(self, date, msg):
        if date in self.days:
            self.days[date].add_message(msg)
        else:
            day = Day(date)
            day.add_message(msg)
            self.days[date] = day
    
    def __init__(self, name):
        self.days = {}
        self.name = name