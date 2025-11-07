from flask import Flask, request, jsonify, redirect
from flask_smorest import Api
from config import Config, TestingConfig
from extensions import db, jwt
from ressources.auth.routes import auth
from ressources.firewall.routes import firewall
from ressources.policy.routes import policy
from ressources.rules.routes import rule
from scripts.seed import seed_database


def create_app(config_name="default"):
    app = Flask(__name__)

    if config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    @app.route("/")
    def root():
        return redirect("/docs")

    @app.cli.command('populate-db')
    def seed_db_command():
        seed_database(app)

    api.spec.components.security_scheme(
        "BearerAuth",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    )

    api.spec.options["security"] = [{"BearerAuth": []}]

    api.register_blueprint(auth)
    api.register_blueprint(firewall)
    api.register_blueprint(policy)
    api.register_blueprint(rule)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8080)


