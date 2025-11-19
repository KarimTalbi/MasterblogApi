from flask import Flask, jsonify, request
from flask_cors import CORS
from data.json_handler import JsonHandler

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        data = request.get_json()
        new_post = {
            "id": unique_post_id(),
            "title": data.get('title'),
            "content": data.get('content')
        }
        if not new_post['title'] or not new_post['content']:
            return {'error': f'Missing fields: {[key for key, value in new_post.items() if not value]}'}, 400
        POSTS.append(new_post)
        return jsonify(new_post), 201

    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if per_page > 30:
            per_page = 30

        sort = request.args.get('sort', 'id')
        direction = request.args.get('direction', 'asc')

        sorted_posts = sorted(POSTS, key=lambda post: post.get(sort), reverse=(direction == 'desc'))
        start = page * per_page - per_page
        end = page * per_page
        return jsonify(sorted_posts[start:end]), 200


@app.route('/api/auth/login', methods=['POST'])
def login():
    pass


@app.route('/api/auth/register', methods=['POST'])
def register():
    pass


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT', 'POST'])
def handle_post(post_id):
    global POSTS
    if request.method == 'DELETE':
        post_count = len(POSTS)
        POSTS = [post for post in POSTS if post['id'] != post_id]
        if len(POSTS) == post_count:
            return {'error': f'Post with id <{post_id}> not found.'}, 404
        return {'message': f'Post with id <{post_id}> has been deleted successfully.'}, 200

    elif request.method == 'PUT':
        data = request.get_json()
        for i, post in enumerate(POSTS):
            if post['id'] == post_id:
                for key in post:
                    POSTS[i][key] = data.get(key) if data.get(key) else post[key]
                return jsonify(POSTS[i]), 200
        return {'error': f'Post with id <{post_id}> not found.'}, 404

    elif request.method == 'POST':
        data = request.get_json()

        for key, value in data.items():
            if key not in ['comments', 'categories', 'tags']:
                return {'error': f'Invalid field: <{key}>'}, 400

            if key == 'comments':
                if not isinstance(data.get('comments'), dict):
                    return {'error': 'Wrong datatype for field: <comments>'}, 400

                if not data['comments'].get('user_id'):
                    return {'error': 'Missing field: <user>'}, 400

                if not data['comments'].get('comment'):
                    return {'error': 'Missing field: <comment>'}, 400

            for i, post in enumerate(POSTS):
                if post['id'] == post_id:
                    if key not in post:
                        POSTS[i][key] = []

                    if not key == 'comments' and value in POSTS[i][key]:
                        return {
                            'error': f'{key}: <{value}> already exists for post with id <{post_id}>'
                        }, 400

                    POSTS[i][key].append(data.get(key))

                    return jsonify(POSTS[i]), 201
    return None


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title', '')
    content = request.args.get('content', '')
    search_result = [
        post for post in POSTS if title.lower() in post['title'].lower() and content.lower() in post['content'].lower()
    ]
    return jsonify(search_result), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
