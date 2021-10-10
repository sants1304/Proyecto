from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.engine import url
from .models import *
from . import db

admin = Blueprint('admin', __name__)

def getUserFromid(id):
    if id ==None:
        class X():
            name = 'None Assigned'
        x = X()
        return x
    user = User.query.filter_by(id=id).first()
    return user

def flight_bookings(id):
    cap = 0
    bookings = Booking.query.filter_by(flightid=id).all()
    for i in bookings:
        cap += i.people
    return cap

@admin.route('/')
def admin_redirect():
    return redirect(url_for('admin.comments'))

@admin.route('/user/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        address = request.form.get('address')
        nationlity = request.form.get('nationality')
        contact = request.form.get('contact')
        email = request.form.get('email')

        user = User.query.filter_by(id=current_user.id).first()
        user.name =  name
        user.address = address
        user.dob = dob
        user.nationality = nationlity
        user.contact_no = contact
        user.email = email
        db.session.commit()
        return redirect(url_for('admin.pilots'))
    return render_template('dashboard.html', user=current_user, yes=True)

@admin.route('/user/delete/<id>')
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@admin.route('/user/assign/<id>')
def assign(id):
    try:
        assigned = request.args['assigned']
        flight = Flight.query.filter_by(id=assigned).first()
        flight.pilotid=id
        db.session.commit()
        return redirect('/admin/pilots')
    except:
        pass
    flights = Flight.query.filter_by(pilotid=None).all()
    return render_template('/admin/assign.html', flights=flights)

@admin.route('/customers')
def users():
    users = User.query.filter_by(role='buyer').all()
    return render_template('/admin/users.html', users=users)

#flights.html

@admin.route('/pilots')
def pilots():
    pilots = User.query.filter_by(role='pilot').all()
    return render_template('/admin/pilots.html', pilots=pilots)

@admin.route('/flights')
def flights():
    flights = Flight.query.all()
    return render_template('/admin/flights.html', flights=flights, bookings=flight_bookings, get=getUserFromid, yes=False)

@admin.route('/flight/add', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        airline = request.form.get('airline')
        fromm = request.form.get('from')
        to = request.form.get('to')
        cost = request.form.get('cost')
        capacity = request.form.get('capacity')
        date = request.form.get('date')
        dept = request.form.get('dept-time')
        arr = request.form.get('arr-time')

        new_flight = Flight(airline=airline, origin=fromm, dest=to, cost=cost, capacity=capacity, date=date, dept_time=dept, arr_time=arr)
        db.session.add(new_flight)
        db.session.commit()
        return redirect(url_for('admin.flights'))

    return render_template('/admin/add-flight.html')

@admin.route('/comments')
def comments():
    comments = Feedback.query.all()
    return render_template('/admin/comments.html', comments=comments, get=getUserFromid)