import json
import os
from pathlib import Path

from werkzeug.datastructures import MultiDict


class JsonHandler:
    __DIR = Path(__file__).parent.resolve()
    __NAME = 'posts.json'
    __PATH = __DIR / __NAME
    __ENCODER = 'UTF-8'

    def __init__(self) -> None:
        if not os.path.exists(self.__PATH):
            self._initialize_file()
        self._posts = None
        self._load()
        self._result = None

    def _initialize_file(self):
        with open(self.__PATH, "w", encoding=self.__ENCODER) as f:
            json.dump([], f)

    def _load(self):
        """Loads the JSON file from the predefined path."""
        with open(self.__PATH, "r", encoding=self.__ENCODER) as f:
            self._posts = json.load(f)

    def _save(self):
        with open(self.__PATH, "w", encoding=self.__ENCODER) as f:
            json.dump(self._posts, f, indent=4)

    @property
    def count(self):
        return len(self._posts)

    @property
    def _map(self) -> dict[int, int]:
        return {self._posts[i]['id']: i for i in range(self.count)}

    def get(self, params: MultiDict[str, str]):
        x = params.get
        start = (x('page', 1, type=int) - 1) * x('per_page', self.count, type=int)
        end = start + x('per_page', self.count, type=int)

        return sorted(
            self._posts, key=lambda post: post.get(x('sort', 'id')),
            reverse=(x('direction', 'asc') == 'desc')
        )[start:end]

    def post(self, post_id):
        if self._map.get(post_id):
            return self._posts[self._map.get(post_id)]
        return None

    @property
    def _id(self):
        return max(post['id'] for post in self._posts) + 1

    def add(self, post: dict[str, str | list[str] | int]):
        new_post = {
            "id": self._id,
            "title": post.get('title'),
            "content": post.get('content'),
            "comments": [],
            "categories": [],
            "tags": []
        }

        self._posts.append(new_post)
        self._save()
        return new_post

    def delete(self, post_id):
        if self._map.get(post_id):
            self._posts.pop(self._map.get(post_id))
            self._save()
            return {"message": f"Post with id <{post_id}> deleted."}
        return None

    def update(self, post_id, data):
        if self._map.get(post_id):
            self._posts[self._map.get(post_id)].update(data)
            self._save()
            return self._posts[self._map.get(post_id)]
        return None

    def category(self, post_id, category):
        self._posts[self._map.get(post_id)]['categories'].append(category)

    def comment(self, post_id, comment):
        self._posts[self._map.get(post_id)]['comments'].append(comment)

    def tag(self, post_id, tag):
        self._posts[self._map.get(post_id)]['tags'].append(tag)

    def attach(self, post_id, attachments):
        if self._map.get(post_id):
            if attachments.get('categories'):
                self.category(post_id, attachments.get('categories'))
                self._save()

            if attachments.get('comments'):
                self.comment(post_id, attachments.get('comments'))
                self._save()

            if attachments.get('tags'):
                self.tag(post_id, attachments.get('tags'))
                self._save()

            self._load()
            return self._posts[self._map.get(post_id)]
        return None

    def _init_result(self):
        self._result = self._posts

    def filter(self, key, value):
        if value:
            self._result = [post for post in self._result if str(value).lower() in str(post.get(key)).lower()]

    def search(self, params: MultiDict[str, str]):
        self._init_result()
        for param in params:
            print(self._result)
            self.filter(param, params.get(param))
        return self._result
