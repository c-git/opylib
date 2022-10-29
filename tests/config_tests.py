import os


class TestsConfig:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TestsConfig()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise Exception("Meant to be singleton but constructed twice")
        self.no_skip: bool = os.getenv("T_NO_SKIP", default=None) is not None
        self.data_dir = 'data/'
        pass
