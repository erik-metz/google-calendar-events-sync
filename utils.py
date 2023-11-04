from datetime import datetime


def get_dateTime_from_millis(timestamp_in_milliseconds:int):
    timestamp_in_seconds = timestamp_in_milliseconds / 1000  # Convert to seconds

    dt = datetime.utcfromtimestamp(timestamp_in_seconds)

    return dt.strftime('%Y-%m-%d %H:%M:%S')
