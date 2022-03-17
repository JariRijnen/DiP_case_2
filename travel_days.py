import datetime


def travel_days() -> datetime:
    """Return next saturday and the week after saterday"""

    today = datetime.date.today()
    # if today is saturday, make sure to return next saturday
    next_saturday = today + datetime.timedelta((4-today.weekday()) % 7+1)
    return_saturday = next_saturday + datetime.timedelta(days=7)

    return next_saturday, return_saturday


if __name__ == '__main__':
    next_saturday, return_saturday = travel_days()
    print(type(next_saturday), return_saturday)
