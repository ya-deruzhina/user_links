from django.conf import settings

from pytz import timezone
import datetime
import calendar


ADMIN_TIMEZONE = timezone(settings.ADMIN_TIMEZONE)


class DatetimeUtils:
    @classmethod
    def current_week_range(cls):
        date = cls.get_admin_datetime()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        return (start_week, end_week)

    @classmethod
    def current_month_range(cls):
        date = cls.get_admin_datetime()
        _, end = calendar.monthrange(date.year, date.month)

        start_month = datetime.datetime(year=date.year, month=date.month, day=1)
        end_month = datetime.datetime(year=date.year, month=date.month, day=end)
        return (start_month, end_month)

    @classmethod
    def working_days_in_range(cls, start, end):
        daygenerator = (start + datetime.timedelta(x) for x in range((end - start).days))
        return [day for day in daygenerator if day.weekday() < 5]

    @classmethod
    def get_last_monday_in_month(cls, year, month):
        cal = calendar.Calendar(0)
        month = cal.monthdatescalendar(year, month)
        lastweek = month[-1]
        monday = lastweek[0]
        return monday

    @classmethod
    def get_admin_datetime(cls, date=None):
        date = date or datetime.datetime.now()
        return date.astimezone(ADMIN_TIMEZONE)

    @classmethod
    def get_admin_date(cls, date=None):
        if isinstance(date, datetime.date):
            date = datetime.datetime(*date.timetuple()[:-4])

        return cls.get_admin_datetime(date).date()

    @classmethod
    def get_now_with_tz(cls):
        return datetime.datetime.now(tz=timezone(settings.TIME_ZONE))
