def convert_time_into_minutes(interval, interval_type):
    if interval_type.lower() == 'minutes':
        pass
    elif interval_type.lower() == 'hours':
        interval = interval * 60
    elif interval_type.lower() == 'days':
        interval = interval * 60 * 24

    return interval
