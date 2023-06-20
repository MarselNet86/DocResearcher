from flask import render_template, redirect, request, send_file, flash, url_for, abort, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json
import hmac
from sweater import app, db, mail, Message
from sweater.models import Users, Files
from werkzeug.security import check_password_hash, generate_password_hash
from email_validate import validate, validate_or_fail


def get_captcha_query(lot_number, captcha_key):
    lotnumber_bytes = lot_number.encode()
    prikey_bytes = captcha_key.encode()
    sign_token = hmac.new(prikey_bytes, lotnumber_bytes, digestmod='SHA256').hexdigest()
    captcha_output = request.form.get('captcha_output', '')
    pass_token = request.form.get('pass_token', '')
    gen_time = request.form.get('gen_time', '')

    query = {
        "lot_number": lot_number,
        "captcha_output": captcha_output,
        "pass_token": pass_token,
        "gen_time": gen_time,
        "sign_token": sign_token,
    }
    return query


def check_captcha(query, captcha_id, api_server):
    url = api_server + '/validate' + '?captcha_id={}'.format(captcha_id)
    try:
        res = requests.post(url, query)
        assert res.status_code == 200
        gt_msg = json.loads(res.text)
        if 'result' in gt_msg and gt_msg['result'] == 'success':
            return True
        else:
            flash('Ошибка при проверке капчи!')
            return False
    except Exception as e:
        flash('Ошибка при проверке капчи!')
        return False


def check_mail(user_mail):
    result = validate(
        email_address=user_mail,
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=False,
        smtp_debug=False
    )
    return result


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('review'))

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = Users.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                captcha_id = '54cd0af70168ed6991797bf2a431c806'
                captcha_key = '676df60bd796084e9dd458fcef310579'
                api_server = 'http://gcaptcha4.geetest.com'
                lot_number = request.form.get('lot_number', '')
                query = get_captcha_query(lot_number, captcha_key)

                if check_captcha(query, captcha_id, api_server):
                    login_user(user)
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'error', 'message': 'Captcha validation failed'})
            else:
                return jsonify({'status': 'error', 'message': 'Неверный логин или пароль!'})
        else:
            return jsonify({'status': 'error', 'message': 'Введите логин и пароль!'})

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('review'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([full_name, email, password, confirm_password]):
            return redirect(url_for('register'))

        count_name = len(full_name.split())
        if count_name not in [2, 3]:
            return jsonify({'status': 'error', 'message': 'Некорректный ввод ФИО'})

        if check_mail(email) is False:
            return jsonify({'status': 'error', 'message': 'Некорректный формат почты!'})

        if password != confirm_password:
            return jsonify({'status': 'error', 'message': 'Пароли не совпадают!'})

        user = Users.query.filter_by(email=email).first()
        if user:
            return jsonify({'status': 'error', 'message': 'Пользователь с данным email уже существует!'})

        captcha_id = '578ba69a0712355259c25102cb404832'
        captcha_key = 'a8efe0b06e97d94efe7c5af504a47a7b'
        api_server = 'http://gcaptcha4.geetest.com'
        lot_number = request.form.get('lot_number', '')
        query = get_captcha_query(lot_number, captcha_key)

        if check_captcha(query, captcha_id, api_server):
            hashed_password = generate_password_hash(password)
            new_user = Users(full_name=full_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Регистрация прошла успешно!'})
        else:
            return jsonify({'status': 'error', 'message': 'Ошибка капчи!'})

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
