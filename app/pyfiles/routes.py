import json

import pandas as pd
from flask import render_template, session, redirect, request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.pyfiles.functions import update_user_last_request
from app.pyfiles.models.post import Post
from app.pyfiles.models.user import User


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if request.method == 'GET':
            # token = request.args.get('token')
            return func(*args, **kwargs)
        else:
            try:
                token = json.loads(request.get_data().decode('utf-8'))['token']
            except Exception as ex:
                return make_response('Token is missing!', 403, {'data': ex})
        if not token:
            return make_response('Token is missing!', 403, {'data': 'Please, enter login and password!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as ex:
            session.pop('username', None)
            # return redirect('login')
            return make_response('Error in token!', 403, {'data': ex})
        if datetime.strptime(payload['expiration'], '%Y-%m-%d %H:%M:%S.%f') < datetime.utcnow():
            session.pop('username', None)
            # return redirect('login')
            return make_response('Token is expired!', 403, {'data': 'Ex'})
        return func(*args, **kwargs)
    return decorated


@app.route('/', methods=['GET'])
def index():
    if not session.get("username"):
        return redirect('login')
    username = session.get('username')
    update_user_last_request(username)
    return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = json.loads(request.get_data().decode('utf-8'))
    username = data.get('login')
    password = data.get('password')
    if username and password:
        user = User.query.filter_by(username=username).first()
        # create checking login and password id db
        if user:
            if check_password_hash(user.password, password):
                session['username'] = username
                token = jwt.encode({
                    'user': username,
                    'expiration': str(datetime.utcnow() + timedelta(minutes=15))
                },
                    app.config['SECRET_KEY']
                )
                update_user_last_request(username)
                return jsonify({'token': token})
            else:
                return make_response('Login or password is not correct.', 401,
                                     {'data': 'Login or password is not correct.'})
        else:
            return make_response('Login is not correct.', 401,
                                 {'data': 'Login is not correct.'})
    return make_response('Please, enter login and password!', 401, {'data': 'Please, enter login and password!'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("username"):
        return redirect('index')
    if request.method == 'GET':
        return render_template('register.html')
    data = json.loads(request.get_data().decode('utf-8'))
    username = data.get('login')
    password = data.get('password')
    password2 = data.get('password')
    if username and password and password == password2:
        user = User.query.filter_by(username=username).first()
        if user:
            return make_response('User already exists!', 401, {'data': 'User already exists!'})
        h_password = generate_password_hash(password)
        user = User(username=username, password=h_password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            return make_response('Error in db', 500, {'data': ex})
        session['username'] = username
        token = jwt.encode({
            'user': username,
            'expiration': str(datetime.utcnow() + timedelta(minutes=15))
        },
            app.config['SECRET_KEY']
        )
        update_user_last_request(username)
        return jsonify({'token': token})
    return make_response('Please, enter proper login and password!', 401, {'data': 'Please, enter login and password!'})


@app.route('/logout', methods=['POST'])
@token_required
def logout():
    username = session.get('username')
    update_user_last_request(username)
    session.pop('username', None)
    return render_template('login.html')


@app.route('/create_post', methods=['GET', 'POST'])
@token_required
def create_post():
    if request.method == 'GET':
        return render_template('createPost.html')
    data = json.loads(request.get_data().decode('utf-8'))
    header = data['header']
    content = data['content']
    username = session.get('username')
    update_user_last_request(username)
    if header and content:
        user = User.query.filter_by(username=username).first()
        user_id = user.get_info()['user_id']
        post = Post(header=header, content=content, author=user_id, date=datetime.utcnow())
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as ex:
            return make_response('Error in db - {}'.format(ex), 500)
        return jsonify({'status': 'Done!'})
    return make_response('Input header and content!', 403)


@app.route('/get_posts', methods=['GET'])
def get_posts():
    username = session['username']
    update_user_last_request(username)
    sql_posts = Post.query.all()
    posts_info = [post.get_info() for post in sql_posts]
    for post in posts_info:
        author = User.query.get(post['author'])
        author_info = author.get_info()
        post['author'] = author_info['username']
        user = User.query.filter_by(username=username).first()
        user_info = user.get_info()
        likes = json.loads(post['likes'].replace('\'', '\"'))
        if len(likes) == 0:
            post['likes'] = 0
            post['liked'] = False
        else:
            people_liked = []
            for like in likes:
                people_liked.extend(likes[like])
            post['likes'] = len(people_liked)
            if user_info['user_id'] in people_liked:
                post['liked'] = True
            else:
                post['liked'] = False
    posts_info.reverse()
    return jsonify({'posts': posts_info}), 200


@app.route('/like_unlike_post', methods=['POST'])
@token_required
def like_unlike_post():
    data = json.loads(request.get_data().decode('utf-8'))
    post_id = data['post_id']
    username = session['username']
    update_user_last_request(username)
    user = User.query.filter_by(username=username).first()
    user_id = user.get_info()['user_id']
    post = Post.query.get(post_id)
    post_likes = json.loads(post.get_info()['likes'].replace('\'', '\"'))
    this_date = datetime.utcnow().strftime('%Y-%m-%d')
    people_liked = []
    for like in post_likes:
        people_liked.extend(like)
    if user_id in people_liked:
        for day in post_likes:
            if user_id in post_likes[day]:
                post_likes[day].remove(user_id)
                break
    else:
        if this_date not in post_likes:
            post_likes[this_date] = [user_id]
        else:
            post_likes[this_date].append(user_id)
    try:
        post.likes = str(post_likes)
        db.session.commit()
    except Exception as ex:
        return make_response('Error in db - {}'.format(ex), 500)
    return jsonify({'status': 'Done!'})


# "analitics" was in task description. You can use both of them
# do not know if I need to put here toke by task description
@app.route('/api/analitics/', methods=['GET'])
@app.route('/api/analytics/', methods=['GET'])
def analytics():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    dates_series = pd.date_range(date_from, date_to)
    aggregated_likes = {date.strftime('%Y-%m-%d'): 0 for date in dates_series}

    posts = Post.query.all()
    posts_likes = [json.loads(post.get_info()['likes'].replace('\'', '\"')) for post in posts]
    for date in aggregated_likes:
        for post in posts_likes:
            if date in post:
                aggregated_likes[date] += len(post[date])
    return jsonify({'status': 'Ok', 'data': aggregated_likes})


