# coding=utf-8
from datetime import date, datetime, timedelta


class DateTimeUtils(object):
    """ This object represents helpful methods for handling
    """
    @staticmethod
    def time_to_minutes(time):
        splitted = time.split(":")

        hours = splitted[0]
        minutes = splitted[1]

        return int(hours) * 60 + int(minutes)

    @staticmethod
    def time_to_minutes_from_full_time(time):
        splitted = time.split(":")

        hours = splitted[0]
        minutes = splitted[1]

        return int(hours) * 60 + int(minutes)

    @staticmethod
    def time_from_minutes(minutes):
        minut = minutes % 60
        hours = (minutes - minut) / 60

        return "%.2d:%.2d" % (hours, minut)

    @staticmethod
    def get_day_number_by_simple_date(date):
        splitted_1 = date.split("-")
        y1 = splitted_1[0]
        m1 = splitted_1[1]
        d1 = splitted_1[2]

        d = datetime.strptime('%s-%s-%s' % (y1, m1, d1), '%Y-%m-%d')
        return d.weekday()

    @staticmethod
    def get_day_number_by_full_datetime(date):
        _d1 = DateTimeUtils.get_date_from_time(date)
        return DateTimeUtils.get_day_number_by_simple_date(_d1)

    @staticmethod
    def get_today_full_datetime_milliseconds():
        """ Use this function to get current time and date in full

        :param timezone:
        :return:
        """

        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

    @staticmethod
    def get_today_full_datetime(timezone="03:00"):
        """ Use this function to get current time and date in seconds

        :param timezone:
        :return:
        """
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+" + timezone)

    @staticmethod
    def get_day_number_by_full_date(date):
        _d1 = DateTimeUtils.get_date_from_time(date)
        splitted_1 = _d1.split("-")
        y1 = splitted_1[0]
        m1 = splitted_1[1]
        d1 = splitted_1[2]

        d = datetime.strptime('%s-%s-%s' % (y1, m1, d1), '%Y-%m-%d')
        return datetime.strftime(d, '%d')


    @staticmethod
    def get_week_number_by_full_date(date):
        _d1 = DateTimeUtils.get_date_from_time(date)
        splitted_1 = _d1.split("-")
        y1 = splitted_1[0]
        m1 = splitted_1[1]
        d1 = splitted_1[2]

        d = datetime.strptime('%s-%s-%s' % (y1, m1, d1), '%Y-%m-%d')
        return datetime.strftime(d, '%W')

    @staticmethod
    def get_time_with_delta(minutes=None):
        if minutes is not None:
            return (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
        else:
            raise StandardError("no argument call is unacceptable")

    @staticmethod
    def time_difference(expected_bigger, expected_smaller):
        """
        Use to compare two date-time string objects and find if there is some difference

        :param expected_bigger:
        :param expected_smaller:
        :return: > 0 if expected bigger is really bigger then expected smaller

        """
        # '2016-09-29T00:16:48+02:00'
        _d1 = expected_bigger.split("T")[0]
        _d2 = expected_smaller.split("T")[0]

        _t1 = expected_bigger.split("T")[1].split("+")[0]
        _t2 = expected_smaller.split("T")[1].split("+")[0]

        h1 = int(_t1.split(":")[0])
        h2 = int(_t2.split(":")[0])

        min1 = int(_t1.split(":")[1])
        min2 = int(_t2.split(":")[1])

        s1 = int(_t1.split(":")[2])
        s2 = int(_t2.split(":")[2])

        splitted_1 = _d1.split("-")
        splitted_2 = _d2.split("-")
        y1 = splitted_1[0]
        m1 = splitted_1[1]
        d1 = splitted_1[2]

        y2 = splitted_2[0]
        m2 = splitted_2[1]
        d2 = splitted_2[2]

        diff1 = datetime(int(y1), int(m1), int(d1), hour=h1, minute=min1, second=s1)
        diff2 = datetime(int(y2), int(m2), int(d2), hour=h2, minute=min2, second=s2)
        return diff1 - diff2

    @staticmethod
    def date_difference(_d1, _d2):
        splitted_1 = _d1.split("-")
        splitted_2 = _d2.split("-")
        y1 = splitted_1[0]
        m1 = splitted_1[1]
        d1 = splitted_1[2]

        y2 = splitted_2[0]
        m2 = splitted_2[1]
        d2 = splitted_2[2]

        diff1 = datetime(int(y1), int(m1), int(d1))
        diff2 = datetime(int(y2), int(m2), int(d2))
        return diff2 - diff1

    @staticmethod
    def get_date_from_time(full_date_time):
        # u'2012-07-20T17:11:22.000Z'
        return full_date_time.split("T")[0]

    @staticmethod
    def get_time(full_date_time):
        # u'2012-07-20T17:11:22.000Z'
        return full_date_time.split("T")[1].split("+")[0]


    @staticmethod
    def get_time_zone(full_date_time):
        # u'2012-07-20T17:11:22.000Z'
        return full_date_time.split("T")[1].split("+")[1]

    @staticmethod
    def get_friendly_offset_name(offset, locale="en"):
        if locale is "en":
            if offset == 0:
                return "Monday"
            elif offset == 1:
                return "Tuesday"
            elif offset == 2:
                return "Wednesday"
            elif offset == 3:
                return "Thursday"
            elif offset == 4:
                return "Friday"
            elif offset == 5:
                return "Saturday"
            elif offset == 6:
                return "Sunday"
        else:
            if offset == 0:
                return "Понедельник"
            elif offset == 1:
                return "Вторник"
            elif offset == 2:
                return "Среда"
            elif offset == 3:
                return "Четверг"
            elif offset == 4:
                return "Пятница"
            elif offset == 5:
                return "Суббота"
            elif offset == 6:
                return "Воскресенье"
