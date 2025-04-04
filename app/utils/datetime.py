'''
This module is used to override jsons datetime serializers and deserializers to be compatible with timezone naive
'''
from datetime import datetime, time, timedelta, timezone
from time import sleep
from .logger import logger

try:
    import jsons
except ImportError:
    logger.warning("jsons is not installed. DateTime (De)Serialization Might be Vulnerable.")
    pass
else:
    def datetime_serializer(obj: datetime,
                            *,
                            strip_microseconds: bool | None = False,
                            **kwargs) -> str:
        if obj.tzinfo is None: 
            # for this project we only use timezone naive datetime with timespec='seconds'
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        else: 
            return jsons.default_datetime_serializer(obj, strip_microseconds=strip_microseconds, **kwargs)

    def datetime_deserializer(obj: str,
                              cls: type = datetime,
                              **kwargs) -> datetime:
        date_str, time_str = obj.split('T')
        if time_str[-1] == 'Z' or '+' in time_str or '-' in time_str:
            # Has timezone info. Use default deserializer.
            return jsons.default_datetime_deserializer(obj, cls=cls, **kwargs)
        else:
            return datetime.strptime(obj, '%Y-%m-%dT%H:%M:%S')
        
    def time_serializer(obj: time, **kwargs) -> str:
        return obj.strftime('%H:%M:%S')
    jsons.set_serializer(func=datetime_serializer, cls=datetime)
    jsons.set_deserializer(func=datetime_deserializer, cls=datetime)
    jsons.set_serializer(func=jsons.default_time_serializer, cls=time)
    jsons.set_deserializer(func=jsons.default_time_deserializer, cls=time)