from datetime import datetime, timezone, timedelta

from dateutil.parser import parse


def in_working_time(now_time, start_time, stop_time):
    """
    hanni
    :param now_time: タイムゾーン付きISO8601形式現在時刻 (01:00:00+09:00)
    :param start_time: ISO8601形式開始時刻 (21:00:00+09:00)
    :param stop_time:  ISO8601形式停止時刻 (06:00:00+09:00)
    :return: 稼働時間内であるか
    """
    to_utctime = lambda t: parse(t).astimezone(timezone.utc).timetz()

    now = to_utctime(now_time)
    start = to_utctime(start_time)
    stop = to_utctime(stop_time)

    if start < stop:
        # 日付をまたがない
        return start <= now < stop
    else:
        # 日付をまたぐ
        return start <= now or now < stop


def get_datetime_now(tz=None):
    return datetime.now().astimezone(tz)


def time_calibrate(datetime1, datetime2, second_delta):
    return (timedelta(seconds=second_delta) - (datetime2 - datetime1)).total_seconds()
