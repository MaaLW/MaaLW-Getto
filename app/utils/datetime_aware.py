'''
This module is used to replace datetime.datetime and datetime.time, to be timezone aware by default
2025-03-15 Not using this for now
'''
from datetime import datetime as _datetime, time as _time, timedelta, timezone

tz = timezone(offset=timedelta(hours=8), name="Asia/Shanghai")

class datetime(_datetime):
    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0,
                microsecond=0, tzinfo=None, *, fold=0):
        if tzinfo is None:
            tzinfo = tz
        return super().__new__(_datetime, year, month, day, hour, minute, second, microsecond, tzinfo, fold=fold)
    
class time(_time):
    def __new__(cls, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        if tzinfo is None:
            tzinfo = tz
        return super().__new__(_time, hour, minute, second, microsecond, tzinfo, fold=fold)
    
try:
    import jsons
except ImportError:
    pass
else:
    jsons.set_serializer(func=jsons.default_datetime_serializer, cls=datetime)
    jsons.set_deserializer(func=jsons.default_datetime_deserializer, cls=datetime)
    jsons.set_serializer(func=jsons.default_time_serializer, cls=time)
    jsons.set_deserializer(func=jsons.default_time_deserializer, cls=time)