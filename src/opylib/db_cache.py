import logging
from datetime import datetime

import yaml

from opylib.log import log
from opylib.timer import set_timeout

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class DBCache:
    """
    Provides a write cache for dict like databases.
    ASSUMPTIONS:
        - Keys are not tuples (tuples are used to trigger conversion to yaml
            (see __setitem__ for more info)
        - Database is not updated elsewhere
        - Thead safety is not an issue, uses blocking routines expected to
            complete in a single pass (operations are not atomic)
    """

    def __init__(self, db_backing: dict, save_cache_delay: int = 30,
                 *, purge_loglevel=logging.DEBUG):
        self.purge_loglevel = purge_loglevel
        self.save_cache_delay = save_cache_delay
        self.db_backing = db_backing
        self.cache = {}  # Values sent but not written to db yet

        # values that need to be converted before submitting to db
        self.to_yaml = set()

        self._timer_write_out = None
        self.last_write_time = datetime.now()

    def __contains__(self, item):
        return item in self.cache or item in self.db_backing

    def __setitem__(self, key, value):
        """
        Sets the value for key to the value passed. NB: If yaml is needed then
            a tuple should be passed as the key. The first element of the tuple
            should be the key and the second the value of should_yaml EG. db[
            'key', True] = 'apple'
        :param key: The key to set or tuple of form (key, should_yaml)
        :param value: The value to set
        """
        log(f'[DB Cache] received request to set {key}', logging.DEBUG)
        if isinstance(key, tuple):
            key, should_yaml = key
        else:
            should_yaml = False
        self.cache[key] = value
        if should_yaml:
            self.to_yaml.add(key)

        if not self.is_write_pending:
            sec_before_save_allowed = \
                self.save_cache_delay \
                - (datetime.now() - self.last_write_time).total_seconds()
            if sec_before_save_allowed < 0:
                self._write_to_backing()
            else:
                self._timer_write_out = set_timeout(sec_before_save_allowed,
                                                    self._write_to_backing)

    def get(self, key, should_yaml=False):
        """
        Retrieves a value corresponding to the key passed if not present
            returns None.
        :param key: The key to use to retrieve the value
        :param should_yaml: if the value need to be converted from yaml
        :return: The value corresponding to the key passed
        """
        if key in self.cache:
            return self.cache[key]
        else:
            result = self.db_backing.get(key)

        if should_yaml and result is not None:
            return yaml.load(result, Loader=Loader)
        else:
            return result

    def __getitem__(self, key):
        """
        Gets the value for they key specified. NB: If yaml is needed then
            a tuple should be passed as the key. The first element
            of the tuple should be the key and the second the value of
            should_yaml EG. db['key', True] = 'apple'
        :param key: The key to set or tuple of form (key, should_yaml)
        :return:
        """
        if isinstance(key, tuple):
            key, should_yaml = key
        else:
            should_yaml = False

        if key in self.cache:
            # No concern for yaml because not written to db yet
            return self.cache[key]
        else:
            if key in self.db_backing:
                # to make use of yaml code there
                return self.get(key, should_yaml=should_yaml)
            else:
                return self.db_backing[key]  # To trigger correct exception

    def _write_to_backing(self):
        """
        Writes the cache to the db. Using existence in self.to_yaml to know
            if that value has to converted to a yaml string before saving to db
        ASSUMPTION: Function completes in its entirety without any other
            thread calling any of the other functions
        """
        log('[DB Cache] Purging', self.purge_loglevel)
        for key in self.cache.keys():
            value = self.cache[key]
            if key in self.to_yaml:
                value = yaml.dump(value, Dumper=Dumper)
            self.db_backing[key] = value

        # Register save time and clear timer variable
        self.last_write_time = datetime.now()
        self._timer_write_out = None

        # reset cache and to_yaml
        self.cache = {}
        self.to_yaml = set()

    @property
    def is_write_pending(self):
        return self._timer_write_out is not None

    def keys(self):
        self.purge()
        return self.db_backing.keys()

    def purge(self):
        if self.is_write_pending:
            self._timer_write_out.cancel()
            self._write_to_backing()
