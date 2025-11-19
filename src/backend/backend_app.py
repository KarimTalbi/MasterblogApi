from flask import Flask, jsonify, request
from flask_cors import CORS
from data.json_handler import JsonHandler

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
