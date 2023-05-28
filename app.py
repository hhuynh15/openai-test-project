import os
from flask import Flask, render_template, request, session
import openai

app = Flask(__name__)
app.secret_key = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'  # Use a secure, unique, and secret value here
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def chat():
    if 'messages' not in session:
        session['messages'] = [{'role':'system', 'content':'You are a helpful assistant.'}]

    if request.method == "POST":
        user_message = request.form["message"]
        session['messages'].append({'role':'user', 'content':user_message})

        # Create a chat message for the API
        chat_message = [{'role':msg['role'], 'content':msg['content']} for msg in session['messages']]

        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=chat_message
        )

        assistant_message = response['choices'][0]['message']['content']
        session['messages'].append({'role':'assistant', 'content':assistant_message})

    return render_template("index.html", chat=session['messages'])


if __name__ == "__main__":
    app.run(debug=True)
