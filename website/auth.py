from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import User, Comparison, UserHistory, db
from flask_login import login_user, logout_user, login_required, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests, os, json
from .views import view

auth = Blueprint('auth', __name__)


    #### STANDARD LOGIN ####
@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('view.home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@auth.route('/signup', methods=["POST"])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = email.split('@')[0]

    user = User.query.filter_by(email=email).first()
    if not user:
        if password == confirm_password:
            new_user = User(email=email, name=name)
            new_user.set_password(password)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect('/')
            except Exception as e:
                db.session.rollback()
                print(f"Signup error: {e}")  # shows in Render logs
                return render_template('login.html', error=f'Error: {str(e)}')
        else:
            return render_template('login.html', error='Passwords do not match')
    else:
        return render_template('login.html', error='Email already registered')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.home'))

    
    #### GOOGLE AUTHENTICATION ####
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

#Client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@auth.route('/login/google')
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        return "Authentication service is currently unavailable. Please try again later.", 503
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth.route('/login/google/callback')
def callback():
    # Get authorization code Google sent back 
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        return "Authentication service is currently unavailable. Please try again later.", 503
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Find and hit the URL from Google that gives the user's profile information, including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    # Make sure their email is verified and if yes, retrieve information
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        pfp = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    #If user email already exists it skips creating a new one 
    user = User.query.filter_by(email=users_email).first() 
    
    if not user:
        user = User(
            email=users_email, 
            name=users_name,
            pfp=pfp,
            auth_provider='Google'
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('view.home')) 

@auth.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    current_user.remove()
    db.session.commit()
    return redirect(url_for("view.home"))