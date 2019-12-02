from abc import ABC

from ids_lib.metrics.caching.cache_data import CacheData
from ids_lib.metrics.caching.cache_handler import CacheHandler
from ids_lib.metrics.metrics import AnomalyDetectionMetrics


class Metrics(AnomalyDetectionMetrics, ABC):
    normal_data_points = [
        (('read', 'open', 'read'), True),
        (('futex', 'open', 'read'), False),
        (('read', 'open', 'futex'), True),
        (('read', 'execve', 'read'), True),
        (('read', 'execve', 'read'), True),
        (('read', 'execve', 'read'), True),
        (('read', 'execve', 'read'), True),
        (('read', 'execve', 'read'), True),
        (('read', 'execve', 'read'), True),
        (('read', 'read', 'execve'), True)
    ]

    anomalous_data_points = [
        (('modprobe', 'open', 'read'), False),
        (('futex', 'futex', 'read'), False),
        (('futex', 'futex', 'read'), False),
        (('futex', 'futex', 'read'), False),
        (('read', 'modprobe', 'futex'), True),
        (('read', 'execve', 'close'), True),
        (('read', 'close', 'execve'), False)
    ]

    def map_anomalous_input_to_detected(self):
        for x in self.anomalous_data_points:
            if x[1]:
                return True
        return False


data = Metrics()
a = CacheData(data)

handler = CacheHandler(a, context_name='CVE-2019-1234')
handler.persist()

lookatmyobject = handler.load()
