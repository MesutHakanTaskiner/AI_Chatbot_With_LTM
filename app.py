"""Main Flask application for handling routes and integrating AI operations.
This module sets up routes for asking questions, deleting sessions, and modifying system instructions.
"""

from flask import Flask, request, jsonify, render_template
from ai_operations import AiOperations

app = Flask(__name__)
ai_ops = AiOperations()


@app.route('/')
# Renders the main index page using the 'index.html' template.
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
# Handles the POST /ask route by processing a question and session, then returns a JSON answer.
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    session_id = data.get('session', None)

    print(f"Question: {question}, Session: {session_id}")
    response = ai_ops.get_answer(question, session_id)

    return jsonify({'response': response, 'session': session_id})


@app.route('/session/<session_id>', methods=['DELETE'])
# Handles the DELETE /session/<session_id> route by deleting the related session thread.
def delete_session(session_id):
    ai_ops.delete_session_thread(session_id)
    # Dummy session deletion
    print(f"Session {session_id} deleted    ")
    return jsonify({'status': 'deleted', 'session_id': session_id})


@app.route('/set_system_instruction', methods=['POST'])
# Handles the POST /set_system_instruction route by updating the system instruction.
def system_instruction():
    data = request.get_json()
    instruction = data.get('instruction')
    ai_ops.set_system_instruction(instruction)
    return jsonify({"status": "success", "message": "System instruction received"})


@app.route('/get_system_instruction', methods=['GET'])
# Handles the GET /get_system_instruction route by returning the current system instruction.
def get_system_instruction():
    return jsonify({"system_instruction": ai_ops.get_system_instruction()})

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
