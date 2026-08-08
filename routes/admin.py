from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from functools import wraps
from extensions import db
from models import User, TrekStaff, Trek, Booking

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='user', status='active').count()
    total_staff = User.query.join(TrekStaff).filter(User.role == 'staff', TrekStaff.approval == True).count()
    pending_staff = User.query.join(TrekStaff).filter(User.role == 'staff', TrekStaff.approval == False, User.status == 'active').count()
    total_bookings = Booking.query.count()

    return render_template('admin/dashboard.html',
                           total_treks=total_treks,
                           total_users=total_users,
                           total_staff=total_staff,
                           pending_staff=pending_staff,
                           total_bookings=total_bookings)

# Trek Management functions

@admin_bp.route('/treks')
@login_required
@admin_required
def manage_treks():
    search = request.args.get('search', '')
    query = Trek.query
    if search:
        query = query.filter(
            (Trek.name.ilike(f'%{search}%')) |
            (Trek.id == search if search.isdigit() else False)
        )
    treks = query.all()
    return render_template('admin/treks.html', treks=treks, search=search)

@admin_bp.route('/treks/add', methods=['GET','POST'])
@login_required
@admin_required
def add_trek():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        duration = request.form.get('duration')
        difficulty = request.form.get('difficulty')
        available_slots = request.form.get('available_slots')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            
        new_trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=int(duration),
            available_slots=int(available_slots),
            status='Pending',
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(new_trek)
        db.session.commit()
        flash('Trek created successfully !', 'success')
        return redirect(url_for('admin.manage_treks'))

    return render_template('admin/add_trek.html')

@admin_bp.route('/treks/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration = int(request.form.get('duration'))
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')
        trek.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        trek.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()

        if trek.status == 'Completed':
            for booking in trek.bookings:
                if booking.status == 'Booked':
                    booking.status = 'Completed'

        db.session.commit()
        flash('Trek updated successfully !', 'success')
        return redirect(url_for('admin.manage_treks'))

    return render_template('admin/edit_trek.html', trek=trek)

@admin_bp.route('/treks/<int:trek_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    flash('Trek deleted :(', 'info')
    return redirect(url_for('admin.manage_treks'))

# Staff Management Functions

@admin_bp.route('/staff')
@login_required
@admin_required
def manage_staff():
    search = request.args.get('search', '')
    query = User.query.filter_by(role='staff')
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) |
            (User.id == search if search.isdigit() else False)
        )
    staff_list = query.all()
    return render_template('admin/staff.html', staff_list=staff_list, search=search)
@admin_bp.route('/staff/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_staff(user_id):
    user = User.query.get_or_404(user_id)
    if user.staff_profile:
        user.staff_profile.approval = True
        db.session.commit()
        flash(f'{user.name} has been approved :D', 'success')
    return redirect(url_for('admin.manage_staff'))


@admin_bp.route('/staff/<int:user_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_staff(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'blacklisted'
    db.session.commit()
    flash(f'{user.name} has been blacklisted D:', 'warning')
    return redirect(url_for('admin.manage_staff'))


@admin_bp.route('/staff/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_staff(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'active'
    db.session.commit()
    flash(f'{user.name} has been reactivated :D', 'success')
    return redirect(url_for('admin.manage_staff'))

@admin_bp.route('/treks/<int:trek_id>/assign', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_staff(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    approved_staff = User.query.join(TrekStaff).filter(User.role == 'staff', TrekStaff.approval == True, User.status == 'active').all()

    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        trek.assigned_staff_id = int(staff_id)
        if trek.status == 'Pending':
            trek.status = 'Approved'
        db.session.commit()
        flash('Staff assigned to trek.', 'success')
        return redirect(url_for('admin.manage_treks'))

    return render_template('admin/assign_staff.html', trek=trek, approved_staff=approved_staff)

# User Management Functions

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    search = request.args.get('search', '')
    query = User.query.filter_by(role='user')
    if search:
        query = query.filter(User.name.ilike(f'%{search}%'))
    users_list = query.all()
    return render_template('admin/users.html', users_list=users_list, search=search)


@admin_bp.route('/users/<int:user_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'blacklisted'
    db.session.commit()
    flash(f'{user.name} has been blacklisted D:', 'warning')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>/reactivate', methods=['POST'])
@login_required
@admin_required
def reactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'active'
    db.session.commit()
    flash(f'{user.name} has been reactivated :D', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/bookings')
@login_required
@admin_required
def view_bookings():
    search = request.args.get('search', '')
    query = Booking.query.join(Trek).join(User, Booking.user_id == User.id)

    if search:
        query = query.filter(
            (Trek.name.ilike(f'%{search}%')) |
            (User.name.ilike(f'%{search}%')) |
            (Booking.id == search if search.isdigit() else False)
        )

    bookings = query.all()
    return render_template('admin/bookings.html', bookings=bookings, search=search)