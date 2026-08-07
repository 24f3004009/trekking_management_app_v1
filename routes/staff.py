from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import Trek, Booking, User

staff_bp = Blueprint('staff', __name__)


def staff_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.role != 'staff':
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@staff_bp.route('/dashboard')
@login_required
@staff_required
def dashboard():
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    return render_template('staff/dashboard.html', assigned_treks=assigned_treks)


@staff_bp.route('/my-treks')
@login_required
@staff_required
def my_treks():
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    return render_template('staff/my_treks.html', assigned_treks=assigned_treks)


@staff_bp.route('/treks/<int:trek_id>/update', methods=['GET', 'POST'])
@login_required
@staff_required
def update_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    # Security check: staff can only update treks assigned to THEM
    if trek.assigned_staff_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')
        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('staff.my_treks'))

    return render_template('staff/update_trek.html', trek=trek)


@staff_bp.route('/treks/<int:trek_id>/participants')
@login_required
@staff_required
def view_participants(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != current_user.id:
        abort(403)

    bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').all()
    return render_template('staff/participants.html', trek=trek, bookings=bookings)