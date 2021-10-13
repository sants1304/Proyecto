from datetime import datetime, date
from .admin import flight_bookings, get_flightcode, getUserFromid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import *
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
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
            return redirect(url_for('views.home'))
        return render_template('dashboard.html', user=current_user)
    else:
        return render_template('home.html', user=None)

@views.route('/about', methods=['GET'])
def about():
    if current_user.is_authenticated:
        return render_template('about.html', user=current_user)
    else:
        return render_template('about.html', user=None)

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        subject = request.form.get('subject')
        comment = request.form.get('comment')
        new = Feedback(userid=current_user.id, subject=subject, comment=comment)
        db.session.add(new)
        db.session.commit()
        flash('Comment sent the admin. Thankyou for the feedback...', category='success')
        return redirect(url_for('views.home'))

    return render_template('contact.html', user=current_user)

@views.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    try:
        origin = request.args['origin']
        dest = request.args['dest']
        date = request.args['date']
        flights = Flight.query.filter_by(origin=origin, dest=dest, date=date).all()
        return render_template('reserve.html', flights=flights, user=current_user, flightbk=flight_bookings)
    except:
        return render_template('reservation.html', user=current_user)

@views.route('/your-flights', methods=['GET', 'POST'])
@login_required
def your_flights():
    if current_user.role == 'pilot':
        flights = Flight.query.filter_by(pilotid=current_user.id).all()
    else:
        bookings = Booking.query.filter_by(userid=current_user.id).all()
        flights = []
        for booking in bookings:
            flight = Flight.query.filter_by(id=booking.flightid).first()
            flights.append(flight)
    return render_template('/admin/flights.html', user=current_user, flights=flights, yes=True, fl=get_flightcode)

@views.route('/buy/<id>', methods=['GET'])
def buy(id):
    flight = Flight.query.filter_by(id=id).first()
    try:
       cap = request.args['capacity']
       new_booking = Booking(userid=current_user.id, date=flight.date, people=cap, flightid=flight.id)
       db.session.add(new_booking)
       db.session.commit()
       return redirect('/your-flights')
    except:
        return render_template('buy.html', user=current_user, flight=flight, fl=get_flightcode, get=getUserFromid)