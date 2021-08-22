import datetime


class Month:
    def __init__(self, month: int, year: int = datetime.datetime.now().year):
        self._month = month
        self._year = year

    @property
    def first_day(self):
        return datetime.date(self._year, self._month, 1)
