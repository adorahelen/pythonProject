from flask import Blueprint, request, jsonify, send_from_directory, redirect, url_for
from models import db, User, Log
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
import json  # Add this import statement


main = Blueprint('main', __name__, static_url_path='', static_folder='build')

#http://localhost:3000/
@main.route('/')
def index():
    return send_from_directory('build', 'index.html')

@main.route('/login')
def login_page():
    return send_from_directory('build', 'index.html')

@main.route('/signup')
def signup_page():
    return send_from_directory('build', 'index.html')

@main.route('/section1')
def index2():
    return send_from_directory('build', 'index.html')

@main.route('/section2')
def index3():
    return send_from_directory('build', 'index.html')

@main.route('/section3')
def index4():
    return send_from_directory('build', 'index.html')

@main.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    # 새 사용자 생성 및 데이터베이스에 추가
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    print(f"Received signup data: {data}")

    # 회원가입 성공 응답
    response = {
        'message': 'User registered successfully',
        'user': {
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
        }
    }

    return jsonify(response), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # 데이터베이스에서 사용자 검색
    user = User.query.filter_by(email=email).first()

    # 사용자가 존재하고 비밀번호가 일치하는지 확인
    if user and user.password == password:
        # 로그인 성공, 홈 화면으로 리디렉션
        response = {
            'message': 'Login successful',
            'redirect': '/',
        }
        return jsonify(response), 200
    else:
        # 로그인 실패, 에러 메시지 반환
        response = {
            'message': 'Login failed. Check your email and password.'
        }
        return jsonify(response), 401

#소켓 통신을 위한 로그 코드 응답 추가 => HTTP 통신을 위한/ 임베디드 측에서 엔드포인트('/log') 부분 맞춰야 함
@main.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()
    if data:
        log = Log(data=json.dumps(data))  # JSON string storage
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Data logged successfully'}), 201
    return jsonify({'message': 'No data received or incorrect format'}), 400