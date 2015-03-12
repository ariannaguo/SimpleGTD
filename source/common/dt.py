from datetime import datetime, timedelta


def week_range(day, offset):
    day = day.date()
    that_monday = day + timedelta(weeks=offset, days=-day.weekday())
    that_monday = datetime.combine(that_monday, datetime.min.time())

    return that_monday, that_monday + timedelta(weeks=1, seconds=-1)


def to_datetime(dt):
    return datetime.combine(dt, datetime.min.time())


def to_end_of_date(dt):
    return to_datetime(dt) + timedelta(days=1, microseconds=-1)


def to_standard_string(dt):
    return dt.strftime("%m/%d/%Y")


def week_range_helper():
    ## use datetime
    today = datetime.today().date()
    print(today)

    print(datetime.now())
    print(to_datetime(datetime.now()))
    print(to_end_of_date(today))
    print(to_end_of_date(datetime.now()))

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
    week_range_helper()

    print(week_range(datetime.now(), -1))
    print(week_range(datetime.now(), -2))
    print(week_range(datetime.now(), 2))