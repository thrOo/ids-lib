import os, errno
from ids_lib.helpers.filelock import FileLock
from ids_lib.helpers.json_helper import serialize_json, deserialize_json
from ids_lib.metrics.caching.cache_data import CacheData
from ids_lib.metrics.caching.defaults import DEFAULT_CACHE_CONTEXT, DEFAULT_CACHE_FILENAME, DEFAULT_CACHE_LOCATION


class CacheHandler:
    def __init__(self, data, context_name=DEFAULT_CACHE_CONTEXT, filename=DEFAULT_CACHE_FILENAME):
        self.data = data
        self.context = context_name
        self.filename = "{}_{}.json".format(context_name, filename)
        if not os.path.exists(DEFAULT_CACHE_LOCATION):
            try:
                os.makedirs(DEFAULT_CACHE_LOCATION)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        self.cachefile = os.path.join(DEFAULT_CACHE_LOCATION, self.filename)

    def persist(self):
        self.data.calculate_metrics()
        # all cache metric functions should be computed and serialized
        if isinstance(self.data, CacheData):
            with FileLock(self.cachefile):
                serialize_json(instance=self.data, path=self.cachefile)
        else:
            raise TypeError

    def load(self):
        with FileLock(self.filename):
            return deserialize_json(cls=CacheData, path=self.cachefile)
