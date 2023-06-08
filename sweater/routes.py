from flask import render_template, redirect, request, send_file, flash, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json
import hmac
from sweater import app, db
from sweater.models import Users, Files
from werkzeug.security import check_password_hash, generate_password_hash
from main import process_excel_files
from flask import jsonify
from babel.dates import format_date


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/community', methods=['GET'])
def deep():
    return render_template('community.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = Users.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                # Проверка капчи GeeTest V4
                captcha_id = '54cd0af70168ed6991797bf2a431c806'
                captcha_key = '676df60bd796084e9dd458fcef310579'
                api_server = 'http://gcaptcha4.geetest.com'

                lot_number = request.form.get('lot_number', '')
                captcha_output = request.form.get('captcha_output', '')
                pass_token = request.form.get('pass_token', '')
                gen_time = request.form.get('gen_time', '')

                lotnumber_bytes = lot_number.encode()
                prikey_bytes = captcha_key.encode()
                sign_token = hmac.new(prikey_bytes, lotnumber_bytes, digestmod='SHA256').hexdigest()

                query = {
                    "lot_number": lot_number,
                    "captcha_output": captcha_output,
                    "pass_token": pass_token,
                    "gen_time": gen_time,
                    "sign_token": sign_token,
                }

                url = api_server + '/validate' + '?captcha_id={}'.format(captcha_id)

                try:
                    res = requests.post(url, query)
                    assert res.status_code == 200
                    gt_msg = json.loads(res.text)
                    if 'result' in gt_msg and gt_msg['result'] == 'success':
                        login_user(user)
                        next_page = request.args.get('next')
                        if next_page:
                            return redirect(next_page)
                        else:
                            return redirect(url_for('panel'))
                    else:
                        flash('Неверный логин или пароль!')
                        return redirect(url_for('auth'))  # Возвращаемся на страницу авторизации
                except Exception as e:
                    flash('Ошибка при проверке капчи!')
                    return redirect(url_for('auth'))  # Возвращаемся на страницу авторизации
            else:
                flash('Неверный логин или пароль!')
                return redirect(url_for('auth'))  # Возвращаемся на страницу авторизации
        else:
            flash('Введите логин и пароль!')
            return redirect(url_for('auth'))  # Возвращаемся на страницу авторизации

    return render_template('auth.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if request.method == 'POST':
        if not (full_name or email or password or confirm_password):
            flash('Заполните все поля!')

        elif password != confirm_password:
            flash('Пароли не совпадают!')

        else:
            hashed_password = generate_password_hash(password)
            new_user = Users(full_name=full_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('auth') + '?next=' + request.url)

    return response


@app.route('/review', methods=['GET'])
@login_required
def review():
    user = current_user
    full_name = user.full_name
    first_name = full_name.split()[1]
    email = user.email
    register_time = format_date(user.register_time, "d MMMM, yyyyг", locale="ru")  # Форматируем дату

    files_quantity = Files.query.filter_by(fk_id=user.id).count()  # Используем count() вместо all()
    return render_template('review.html', first_name=first_name, full_name=full_name,
                           email=email, files_quantity=files_quantity, register_time=register_time)


@app.route('/panel', methods=['GET'])
@login_required
def panel():
    full_name = current_user.full_name
    first_name = full_name.split()[1]
    return render_template('panel.html', first_name=first_name)


@app.route('/user_documents', methods=['GET'])
@login_required
def user_documents():
    full_name = current_user.full_name
    first_name = full_name.split()[1]
    files = Files.query.filter_by(fk_id=current_user.id).all()
    for file in files:
        file.request_time = file.request_time.strftime("%d.%m.%Y - %H:%M")
    return render_template('user_documents.html', first_name=first_name, files=files)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    zip_filename = process_excel_files(file)
    print(zip_filename)

    new_file = Files(fk_id=current_user.id, file_id=zip_filename)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'zip_filename': zip_filename})


@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    # Путь к файлу, который вы хотите скачать
    file_path = f'download/{filename}'

    # Отправляем файл клиенту для скачивания
    return send_file(file_path, as_attachment=True)


@app.route('/delete_file/<filename>', methods=['GET'])
@login_required
def delete_file(filename):
    # Находим файл в базе данных по имени файла
    file = Files.query.filter_by(file_id=filename).first()

    # Если файл с таким именем не найден, возвращаем ошибку 404
    if file is None:
        abort(404)

    # Если файл найден, удаляем его из базы данных
    db.session.delete(file)
    db.session.commit()

    # После удаления файла, перенаправляем пользователя обратно на страницу с его документами
    return redirect(url_for('user_documents'))



@app.route('/docs_templates/<filename>', methods=['GET'])
@login_required
def download_template(filename):
    # Путь к файлу, который вы хотите скачать
    file_path = f'docs_templates/{filename}'
    # Отправляем файл клиенту для скачивания
    return send_file(file_path, as_attachment=True)