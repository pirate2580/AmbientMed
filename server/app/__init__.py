from flask import Flask, redirect, render_template, session, url_for
from app.controllers.appointment_controller import appointment_bp
from app.controllers.user_controller import login_bp
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import os
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import json
from flask_cors import CORS

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    # app.secret_key = os.environ.get('APP_SECRET_KEY')
    # Register Blueprints
    app.register_blueprint(appointment_bp, url_prefix='/appointments')
    app.register_blueprint(login_bp, url_prefix='/auth')
    return app
    # oauth = OAuth(app)

    # oauth.register(
    #     "auth0",
    #     client_id=os.environ.get("AUTH0_CLIENT_ID"),
    #     client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    #     client_kwargs={
    #         "scope": "openid profile email",
    #     },
    #     server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    # )

    # @app.route("/login")
    # def login():
    #     return oauth.auth0.authorize_redirect(
    #         redirect_uri=url_for("callback", _external=True)
    #     )
    
    # @app.route("/callback", methods=["GET", "POST"])
    # def callback():
    #     token = oauth.auth0.authorize_access_token()
    #     session["user"] = token
    #     return redirect("/")
    
    # @app.route("/logout")
    # def logout():
    #     session.clear()
    #     return redirect(
    #         "https://" + os.environ.get("AUTH0_DOMAIN")
    #         + "/v2/logout?"
    #         + urlencode(
    #             {
    #                 "returnTo": url_for("home", _external=True),
    #                 "client_id": os.environ.get("AUTH0_CLIENT_ID"),
    #             },
    #             quote_via=quote_plus,
    #         )
    #     )
    
    # @app.route("/")
    # def home():
    #     return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
    
    # return app