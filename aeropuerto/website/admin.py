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

def get_flightcode(flight):
    rep = ''
    origin = flight.origin
    dest = flight.dest
    airline = flight.airline
    id = flight.id
    ret = origin.split(' ')
    ret+=(dest.split(' '))
    ret+=(airline.split(' '))
    for r in ret:
        rep += str(r[0]).upper()
    rep+=str(id)
    return rep

@admin.route('/')
def admin_redirect():
    return redirect(url_for('admin.comments'))

@admin.route('/user/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        address = request.form.get('address')
        nationlity = request.form.get('nationality')
        contact = request.form.get('contact')
        email = request.form.get('email')
        flash('Los cambios se han guardado exitosamente', category='success')

        user = User.query.filter_by(id=id).first()
        user.name =  name
        user.address = address
        user.dob = dob
        user.nationality = nationlity
        user.contact_no = contact
        user.email = email
        db.session.commit()
        if user.role == 'buyer':
            return redirect(url_for('admin.users'))
        else:
            return redirect(url_for('admin.pilots'))
    return render_template('dashboard.html', user=user, yes=True)

@admin.route('/user/delete/<id>', methods=['GET'])
def delete(id):
    user = User.query.filter_by(id=id).first()
    flash('Usuario eliminado '+user.name, category='success')
    db.session.delete(user)
    db.session.commit()
    if user.role == 'buyer':
        return redirect(url_for('admin.users'))
    else:
        return redirect(url_for('admin.pilots'))

@admin.route('/user/assign/<id>', methods=['GET'])
def assign(id):
    try:
        assigned = request.args['assigned']
        flight = Flight.query.filter_by(id=assigned).first()
        flight.pilotid=id
        db.session.commit()
        flash('Vuelo asignado', category='success')
        return redirect('/admin/pilots')
    except:
        pass
    flights = Flight.query.filter_by(pilotid=None).all()
    return render_template('/admin/assign.html', flights=flights)

@admin.route('/customers', methods=['GET'])
def users():
    users = User.query.filter_by(role='buyer').all()
    return render_template('/admin/users.html', users=users)

#flights.html

@admin.route('/pilots', methods=['GET'])
def pilots():
    pilots = User.query.filter_by(role='pilot').all()
    return render_template('/admin/pilots.html', pilots=pilots)

@admin.route('/flights', methods=['GET'])
def flights():
    flights = Flight.query.all()
    return render_template('/admin/flights.html', flights=flights, bookings=flight_bookings, get=getUserFromid, yes=False, fl = get_flightcode)

@admin.route('/flight/add', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        status = request.form.get('status')
        airline = request.form.get('airline')
        fromm = request.form.get('from')
        to = request.form.get('to')
        cost = request.form.get('cost')
        capacity = request.form.get('capacity')
        date = request.form.get('date')
        dept = request.form.get('dept-time')
        arr = request.form.get('arr-time')
        flash('Created Flight', category='success')

        new_flight = Flight(status=status, airline=airline, origin=fromm, dest=to, cost=cost, capacity=capacity, date=date, dept_time=dept, arr_time=arr)
        db.session.add(new_flight)
        db.session.commit()
        return redirect(url_for('admin.flights'))

    return render_template('/admin/add-flight.html')

@admin.route('/flight/edit/<id>', methods=['GET', 'POST'])
def edit_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    if request.method == 'POST':
        status = request.form.get('status')
        airline = request.form.get('airline')
        fromm = request.form.get('from')
        to = request.form.get('to')
        cost = request.form.get('cost')
        capacity = request.form.get('capacity')
        date = request.form.get('date')
        dept = request.form.get('dept-time')
        arr = request.form.get('arr-time')
        flash('Los cambios en su vuelo se han guardado exitosamente', category='success')

        flight = Flight.query.filter_by(id=id).first()
        flight.status = status
        flight.airline=airline
        flight.origin=fromm
        flight.dest=to
        flight.cost=cost
        flight.capacity=capacity
        flight.date=date
        flight.dept_time=dept
        flight.arr_time=arr
        db.session.commit()
        return redirect(url_for('admin.flights'))

    return render_template('/admin/edit-flight.html', flight=flight)

@admin.route('/flight/assign/<id>', methods=['GET'])
def assign_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    try:
        assigned = request.args['assigned']
        flight = Flight.query.filter_by(id=id).first()
        flight.pilotid=assigned
        db.session.commit()
        flash('Vuelo asignado', category='success')
        return redirect('/admin/flights')
    except:
        pass
    pilots = User.query.filter_by(role='pilot').all()
    used_pilots = Flight.query.all()
    for pilot in used_pilots:
        pilot = User.query.filter_by(id=pilot.pilotid).first()
        if pilot in pilots:
            pilots.remove(pilot)
    return render_template('/admin/assign-flight.html', flights=pilots)

@admin.route('/flight/delete/<id>')
def delete_flight(id):
    flight = Flight.query.filter_by(id=id).first()
    flash('Se ha eliminado el vuelo '+get_flightcode(flight), category='success')
    db.session.delete(flight)
    db.session.commit()
    return redirect(url_for('admin.flights'))

@admin.route('/comments', methods=['GET'])
def comments():
    comments = Feedback.query.all()
    return render_template('/admin/comments.html', comments=comments, get=getUserFromid)

@admin.route('/comment/delete/<id>', methods=['GET'])
def delete_comment(id):
    user = Feedback.query.filter_by(id=id).first()
    flash('Se ha borrado el comentario exitosamente '+user.subject, category='success')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.comments'))

@admin.route('/view/<id>')
def view(id):
    flight = Flight.query.filter_by(id=id).first()
    return render_template('/admin/view.html', flight=flight, fl=get_flightcode, get=getUserFromid)
