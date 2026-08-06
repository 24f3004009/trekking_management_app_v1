from flask import Flask,render_template
from config import Config
from extensions import db, login_manager
from models import *
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  #if not loged in
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

app = create_app()

@app.route("/")
def hello_world():
    return "<p>oi mate, why r u here !!</p>"

if __name__ == '__main__':
    app.run(debug=True)