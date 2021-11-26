from flask import Flask, redirect, request
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from oauthlib.oauth2 import WebApplicationClient
import pyautogui
import requests
import json
import os

# Your ngrok url, obtained after running "ngrok http 5000"
URL = "https://83dc-86-106-238-57.ngrok.io"

# Simple Login Authentication
CLIENT_ID = "cs-app-xukyzignqy"
CLIENT_SECRET = "jdoiamnndvoqsthptdgxeovepqrxrvwbxntmtwyl"

AUTHORIZATION_BASE_URL = "https://app.simplelogin.io/oauth2/authorize"
TOKEN_URL = "https://app.simplelogin.io/oauth2/token"
USERINFO_URL = "https://app.simplelogin.io/oauth2/userinfo"

# Facebook authorization
FB_CLIENT_ID = "1052898728883201"
FB_CLIENT_SECRET = "b76c07610b09eca336b3945d30875881"

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

FB_SCOPE = ["email"]

# Gmail authorization
GOOGLE_CLIENT_ID = '455493103678-npfjdrf7bk5tjmhtrd45644dcbce4131.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)


@app.route("/")
def index():
    if os.path.exists('profile_data.json'):
        return """
        <h2> You are already signed in </h2> <br>
        <a href = '/close'> Close </a> <br>
        <a href = '/sign_out'> Sign out </a>
        """
    else:
        return """

        <a href = '/simple-login'>Login with Simple Login</a> <br>
        <a href="/fb-login">Login with Facebook</a> <br>
        <a class="button" href="/gmail-login">Login with Google</a> <br>
        <a href = '/close'> Close </a> <br>
        """


@app.route("/simple-login")
def login():
    simple_login = requests_oauthlib.OAuth2Session(
        CLIENT_ID, redirect_uri="http://localhost:5000/simple-callback"
    )
    authorization_url, _ = simple_login.authorization_url(AUTHORIZATION_BASE_URL)

    return redirect(authorization_url)


@app.route("/simple-callback")
def callback():
    simple_login = requests_oauthlib.OAuth2Session(CLIENT_ID)
    simple_login.fetch_token(
        TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url
    )

    user_info = simple_login.get(USERINFO_URL).json()
    return f"""
    User information: <br>
    Name: {user_info["name"]} <br>
    Email: {user_info["email"]} <br>
    <a href="/">Home</a>
    """


@app.route("/fb-login")
def fb_login():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
    )
    authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)

    return redirect(authorization_url)


@app.route("/fb-callback")
def fb_callback():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/fb-callback"
    )

    # we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=request.url,
    )

    # Fetch a protected resource, i.e. user profile, via Graph API
    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    email = facebook_user_data["email"]
    name = facebook_user_data["name"]
    picture_url = facebook_user_data.get("picture", {}).get("data", {}).get("url")

    return f"""
    User information: <br>
    Name: {name} <br>
    Email: {email} <br>
    Avatar <img src="{picture_url}"> <br>
    <a href="/">Home</a>
    """


@app.route("/gmail-login")
def gmail_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/gmail-callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/gmail-login/gmail-callback")
def gmail_callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    output = {'name': users_name, 'email': users_email, 'picture': picture}

    with open('profile_data.json', 'w') as f:
        json.dump(output, f)

    # return  """<a href='/'> Back </a>"""

    return f"""
    User information: <br>
    Name: {users_name} <br>
    Email: {users_email} <br>
    Avatar <img src = "{picture}"> <br>
    <a href ="/">Close</a>
    """


def shutdown_server():
    func = request.environ.get('https://127.0.0.1:5000')
    if func is None:
        raise RuntimeError('Not running with the local server')
    func()


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/sign_out")
def sign_out():
    os.remove('profile_data.json')
    return f"""
        <h2> You are signed out! </h2> <br>
        <a href = '/'> Back </a>
        """


@app.route("/close")
def close():
    pyautogui.hotkey('ctrl', 'w')


if __name__ == '__main__':
    app.run(debug=True)
