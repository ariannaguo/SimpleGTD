from datetime import datetime, timedelta


def week_range(day, offset):
    day = day.date()
    that_monday = day + timedelta(weeks=offset, days=-day.weekday())
    that_monday = datetime.combine(that_monday, datetime.min.time())

    return that_monday, that_monday + timedelta(weeks=1, seconds=-1)


def to_datetime(dt):
    return datetime.combine(dt, datetime.min.time())


def week_range_helper():
    ## use datetime
    today = datetime.today().date()
    print(today)

    # this Monday
    this_monday = today - timedelta(days=today.weekday())
    print(this_monday)

    # last week
    last_monday = this_monday + timedelta(weeks=-1)
    last_monday = datetime.combine(last_monday, datetime.min.time())

    last_friday = last_monday + timedelta(days=4)
    last_sunday = last_monday + timedelta(days=7, seconds=-1)
    print(last_monday)
    print(last_friday)
    print(last_sunday)


if __name__ == '__main__':
    print(week_range(datetime.now(), -1))
    print(week_range(datetime.now(), -2))
    print(week_range(datetime.now(), 2))