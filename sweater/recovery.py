from flask import render_template, redirect, request, send_file, flash, url_for, abort, session
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json
import secrets
import hmac
from random import randint
from sweater import app, db, mail, Message
from sweater.models import Users, Recovery
from werkzeug.security import check_password_hash, generate_password_hash
from main import process_excel_files
from flask import jsonify
from datetime import datetime, timedelta
from babel.dates import format_date


def generate_code():
    return str(randint(100000, 999999))


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            return jsonify({'status': 'error', 'message': 'Введите адрес почты!'})

        user = Users.query.filter_by(email=email).first()

        if not user:
            return jsonify({'status': 'error', 'message': 'Пользователь с таким email не найден.'})

        code = generate_code()
        recovery = Recovery.query.filter_by(fk_id=user.id).first()
        if recovery:
            recovery.recovery_code = code
            recovery.recovery_code_expiry = datetime.utcnow() + timedelta(minutes=10)
        else:
            recovery = Recovery(fk_id=user.id, recovery_code=code, recovery_code_expiry=datetime.utcnow() + timedelta(minutes=10))
            db.session.add(recovery)

        user_ip = request.remote_addr
        user_platform = request.user_agent.platform
        user_device = request.user_agent.browser
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.session.commit()
        msg = Message(f'[//DocResearcher] Восстановление пароля - {current_time}', recipients=[email])
        msg.html = f'<div class="m_-801948374601670110wrapper-box"><div style="background:0 0;background-color:transparent;margin:0 auto;max-width:600px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:0 0;background-color:transparent;width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:20px 0;text-align:center"><div style="background:#fff;background-color:#fff;margin:0 auto;border-radius:4px;max-width:600px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%;border-radius:4px"><tbody><tr><td style="direction:ltr;font-size:0;padding:48px 16px;text-align:center"><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:24px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top" width="100%"><tbody><tr><td align="center" style="font-size:0;padding:0;word-break:break-word"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0"><tbody><tr><td style="width:336px"><img height="auto" src="https://i.ibb.co/34vXkbY/dr.png" style="border:0;display:block;outline:0;text-decoration:none;height:auto;width:100%;font-size:13px" width="171" class="CToWUd" data-bit="iit"></td></tr></tbody></table></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:24px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"><tbody><tr><td style="background-color:#d4e3f1;border-radius:4px;vertical-align:top;padding:12px 24px"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"><tbody><tr><td align="left" style="font-size:0;padding:0;word-break:break-word"><div style="font-family:URWDIN;font-size:16px;line-height:24px;text-align:left;color:rgb(12, 67, 140)"><u></u>  Буп-Бип-Буп... Восстановление учетной записи. <u></u></div></td></tr></tbody></table></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:12px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top" width="100%"><tbody><tr><td align="left" style="font-size:0;padding:0;word-break:break-word"><div style="font-family:URWDIN;font-size:14px;line-height:22px;text-align:left;color:rgba(1,8,30,.6)">Уважаемый пользователь //DocResearcher,</div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:12px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top" width="100%"><tbody><tr><td align="left" style="font-size:0;padding:0;word-break:break-word"><div style="font-family:URWDIN;font-size:14px;line-height:22px;text-align:left;color:rgba(1,8,30,.6)">Код восстановления:</div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:12px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"><tbody><tr><td style="vertical-align:top;padding:0"><table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"><tbody><tr><td align="left" style="font-size:0;padding:0;word-break:break-word"><div style="font-family:URWDIN;font-size:34px;font-weight:500;line-height:48px;text-align:left;color:#01081e">{code}</div></td></tr></tbody></table></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:24px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top" width="100%"><tbody><tr><td align="left" style="font-size:0;padding:0;word-break:break-word"><div style="font-family:URWDIN;font-size:14px;line-height:22px;text-align:left;color:rgba(1,8,30,.6)">Этот код будет действителен в течение 10 минут. Не сообщайте этот код никому, включая сотрудников //DocResearcher.</div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="direction:ltr;font-size:0;padding:0;padding-bottom:24px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top" width="100%"><tbody><tr><td align="left" class="m_-801948374601670110list" style="background:rgba(0,10,30,.02);font-size:0;padding:10px 25px;word-break:break-word"><table cellpadding="0" cellspacing="0" width="100%" border="0" style="color:#000;font-family:URWDIN;font-size:13px;line-height:22px;table-layout:auto;width:100%;border:none"><tbody><tr><td valign="top" class="m_-801948374601670110list-title">Аккаунт:</td><td valign="top" class="m_-801948374601670110list-content"> <a href="mailto:{email}" target="_blank">{email}</a> </td></tr><tr><td valign="top" class="m_-801948374601670110list-title">IP:</td><td valign="top" class="m_-801948374601670110list-content"> {user_ip} </td></tr><tr><td valign="top" class="m_-801948374601670110list-title">Платформа:</td><td valign="top" class="m_-801948374601670110list-content"> {user_platform} </td></tr><tr><td valign="top" class="m_-801948374601670110list-title">Устройство:</td><td valign="top" class="m_-801948374601670110list-content"> {user_device} </td></tr><tr><td valign="top" class="m_-801948374601670110list-title">Время:</td><td valign="top" class="m_-801948374601670110list-content"> {current_time} </td></tr></tbody></table></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="margin:0 auto;max-width:568px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tbody><tr><td style="border-top:1px solid rgba(0,10,30,.08);direction:ltr;font-size:0;padding:0;padding-top:48px;text-align:center"><div class="m_-801948374601670110mj-column-per-100" style="font-size:0;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top" width="100%"><tbody><tr><td align="center" style="font-size:0;padding:0;word-break:break-word"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table"><tbody><tr><td style="padding:4px 8px"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:32px"><tbody><tr><td style="font-size:0;height:32px;vertical-align:middle;width:32px"><a href="https://www.youtube.com/channel/UCa-eL3mjZsc3zxz_w6pg3WA" target="_blank"><img height="32" src="https://i.ibb.co/4M6c0Kz/youtube.png" style="border-radius:3px;display:block" width="32" class="CToWUd" data-bit="iit"></a></td></tr></tbody></table></td></tr></tbody></table><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table"><tbody><tr><td style="padding:4px 8px"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:32px"><tbody><tr><td style="font-size:0;height:32px;vertical-align:middle;width:32px"><a href="https://vk.com/marselnet" target="_blank"><img height="32" src="https://i.ibb.co/BrNJVJh/vk.png" style="border-radius:3px;display:block" width="32" class="CToWUd" data-bit="iit"></a></td></tr></tbody></table></td></tr></tbody></table><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table"><tbody><tr><td style="padding:4px 8px"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:32px"><tbody><tr><td style="font-size:0;height:32px;vertical-align:middle;width:32px"><a href="https://github.com/marselnet86" target="_blank" ><img height="32" src="https://i.ibb.co/6F6493p/github.png" style="border-radius:3px;display:block" width="32" class="CToWUd" data-bit="iit"></a></td></tr></tbody></table></td></tr></tbody></table><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="float:none;display:inline-table"><tbody><tr><td style="padding:4px 8px"><table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-radius:3px;width:32px"><tbody><tr><td style="font-size:0;height:32px;vertical-align:middle;width:32px"><a href="https://t.me/marselnet" target="_blank"><img height="32" src="https://i.ibb.co/9NV4F0J/free-icon-telegram-2111644.png" style="border-radius:3px;display:block" width="32" class="CToWUd" data-bit="iit"></a></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td align="center" style="font-size:0;padding:10px 25px;word-break:break-word"><div style="font-family:URWDIN;font-size:13px;line-height:1;text-align:center;color:rgba(1,8,30,.38)">Присоединяйтесь к сообществу //DocResearcher и откройте мир возможностей!</div></td></tr></tbody></table></div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style="height:24px">&nbsp;</div><div style="background:#fff;background-color:#fff;margin:0 auto;border-radius:4px;max-width:600px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%;border-radius:4px"><tbody><tr><td style="direction:ltr;font-size:0;padding:24px 40px;text-align:center"><div style="margin:0 auto;max-width:520px"><table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%"></div></td></tr></tbody></table></div></div>'
        mail.send(msg)

        return jsonify({'status': 'success', 'message': 'Код успешно отправлен.'})

    return render_template('recovery.html')


