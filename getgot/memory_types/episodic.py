import sqlite3

from src.getgot.config import Config
from src.getgot.memory_types.base import BaseMemory


class EpisodicMemory(BaseMemory):
    def __init__(self):
        self.config = Config()
        self.config.ensure_dirs()
        self._init_db()

    def _init_db(self):
        # Use config.data_dir for SQLite file location
        pass
