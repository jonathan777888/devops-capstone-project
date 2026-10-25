from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman


def create_app():
    app = Flask(__name__)

    CORS(app)

    Talisman(
        app,
        force_https=False,
        content_security_policy=None
    )

    from service.routes import accounts_bp
    app.register_blueprint(accounts_bp)

    return app


app = create_app()
