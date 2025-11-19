from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def unique_id():
    return max(post['id'] for post in POSTS) + 1


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        data = request.get_json()
        new_post = {
            "id": unique_id(),
            "title": data.get('title'),
            "content": data.get('content')
        }
        if not new_post['title'] or not new_post['content']:
            return {'error': f'Missing fields: {[key for key, value in new_post.items() if not value]}'}, 400
        POSTS.append(new_post)
        return jsonify(new_post), 201

    else:
        sort = request.args.get('sort', 'id')
        direction = request.args.get('direction', 'asc')

        sorted_posts = sorted(POSTS, key=lambda post: post.get(sort), reverse=(direction == 'desc'))
        return jsonify(sorted_posts), 200


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
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

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title','')
    content = request.args.get('content', '')
    search_result = [
        post for post in POSTS if title.lower() in post['title'].lower() and content.lower() in post['content'].lower()
    ]
    return jsonify(search_result), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
