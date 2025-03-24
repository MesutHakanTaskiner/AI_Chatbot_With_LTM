from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    # Dummy processing for the question
    response = f"Baba: {question}"
    return jsonify({'response': response})

@app.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    # Dummy session deletion
    return jsonify({'status': 'deleted', 'session_id': session_id})

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
