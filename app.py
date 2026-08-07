from flask import Flask,render_template
from werkzeug.security import generate_password_hash
from config import Config
from extensions import db, login_manager
from models import *
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  #if not loged in
    with app.app_context():
        db.create_all()

        admin_exists = User.query.filter_by(role='admin').first()
        if not admin_exists:
            admin = User(
                name='Admin',
                email='admin@treknfun.com',
                password_hash=generate_password_hash('adminmad1'),
                role='admin',
                status='active'
            )
            db.session.add(admin)
            db.session.commit()
            print('Default admin created: admin@treknfun.com / adminmad1')

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_perfix='/admin')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app

app = create_app()

@app.route("/")
def hello_world():
    return "<p>oi mate, why r u here !!</p>"

if __name__ == '__main__':
    app.run(debug=True)