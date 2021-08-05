from flask import Flask, render_template, session, request
# from flask_sqlalchemy import SQLAlchemy
import json

from werkzeug.utils import redirect
with open('config.json', 'r') as f:
    params = json.load(f)["params"]

import sqlite3

app = Flask(__name__) 
app.secret_key = 'my-secret-key'


@app.route('/')
def index():
    return render_template('index.html', params=params)

@app.route('/login', methods=['GET','POST'])
def login():
    if ('user' in session and session['user'] == "sid86"):
        return render_template("home.html")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/home', methods=['GET','POST'])
def home():
    login_fail=False
    if ('user' in session and session['user'] == "sid86"):
        # posts = Posts.query.all()
        username = session['user']
        return render_template('home.html', username=username)

    if request.method == 'POST':
        username = request.form.get('username')
        userpass = request.form.get('password')
        try:
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            c.execute(f"SELECT * FROM users WHERE username='{username}'")

            # data processing
            data = c.fetchone()
            conn.commit()
            conn.close()
        except:
            login_fail=True
        # print(data)
        data_username = data[0]
        data_password = data[1]
        
        if (username == data_username and userpass == data_password):
            # set the session variable
            session['user'] = username
            # posts = Posts.query.all()
            return render_template('home.html', username=username)
    return render_template('login.html', login_fail=login_fail)

@app.route(
    '/link/<user>')
def sid(user):
    # connects to database
    conn = sqlite3.connect('linklerz_.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM details WHERE username='{user}'")

    # data processing
    data = c.fetchone()
    conn.commit()
    conn.close()
    link_name = []
    link_address = []
    for i in range(1,4):
        link  = data[i]
        seperate = link.split(">")
        # print(seperate)
        link_name.append(seperate[0])
        link_address.append(seperate[1])
    # print(link_name)
    # print(link_address)
    # lst = ["Instagram", "Facebook", "Whatsupp", "Snapchat"]

    return render_template('link.html', username=user,link_name=link_name,link_address=link_address)

if __name__ == "__main__":
    app.run(debug=True)