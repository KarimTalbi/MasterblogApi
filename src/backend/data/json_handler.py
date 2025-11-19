import json
import os
from pathlib import Path


class JsonHandler:
    __DIR = Path(__file__).parent.resolve()
    __NAME = 'posts.json'
    __PATH = __DIR / __NAME
    __ENCODER = 'UTF-8'

    def __init__(self) -> None:
        if not os.path.exists(self.__PATH):
            self._initialize_file()
        self.__posts = self._load()
        self.__modified_posts = None

    def _initialize_file(self):
        with open(self.__PATH, "w", encoding=self.__ENCODER) as f:
            json.dump([], f)

    def _load(self) -> list[dict[str, str | list[str] | int]]:
        """Loads the JSON file from the predefined path."""
        with open(self.__PATH, "r", encoding=self.__ENCODER) as f:
            return json.load(f)

    def _save(self):
        with open(self.__PATH, "w", encoding=self.__ENCODER) as f:
            json.dump(self.__modified_posts, f)

    def get(self):
        return self.__posts

    def unique_id(self):
        return max(post['id'] for post in self.__posts) + 1