from flask import render_template, redirect, request, send_file, flash, url_for, abort, render_template_string
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc, asc
import requests
import json
import hmac
from random import randint
from sweater import app, db, mail, Message
from sweater.models import Users, Files
from werkzeug.security import check_password_hash, generate_password_hash
from main import process_excel_files
from flask import jsonify
from math import ceil
from babel.dates import format_date


@app.route('/', methods=['GET'])
def index():
    email = current_user.email if current_user.is_authenticated else None
    return render_template('index.html', email=email, user=current_user)


@app.route('/community', methods=['GET'])
def community():
    email = current_user.email if current_user.is_authenticated else None
    return render_template('community.html', email=email, user=current_user)


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
    page_size = request.args.get('pagesize', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    sort = request.args.get('sort', default='request_time', type=str)
    order = request.args.get('order', default='asc', type=str)

    start = (page - 1) * page_size
    end = start + page_size

    sort_column = getattr(Files, sort, None)
    if sort_column is None:
        sort_column = Files.request_time

    if order == 'desc':
        files = Files.query.filter_by(fk_id=current_user.id).order_by(desc(sort_column)).slice(start, end).all()
    else:
        files = Files.query.filter_by(fk_id=current_user.id).order_by(asc(sort_column)).slice(start, end).all()

    files_quantity = Files.query.filter_by(fk_id=current_user.id).count()
    pages = ceil(files_quantity / page_size)
    for file in files:
        file.request_time = file.request_time.strftime("%d.%m.%Y - %H:%M")

    return render_template('user_documents.html', files_quantity=files_quantity, first_name=first_name, files=files, sort=sort, order=order, pages=pages, current_page=page)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)

    return response


@app.errorhandler(404)
def error404(error):
    email = current_user.email if current_user.is_authenticated else None
    return render_template('error404.html', email=email, user=current_user)