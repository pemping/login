from flask import render_template, redirect, request, url_for, flash
from . import auth  # 当前文件夹的 . 相当于 __init__.py
from ..models import User, Permission, Role
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from .email import send_email
from datetime import datetime


# @auth.route('/login')
# def login():
#     # temp = db.users.find({'username': 'ly'})
#     temp = User.objects().all()
#     return render_template('auth/login.html', dbc=temp)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.password = form.password.data
        user.role_id = Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES
        if user.email == "54004267@qq.com":
            r = Role(name='Admin', default=True, permissions=Permission.ADMINISTER)
            r.save()
            user.role = r
        else:
            r = Role(name='User', default=False, permissions=user.role_id)
            r.save()
            user.role = r
        user.save()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('确认邮件已发送，请在邮箱中点击链接激活！')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户激活成功！')
    else:
        flash('账户激活失败！')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.update(last_seen=datetime.utcnow())
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('确认邮件已再次发送，请在邮箱中点击链接激活！')
    return redirect(url_for('main.index'))
