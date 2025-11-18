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
            return jsonify({'error': f'Missing fields: {[key for key, value in new_post.items() if not value]}'})
        return jsonify(new_post), 201
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
