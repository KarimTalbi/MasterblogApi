from flask import Flask, jsonify, request
from flask_cors import CORS
from data.json_handler import JsonHandler
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    posts = JsonHandler()

    if request.method == 'POST':
        data = request.get_json()

        if not data['title'] or not data['content']:
            return {'error': f'Missing fields: {[key for key, value in data.items() if not value]}'}, 400

        new_post = posts.add(data)
        return jsonify(new_post), 201

    return jsonify(posts.get(request.args)), 200


@app.route('/api/posts/<int:post_id>', methods=['GET', 'DELETE', 'PUT', 'POST'])
def handle_post(post_id):
    posts = JsonHandler()

    if request.method == 'GET':
        post = posts.post(post_id)
        if post:
            return jsonify(post), 200

    if request.method == 'DELETE':
        delete = posts.delete(post_id)
        if delete:
            return jsonify(delete), 200

    data = request.get_json()

    if request.method == 'PUT':
        update = posts.update(post_id, data)
        if update:
            return jsonify(update), 200

    if request.method == 'POST':
        attach = posts.attach(post_id, data)
        if attach:
            return jsonify(attach), 201

    return {'error': f'Post with id <{post_id}> not found.'}, 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    posts = JsonHandler()
    search_result = posts.search(request.args)
    if search_result:
        return jsonify(search_result), 200

    return {'error': 'No posts found.'}, 404


SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
