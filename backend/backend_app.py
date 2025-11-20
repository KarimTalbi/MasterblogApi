"""
This module implements a simple Flask API for a blog.

It provides CRUD (Create, Read, Update, Delete) functionality for blog posts,
as well as a search endpoint. The API is documented using Swagger UI.
"""
import json
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from data.json_handler import Posts
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts() -> tuple[Response, int]:
    """
    Handles GET and POST requests for the /api/posts endpoint.

    GET: Returns a list of all posts, with optional sorting.
    POST: Creates a new post.

    Returns:
        A Flask response object.
    """
    posts = Posts()

    if request.method == 'POST':
        data = request.get_json()
        return posts.add(data)

    return posts.posts(request.args)


@app.route('/api/posts/<int:post_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_post(post_id: int) -> tuple[Response, int]:
    """
    Handles GET, DELETE, and PUT requests for a single post.

    Args:
        post_id: The ID of the post to handle.

    Returns:
        A Flask response object.
    """
    posts = Posts()

    if request.method == 'GET':
        return posts.post(post_id)

    if request.method == 'DELETE':
        return posts.delete(post_id)

    if request.method == 'PUT':
        data = request.get_json()
        return posts.update(post_id, data)

    return jsonify({'error': f'Post with id <{post_id}> not found.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts() -> tuple[Response, int]:
    """
    Handles GET requests for the /api/posts/search endpoint.

    Searches for posts based on query parameters.

    Returns:
        A Flask response object.
    """
    posts = Posts()
    return posts.search(request.args)


@app.errorhandler(404)
def not_found(error: Exception) -> tuple[Response, int]:
    """
    Handles 404 Not Found errors.

    Args:
        error: The error object.

    Returns:
        A JSON response with a 404 status code.
    """
    print(error)
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(json.JSONDecodeError)
def json_decode_error(error: json.JSONDecodeError) -> tuple[Response, int]:
    """
    Handles JSON decoding errors.

    Args:
        error: The error object.

    Returns:
        A JSON response with a 404 status code.
    """
    print(error)
    return jsonify({'error': 'Invalid JSON format'}), 404


@app.errorhandler(500)
def internal_error(error: Exception) -> tuple[Response, int]:
    """
    Handles 500 Internal Server errors.

    Args:
        error: The error object.

    Returns:
        A JSON response with a 500 status code.
    """
    print(error)
    return jsonify({'error': 'Internal server error'}), 500


SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)