from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import timedelta
from flask_jwt_extended import *
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')
db = client.guhaejo

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "guhaejo-secret"
jwt = JWTManager(app)

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_CSRF_IN_COOKIES'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=14)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required(optional=True)
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(logged_in_as=current_user), 200

@app.route('/hello')
@jwt_required(optional=True)
def hello():
    return "hello"

@app.route('/home')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    print(current_user)
    return render_template('index.html')
# @jwt_required(refresh=True)
# def refresh():
#     current_user = get_jwt_identity()
#     print(current_user)
#
#     access_token = create_access_token(identity=current_user)
#     response = jsonify({'flag': 1})
#     set_access_cookies(response, access_token)
#
#     return jsonify({'msg': "재발급 성공"})

#     return render_template('index.html')R

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login', methods=["POST"])
def login():
    user_email = request.form['email_give']
    user_password = request.form['password_give']

    # print(user_email)
    # print(user_password)

    user = db.user.find_one({'email': user_email})
    # print(user)

    if user is None:
        return jsonify({'msg': "이메일이 존재하지 않습니다."});
    if check_password_hash(user['password'], user_password) is False:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다.'});

    access_token = create_access_token(identity=user['email'])
    refresh_token = create_refresh_token(identity=user['email'])

    response = jsonify({'flag': 1})

    # Save tokens into cookie storage
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    # print(access_token)
    # print(refresh_token)
    # return jsonify(access_token=access_token)
    return response, 200

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "로그아웃 하였습니다."})
    unset_jwt_cookies(response)
    return response

@app.route("/signup", methods=["POST"])
def sign_up():
    nickname_receive = request.form['nickname_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    confirm_password_receive = request.form['confirm_password_give']

    print(nickname_receive, email_receive, password_receive)
    # Validation
    if nickname_receive == "":
        return jsonify({'msg': '닉네임을 입력해주세요'})
    elif password_receive == "":
        return jsonify({'msg': '비밀번호를 입력해주세요'})
    elif email_receive == "":
        return jsonify({'msg': '이메일을 입력해주세요'})

    if password_receive != confirm_password_receive:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다'})

    check_dup_email = db.user.find_one({'email': email_receive})
    # print(type(check_dup_email))
    if check_dup_email is None:
        doc = {
            'nickname': nickname_receive,
            'email': email_receive,
            'password': generate_password_hash(password_receive)
        }
        db.user.insert_one(doc)
    elif check_dup_email['email'] == email_receive:
        return jsonify({'msg': '이미 가입된 이메일 입니다.'})

    return jsonify({'flag': 1})

@app.route('/refresh', methods=['GET'])
@jwt_required(optional=False, refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({'flag': 1})
    set_access_cookies(response, access_token)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