@app.route('/check_code', methods=['POST'])
def check_code():
    email = request.form.get('email')
    code = request.form.get('code')

    if not email or not code:
        return jsonify({'status': 'error', 'message': 'Заполните все поля'})

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'Пользователь с таким email не найден.'})

    recovery = Recovery.query.filter_by(fk_id=user.id).first()
    if recovery and recovery.recovery_code == code:
        if datetime.utcnow() > recovery.recovery_code_expiry:
            return jsonify({'status': 'error', 'message': 'Срок действия кода истек.'})

        session['email'] = email
        session['token'] = secrets.token_urlsafe(16)

        db.session.delete(recovery)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Код подтвержден.', 'token': session['token']})
    else:
        return jsonify({'status': 'error', 'message': 'Неправильный код. Попробуйте снова.'})


@app.route('/change_password/<email>', methods=['GET', 'POST'])
def change_password(email):
    if not session.get('email') == email or not session.get('token'):
        flash('Недействительный токен восстановления аккаунта! Попробуйте снова', 'danger')
        return redirect(url_for('recovery'))

    if request.method == 'POST':
        if not session.get('email') == email or not request.headers.get('X-Auth-Token') == session['token']:
            flash('Недействительный токен восстановления аккаунта! Попробуйте снова', 'danger')
            return redirect(url_for('recovery'))

        user = Users.query.filter_by(email=email).first()
        password = request.form.get('password')
        password_confirm = request.form.get('confirm-password')

        if password != password_confirm:
            return jsonify({'status': 'error', 'message': 'Пароли не совпадают.'})
        elif len(password) < 8:
            return jsonify({'status': 'error', 'message': 'Пароль должен быть больше 8 символов'})
        else:
            if user:
                hashed_password = generate_password_hash(password)
                user.password = hashed_password
                db.session.commit()

                # Сброс данных сессии
                session.pop('email', None)
                session.pop('token', None)

                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'Пользователь не найден.'})

    return render_template('change_password.html', email=email)
