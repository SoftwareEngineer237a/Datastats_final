from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm
from app.models import User, db

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            # Redirect by role
            if user.role == 'analyst':
                return redirect(url_for('analyst.dashboard'))
            elif user.role == 'viewer':
                return redirect(url_for('viewer.viewer_dashboard'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
