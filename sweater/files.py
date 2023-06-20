from flask import render_template, redirect, request, send_file, flash, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json
import hmac
from random import randint
from sweater import app, db, mail, Message
from sweater.models import Users, Files
from werkzeug.security import check_password_hash, generate_password_hash
from main import process_excel_files
from flask import jsonify
from babel.dates import format_date


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']

        # Проверка, что файл является файлом .xlsx
        if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            return jsonify({'error': 'Invalid file type. Please upload a .xlsx file.', 'status': 'error'})

        file_id, group = process_excel_files(file) # принимаем имя файла и значение группы

        new_file = Files(fk_id=current_user.id, file_id=file_id, group=group)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({'zip_filename': f'{group}_{file_id}', 'status': 'success'}) # передаем значение группы в jsonify
    except (IndexError, AttributeError) as e: # обрабатываем ошибки IndexError и AttributeError
        return jsonify({'error': str(e), 'status': 'error'}) # отправляем ошибку



@app.route('/download/<filename>', methods=['GET', 'POST'])
@login_required
def download_file(filename):
    # Путь к файлу, который вы хотите скачать
    file_path = f'download/{filename}'  # добавляем расширение .zip

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