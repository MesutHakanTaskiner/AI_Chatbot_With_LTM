from flask import Flask, request, jsonify, render_template
from ai_operations import get_answer, delete_session_thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    session_id = data.get('session', None)

    print(f"Question: {question}, Session: {session_id}")
    response = get_answer(question, session_id)

    return jsonify({'response': response, 'session': session_id})

@app.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    delete_session_thread(session_id)
    # Dummy session deletion
    print(f"Session {session_id} deleted    ")
    return jsonify({'status': 'deleted', 'session_id': session_id})


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
