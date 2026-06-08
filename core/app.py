from flask import Flask
from core.models import db
import os
from dotenv import load_dotenv
from core.extensions import mail, admin

load_dotenv()
def create_app():
    from core.admin.views import BaseSecureView
    from core.routes import core
    # 
    app = Flask(__name__)

    app.static_folder = 'static'
    app.static_path = '/static'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') in ['True', 'true', '1', 1]
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') in ['True', 'true', '1', 1]
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'contact@nmemusic.co.uk')
    app.config['INBOUND_MAIL'] = os.environ.get('INBOUND_MAIL')
    app.config['MAIL_DEBUG'] = True
    app_env = os.environ.get('FLASK_ENV')
    if app_env is None:
        app_env = 'production'
    app.config['FLASK_ENV'] = app_env
    mail.init_app(app)
    admin.init_app(app)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


    UPLOAD_PATH = os.path.join(BASE_DIR, 'media')

    app.config['UPLOAD_PATH'] = UPLOAD_PATH
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(PARENT_DIR, 'project.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    with app.app_context():
        from core.models.media import Media
        from core.models.user import User



        admin.add_view(BaseSecureView(Media, db.session))
        admin.add_view(BaseSecureView(User, db.session))
    app.register_blueprint(core)
    return app

if __name__ == '__main__':
    # Setting debug=True activates the auto-reloader
    app = create_app()
    app.run(debug=app.config['FLASK_ENV'] == 'development')