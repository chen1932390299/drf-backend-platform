import datetime, pytz


def iso2timestamp(date_string, format='%Y-%m-%d %H:%M:%S', timespec='seconds'):
    """
    ISO8601时间转换为时间戳,Z表示祖鲁时间Zulu time 即+0时区,若去掉不写Z则采用系统本地时区。
    :param: date_string: '2018-01-16T02:59:02' match format '%Y-%m-%dT%H:%M:%S'
        while iso时间字符串 2019-03-25T16:00:00.000Z，2019-03-25T16:00:00.000111Z
        format:%Y-%m-%dT%H:%M:%S.%fZ；其中%f 表示毫秒或者微秒
    :param timespec:返回时间戳最小单位 seconds 秒，milliseconds 毫秒,microseconds 微秒
    :return:时间戳 默认单位秒
    """
    tz = pytz.timezone('Asia/Shanghai')
    utc_time = datetime.datetime.strptime(date_string, format)  # 将字符串读取为 时间 class datetime.datetime

    time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)

    times = {
        'seconds': int(time.timestamp()),
        'milliseconds': round(time.timestamp() * 1000),
        'microseconds': round(time.timestamp() * 1000 * 1000),
    }
    return times[timespec]


def timestamp2iso(timestamp, format='%Y-%m-%dT%H:%M:%S.%fZ'):
    """
    时间戳转换到ISO8601标准时间(支持微秒级输出 YYYY-MM-DD HH:MM:SS.mmmmmm)
    :param timestamp:时间戳，支持 秒，毫秒，微秒级别
    :param format:输出的时间格式  默认 iso=%Y-%m-%dT%H:%M:%S.%fZ；其中%f表示微秒6位长度

    此函数特殊处理，毫秒/微秒部分 让其支持该部分的字符格式输出
    :return:
    """
    format = format.replace('%f', '{-FF-}')  # 订单处理微秒数据 %f
    length = min(16, len(str(timestamp)))  # 最多去到微秒级

    # 获取毫秒/微秒 数据
    sec = '0'
    if length != 10:  # 非秒级
        sec = str(timestamp)[:16][-(length - 10):]  # 最长截取16位长度 再取最后毫秒/微秒数据
    sec = '{:0<6}'.format(sec)  # 长度位6，靠左剩下的用0补齐
    timestamp = float(str(timestamp)[:10])  # 转换为秒级时间戳
    return datetime.datetime.utcfromtimestamp(timestamp).strftime(format).replace('{-FF-}', sec)
