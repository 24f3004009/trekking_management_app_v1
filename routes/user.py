from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import Trek, Booking, User

user_bp = Blueprint('user', __name__)


def user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.role != 'user':
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@user_bp.route('/dashboard')
@login_required
@user_required
def dashboard():
    open_treks_count = Trek.query.filter_by(status='Open').count()
    my_bookings_count = Booking.query.filter_by(user_id=current_user.id, status='Booked').count()
    return render_template('user/dashboard.html',
                            open_treks_count=open_treks_count,
                            my_bookings_count=my_bookings_count)


@user_bp.route('/treks')
@login_required
@user_required
def show_treks():
    difficulty = request.args.get('difficulty', '')
    location = request.args.get('location', '')

    query = Trek.query.filter_by(status='Open')

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))

    treks = query.all()
    return render_template('user/show_treks.html', treks=treks, difficulty=difficulty, location=location)


@user_bp.route('/treks/<int:trek_id>/book', methods=['POST'])
@login_required
@user_required
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if trek.status != 'Open':
        flash('This trek is not open for booking.', 'danger')
        return redirect(url_for('user.show_treks'))

    if trek.available_slots <= 0:
        flash('Sorry, this trek is fully booked.', 'danger')
        return redirect(url_for('user.show_treks'))

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id, trek_id=trek.id, status='Booked'
    ).first()
    if existing_booking:
        flash('You have already booked this trek.', 'warning')
        return redirect(url_for('user.show_treks'))

    new_booking = Booking(user_id=current_user.id, trek_id=trek.id, status='Booked')
    trek.available_slots -= 1
    db.session.add(new_booking)
    db.session.commit()

    flash(f'Successfully booked {trek.name}!', 'success')
    return redirect(url_for('user.my_bookings'))


@user_bp.route('/bookings')
@login_required
@user_required
def my_bookings():
    search = request.args.get('search', '')
    query = Booking.query.filter_by(user_id=current_user.id).join(Trek)

    if search:
        query = query.filter(
            (Trek.name.ilike(f'%{search}%')) |
            (Booking.status.ilike(f'%{search}%'))
        )

    bookings = query.all()
    return render_template('user/bookings.html', bookings=bookings, search=search)


@user_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
@user_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        abort(403)

    if booking.status == 'Booked':
        booking.status = 'Cancelled'
        booking.trek.available_slots += 1
        db.session.commit()
        flash('Booking cancelled.', 'info')

    return redirect(url_for('user.my_bookings'))


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@user_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('user.edit_profile'))

    return render_template('user/profile.html')