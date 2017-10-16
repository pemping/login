from . import main
from flask import render_template, abort, flash, redirect, url_for
from ..models import User
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditProfileAdminForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.objects(username=username).first()
    if user is None:
        abort(404)
    # user = User.objects.first_or_404(username=username)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.save()
        flash('档案更新成功')
        return redirect(url_for('main.user', username=current_user.username))
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<id>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(id):
    # user = User.objects.first_or_404(id=id)
    user = User.objects(id=id).first()
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data
        user.about_me = form.about_me.data

        user.save()
        flash('档案更新成功')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
