from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import *
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "admin@gmail.com":
            return redirect(url_for('admin.admin_redirect'))

        user=User.query.filter_by(email=email).first()
        if not user:
            flash('Usuario no existe', category='error')
        elif user.password != password:
            flash('Contraseña incorrecta', category='error')
        else:
            flash('Se ha logueado exitosamente', category='success')
            login_user(user)
            return redirect(url_for('views.home'))

    return render_template('login.html', user=None, l=True)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if len(password)<7:
            flash('La contraseña debe tener 7 o más caracteres.', category='error')
        elif password != confirm:
            flash('La contraseña debe coincidir.', category='error')
        else:
            print(role)
            new_user = User(role=role,name=name, email=email, password=password, dob='', nationality='', contact_no='', address='')
            db.session.add(new_user)
            db.session.commit()

            user=User.query.filter_by(email=email).first()

            login_user(user)

            flash('Cuenta creada exitosamente', category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html', user=None, r=True, l=True)

@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))