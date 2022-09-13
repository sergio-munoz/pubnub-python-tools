"""Time management related activities."""
from datetime import datetime
 
class TimeConfig():

    def __init__(self):
        # record current timestamp
        self.start_time = datetime.now()
        self.end_time = datetime.now()
 
    def _end(self):
        self.end_time = datetime.now()
 
    def total_seconds(self):
        self._end()
        td = (self.end_time - self.start_time).total_seconds() * 10**3
        return td
