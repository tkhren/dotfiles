# coding: utf-8

import time

class StopWatch(object):
    """ Timer to find bottleneck

        sw = StopWatch('start')
        do_somthing_A()
        sw.lap('timeA')
        do_somthing_B()
        sw.lap('timeB')
        sw.dump()
    """
    def __init__(self, msg=None):
        self.restart(msg)

    def restart(self, msg=None):
        self.records = []
        if msg is None:
            msg = 't%d' % len(self.records)

        delta = 0.0   # delta
        self.elapsed_time = 0.0
        self.records.append( (msg, self.elapsed_time, delta) )

        self.last_time = time.time()

    def lap(self, msg=None):
        delta = time.time() - self.last_time

        if msg is None:
            msg = 't%d' % len(self.records)

        self.elapsed_time = self.records[-1][1] + delta
        self.records.append( (msg, self.elapsed_time, delta) )

        self.last_time = time.time()

    def dump(self, msg=None, precision=5, screenwidth=70):
        col0_label = 'point'
        col1_label = 'elapsed'
        col2_label = 'delta'
        col3_label = ''
        col4_label = ''

        col0_w = max([len(r[0]) for r in self.records] or [0])
        col1_w = max([str(r[1]).index('.') for r in self.records] or [0])
        col2_w = max([str(r[2]).index('.') for r in self.records] or [0])
        col3_w = len('xx.xx%')
        col4_w = max([int(100.0 * r[2] / self.elapsed_time) for r in self.records] or [0])

        col0_width = max(col0_w, len(col0_label))
        col1_width = max(col1_w + precision + 1, len(col1_label))
        col2_width = max(col2_w + precision + 1, len(col2_label))
        col3_width = max(col3_w, len(col3_label))
        bar_width = float(screenwidth - col0_width \
                                      - col1_width \
                                      - col2_width \
                                      - col3_width \
                                      - 6) / col4_w

        col4_width = int(bar_width)

        fmt0 = '%s'
        fmt1 = '%%%d.0%df' % (col1_w, precision)
        fmt2 = '%%%d.0%df' % (col2_w, precision)
        fmt3 = '%2.2f%%'
        fmt4 = '%s'

        record_fmt0 = '%s: %s'
        record_fmt = '%s: %s +%s %s %s'
        record = record_fmt % (
                col0_label.ljust(col0_width),
                col1_label.ljust(col1_width),
                col2_label.ljust(col2_width),
                col3_label.ljust(col3_width),
                col4_label.ljust(col3_width)
            )
        print(record)

        for msg, elapsed, delta in self.records:
            col0 = (fmt0 % msg).ljust(col0_width)
            col1 = (fmt1 % elapsed).rjust(col1_width)
            col2 = (fmt2 % delta).rjust(col2_width)

            rate = 100.0 * delta / self.elapsed_time
            col3 = (fmt3 % rate).rjust(col3_width)
            col4 = (fmt4 % ('*' * int(bar_width * rate))).ljust(col4_width)

            if delta > 0:
                print(record_fmt % (col0, col1, col2, col3, col4))
            else:
                print(record_fmt0 % (col0, col1))

        self.last_time = time.time()






















from datetime import datetime
import calendar

import dateutil
from dateutil import zoneinfo
from dateutil.relativedelta import relativedelta

# よく使うタイムゾーンを列挙
TZ_UTC = zoneinfo.gettz('UTC')
TZ_JST = zoneinfo.gettz('Asia/Tokyo')   # 日本標準時 Japan ST  (UTC+0900)



# tzname からタイムゾーンを得るショートカット
def gettz(tzname):
    return zoneinfo.gettz(tzname)


# タイムゾーンの変換
def localtime(dt, tzinfo=None):
    if tzinfo is None:
        tzinfo = TZ_UTC

    if not dt.tzinfo:
        # タイムゾーン情報の無い datetime については UTC 決め打ちにする.
        dt = dt.replace(tzinfo=TZ_UTC)
        if dt.tzinfo == tzinfo:
            return dt
    return dt.astimezone(tzinfo)

def utctime(dt):
    return localtime(dt, TZ_UTC)

def jsttime(dt):
    return localtime(dt, TZ_JST)


# 現在時刻 (デフォルトは UTC)
def localnow(tzinfo=None):
    return localtime(datetime.utcnow(), tzinfo)

def utcnow():
    return utctime(datetime.utcnow())

def jstnow():
    return jsttime(datetime.utcnow())


# 相対時刻の取得
def reldatetime(pivot=None, **kwds):
    """ Relative datetime:
        tommorow  => reldatetime(days=+1)
        yesterday => reldatetime(days=-1)
        next_month => reldatetime(months=+1)
        last_month => reldatetime(months=-1)

        If the pivot datetime is None, the current time will be used as pivot.
    """
    if not pivot:
        tzinfo = kwds.pop('tzinfo', None)
        pivot = localnow(tzinfo)
    return pivot + relativedelta(**kwds)


# 誕生日を入れると年齢を返す.
def how_old_are_you(birthday_dt):
    now = localnow(birthday_dt.tzinfo)
    return relativedelta(now - birthday_dt).years




# vim: ft=python ff=unix fenc=utf-8
