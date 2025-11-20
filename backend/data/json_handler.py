"""
This module provides a handler for managing blog posts stored in a JSON file.
"""
import json
import os
from pathlib import Path
from datetime import datetime
from flask import jsonify, Response


class Posts:
    """
    A class to manage blog posts stored in a JSON file.

    This class handles reading, writing, and manipulating post data.
    """
    __DIR = Path(__file__).parent.resolve()
    __FILE = 'posts.json'

    def __init__(self):
        """
        Initializes the Posts object.

        Sets up the file path, ensures the JSON file exists, and loads the data.
        """
        self._path = self.__DIR / self.__FILE
        self._init()
        self._data = None
        if not self._data:
            self._get()
        self._result = None

    def _init(self) -> None:
        """
        Initializes the posts.json file if it doesn't exist.
        """
        if not os.path.exists(self._path):
            with open(self._path, "w", encoding='UTF-8') as f:
                json.dump([], f)

    def _get(self) -> None:
        """
        Reads the posts.json file and loads the data.
        """
        with open(self._path, "r", encoding='UTF-8') as f:
            self._data = json.load(f)

    def _set(self) -> None:
        """
        Writes the current data back to the posts.json file.
        """
        with open(self._path, "w", encoding='UTF-8') as f:
            json.dump(self._data, f, indent=4)

    def _id(self) -> int:
        """
        Calculates the next available post ID.

        Returns:
            The next integer ID.
        """
        if not self._data:
            return 1
        return max(post.get('id') for post in self._data) + 1

    @property
    def _map(self) -> dict[int, int]:
        """
        Creates a mapping from post ID to list index for quick lookups.

        Returns:
            A dictionary mapping post IDs to their index in the data list.
        """
        return {self._data[i].get('id'): i for i in range(len(self._data))}

    def post(self, post_id: int) -> tuple[Response, int]:
        """
        Retrieves a single post by its ID.

        Args:
            post_id: The ID of the post to retrieve.

        Returns:
            A tuple containing the JSON response and status code.
        """
        if self._map.get(post_id) is not None:
            return jsonify(self._data[self._map.get(post_id)]), 200
        return jsonify({'error': f'Post with id <{post_id}> not found.'}), 404

    def posts(self, params: dict[str, str]) -> tuple[Response, int]:
        """
        Retrieves all posts, with optional sorting.

        Args:
            params: A dictionary of query parameters for sorting.

        Returns:
            A tuple containing the JSON response and status code.
        """
        if params.get('sort') == 'date':
            return jsonify(sorted(
                self._data, key=lambda post: datetime.strptime(post.get('date'), "%Y-%m-%d"),
                reverse=(params.get('direction', 'asc') == 'desc')
            )), 200

        return jsonify(sorted(
            self._data, key=lambda post: post.get(params.get('sort', 'id')),
            reverse=(params.get('direction', 'asc') == 'desc')
        )), 200

    @staticmethod
    def check_unsupported(post: dict[str, str | list[str] | int]) -> list[str] | list[None]:
        """
        Checks for unsupported fields in a post dictionary.

        Args:
            post: The post dictionary to check.

        Returns:
            A list of unsupported field names.
        """
        unsupported = []
        for key in post:
            if key not in ["title", "content", "author"]:
                unsupported.append(key)
        return unsupported

    @staticmethod
    def check_missing(post: dict[str, str | list[str] | int]) -> list[str] | list[None]:
        """
        Checks for missing required fields in a post dictionary.

        Args:
            post: The post dictionary to check.

        Returns:
            A list of missing field names.
        """
        missing = []
        for key in ["title", "content", "author"]:
            if key not in post:
                missing.append(key)
        return missing

    def add(self, post: dict[str, str | list[str] | int]) -> tuple[Response, int]:
        """
        Adds a new post.

        Args:
            post: The post dictionary to add.

        Returns:
            A tuple containing the JSON response and status code.
        """
        if not post.get('author'):  # This is just in here for now because the frontend doesn't support it yet.
            post['author'] = 'unknown'

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

    def delete(self, post_id: int) -> tuple[Response, int]:
        """
        Deletes a post by its ID.

        Args:
            post_id: The ID of the post to delete.

        Returns:
            A tuple containing the JSON response and status code.
        """
        if self._map.get(post_id) is not None:
            self._data.pop(self._map.get(post_id))
            self._set()
            return jsonify({"message": f"Post with id <{post_id}> deleted."}), 200
        return jsonify({'error': f'Post with id <{post_id}> not found.'}), 404

    def update(self, post_id: int, params: dict[str, str | list[str] | int]) -> tuple[Response, int]:
        """
        Updates an existing post.

        Args:
            post_id: The ID of the post to update.
            params: The dictionary with the fields to update.

        Returns:
            A tuple containing the JSON response and status code.
        """
        if self._map.get(post_id) is not None:
            missing = self.check_missing(params)
            if len(missing) == 3:
                return jsonify({'error': f'No supported fields. Supported: {missing}'}), 400

            unsupported = self.check_unsupported(params)
            if unsupported:
                return jsonify({'error': f'Unsupported fields: {unsupported}'}), 400

            self._data[self._map.get(post_id)].update(params)
            self._set()
            return jsonify(self._data[self._map.get(post_id)]), 200
        return jsonify({'error': f'Post with id <{post_id}> not found.'}), 404

    def filter(self, key: str, value: int | str) -> None:
        """
        Filters the result list based on a key-value pair.

        Args:
            key: The key to filter by.
            value: The value to match.
        """
        if value:
            self._result = [post for post in self._result if str(value).lower() in str(post.get(key)).lower()]

    def search(self, params: dict[str, str | list[str] | int]) -> tuple[Response, int]:
        """
        Searches posts based on query parameters.

        Args:
            params: A dictionary of query parameters for searching.

        Returns:
            A tuple containing the JSON response and status code.
        """
        self._result = self._data.copy()
        for param in params:
            self.filter(param, params.get(param))
            if not self._result:
                return jsonify({'error': 'No posts found.'}), 404
        return jsonify(self._result), 200
