import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from data.json_handler import Posts
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    posts = Posts()

    if request.method == 'POST':
        data = request.get_json()
        return posts.add(data)

    return jsonify(posts.posts(request.args)), 200


@app.route('/api/posts/<int:post_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_post(post_id):
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
def search_posts():
    posts = Posts()
    return posts.search(request.args)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(json.JSONDecodeError)
def json_decode_error(error):
    return jsonify({'error': 'Invalid JSON format'}), 404


@app.errorhandler(500)
def internal_error(error):
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
