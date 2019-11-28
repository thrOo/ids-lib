import hashlib
import os
from pathlib import Path
from datetime import datetime

timestamp = datetime.timestamp(datetime.now())

DEFAULT_CACHE_LOCATION = os.path.join(str(Path.home()), '.cache', 'ids_lib')
DEFAULT_CACHE_FILENAME = hashlib.sha256(str(timestamp).encode('ASCII')).hexdigest()
DEFAULT_CACHE_CONTEXT = "ANY"
