def is_leap_year(year):
    return year % 4 == 0 and year % 400 != 0


def date2count(year, month, day):
    """
    convert the date into days count from 2020/1/1.
    :param year:
    :param month:
    :param day:
    :return: [year, month, day] is the count_th days from 2020/1/1
    """
    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_leap_year = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    count = 0
    for i in range(2020, year):    # add days until last year
        if is_leap_year(i):
            count += 366
        else:
            count += 365

    if is_leap_year(year):
        days_current_year = days_leap_year
    else:
        days_current_year = days

    for i in range(1, month):           # add months until last month
        count += days_current_year[i]

    count += day             # 天数 = 日期中的第几天

    return count


def count2date(count):
    """
    convert the days count from 2020/1/1 into the real date.
    :param count:
    :return: year, month, day converted by the count_th days from 2020/1/1
    """
    year = 2020
    month = 1
    while count > 0:         # 减至小于0，年份为next_year
        if is_leap_year(year):
            count -= 366
        else:
            count -= 365
        year += 1

    year -= 1   # 从next_year回退
    if is_leap_year(year):
        count += 366
    else:
        count += 365

    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_leap_year = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if is_leap_year(year):
        days_current_year = days_leap_year
    else:
        days_current_year = days

    while count > 0:      # 减至小于0，年份为next_month
        count -= days_current_year[month]
        month += 1

    month -= 1        # 从next_month回退
    count += days_current_year[month]
    day = count

    return year, month, day


def add_print_date(year_from, month_from, day_from,
               year_to, month_to, day_to, list_of_date):
    """
    add the date in the [date_from, date_to] to the list_of_date
    :param year_from: from which year
    :param month_from: from which month
    :param day_from: from which day
    :param year_to: to which year
    :param month_to: to which month
    :param day_to: to which day
    :param list_of_date: example:['2020/7/30', '2020/7/31'] new date will be appended here
    :return:
    """

    # 从2020/1/1开始计数
    counts_from = date2count(year_from, month_from, day_from)
    counts_to = date2count(year_to, month_to, day_to)

    assert counts_from <= counts_to, "Date_from must be earlier than Date_to!"

    for i in range(counts_from, counts_to+1):
        year, month, day = count2date(i)
        date = str(year) + '/' + str(month) + '/' + str(day)
        list_of_date.append(date)

