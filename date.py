import common


def db_to_date(date_string):
    splitted = date_string.split('|')
    date = splitted[0]
    time = splitted[1]
    date_splitted = date.split('.')
    time_splitted = time.split(':')
    return {'day': int(date_splitted[0]), 'month': int(date_splitted[1]), 'year': int(date_splitted[2]), 'minute': int(time_splitted[1]), 'hour': int(time_splitted[0])}


def date_to_db(date):
    str = date['day'] + '.' + date['month'] + '.' + date['year'] + '|' + date['minute'] + ':' + date['hour']
    return str