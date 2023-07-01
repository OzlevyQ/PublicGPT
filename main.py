from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import requests
import time
import openai
from flask_ngrok import run_with_ngrok



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)
run_with_ngrok(app)


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            return redirect(url_for('index', username=username))
    return render_template('login.html')

@app.route('/index/<username>')
def index(username):
    return render_template('index.html', username=username)



openai.api_key = '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'

def get_gpt3_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@socketio.on('message')
def handle_message(data):
    message = data['message']
    username = data['username']
    if message.startswith("/צאט"):
        prompt = message.replace("/צאט", "").strip()
        emit('message', {'username': "Chat Bot", 'message': "מקליד..."}, broadcast=True)
        time.sleep(2)
        response = get_gpt3_response(prompt)
        emit('message', {'username': "Chat Bot", 'message': response}, broadcast=True)
    else:
        emit('message', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    app.run()
