import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
google_bp = make_google_blueprint(scope=["youtube"])
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    email=resp.json()
    print(email)
    request = email.subscriptions().list(
        part="snippet",
        forChannelId="UCIp7tRBZx3UVC2tIVFx1xyw",
        mine=True
    )
    response = request.execute()
    results = response['pageInfo']['totalResults']
    if results != 0:
        return 'You are subscribed. Thank you!'
    else:
        return 'You are not subscribed yet.'
    #return "You are on Google {email} ".format(email=resp.json())
