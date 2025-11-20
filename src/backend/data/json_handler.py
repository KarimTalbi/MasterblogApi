import json
import os
from pathlib import Path
from werkzeug.datastructures import MultiDict
from datetime import datetime
from flask import jsonify


class Posts:
    __DIR = Path(__file__).parent.resolve()
    __FILE = 'posts.json'

    def __init__(self):
        self._path = self.__DIR / self.__FILE
        self._init()
        self._data = None
        if not self._data:
            self._get()
        self._result = None

    def _init(self):
        if not os.path.exists(self._path):
            with open(self._path, "w", encoding='UTF-8') as f:
                json.dump([], f)

    def _get(self):
        with open(self._path, "r", encoding='UTF-8') as f:
            self._data = json.load(f)

    def _set(self):
        with open(self._path, "w", encoding='UTF-8') as f:
            json.dump(self._data, f, indent=4)

    def _id(self):
        if not self._data:
            return 1
        return max(post.get('id') for post in self._data) + 1

    @property
    def _map(self) -> dict[int, int]:
        return {self._data[i].get('id'): i for i in range(len(self._data))}

    def post(self, post_id):
        if self._map.get(post_id) is not None:
            return jsonify(self._data[self._map.get(post_id)]), 200
        return {'error': f'Post with id <{post_id}> not found.'}, 404

    def posts(self, params: dict[str, str]):
        if params.get('sort') == 'date':
            return sorted(
                self._data, key=lambda post: datetime.strptime(post.get('date'), "%Y-%m-%d"),
                reverse=(params.get('direction', 'asc') == 'desc')
            )

        return sorted(
            self._data, key=lambda post: post.get(params.get('sort', 'id')),
            reverse=(params.get('direction', 'asc') == 'desc')
        )

    @staticmethod
    def check_unsupported(post: dict[str, str | list[str] | int]):
        unsupported = []
        for key in post:
            if key not in ["title", "content", "author"]:
                unsupported.append(key)
        return unsupported

    @staticmethod
    def check_missing(post: dict[str, str | list[str] | int]):
        missing = []
        for key in ["title", "content", "author"]:
            if key not in post:
                missing.append(key)
        return missing


    def add(self, post: dict[str, str | list[str] | int]):
        missing = self.check_missing(post)
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400

        unsupported = self.check_unsupported(post)
        if unsupported:
            return jsonify({'error': f'Unsupported fields: {unsupported}'}), 400

        new_post = {
            "id": self._id(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        new_post.update(post)

        self._data.append(new_post)
        self._set()
        return jsonify(new_post), 201

    def delete(self, post_id):
        if self._map.get(post_id) is not None:
            self._data.pop(self._map.get(post_id))
            self._set()
            return jsonify({"message": f"Post with id <{post_id}> deleted."}), 200
        return {'error': f'Post with id <{post_id}> not found.'}, 404

    def update(self, post_id, data):
        if self._map.get(post_id) is not None:
            missing = self.check_missing(data)
            if len(missing) == 3:
                return jsonify({'error': f'No supported fields. Supported: {missing}'}), 400

            unsupported = self.check_unsupported(data)
            if unsupported:
                return jsonify({'error': f'Unsupported fields: {unsupported}'}), 400

            self._data[self._map.get(post_id)].update(data)
            self._set()
            return jsonify(self._data[self._map.get(post_id)]), 200
        return {'error': f'Post with id <{post_id}> not found.'}, 404

    def filter(self, key, value):
        if value:
            self._result = [post for post in self._result if str(value).lower() in str(post.get(key)).lower()]

    def search(self, params: MultiDict[str, str]):
        self._result = self._data.copy()
        for param in params:
            print(self._result)
            self.filter(param, params.get(param))
            if not self._result:
                return {'error': 'No posts found.'}, 404
        return jsonify(self._result), 200
