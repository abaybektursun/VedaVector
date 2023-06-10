#!/usr/bin/env python
from flask import Flask, url_for, render_template, jsonify
import jinja2.exceptions

from flask import request, redirect, session
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os

app = Flask(__name__)

client_secrets_file = "/Users/abaybektursun/projects/VedaVector/client_secret_68746824277-t2021ivtkphusqcar5gv525bq0idr6jm.apps.googleusercontent.com.json"
# Initialize the flow using the client secrets file
flow = Flow.from_client_secrets_file(
    client_secrets_file,
    scopes=["https://www.googleapis.com/auth/drive"],
    redirect_uri="http://127.0.0.1:5001/oauth2callback"
)

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url(
        "https://accounts.google.com/o/oauth2/auth",
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)
    if not flow.credentials:
        return "Failed to get tokens."
    # Save credentials to the session.
    credentials = {
        'token': flow.credentials.token,
        'refresh_token': flow.credentials.refresh_token,
        'token_uri': flow.credentials.token_uri,
        'client_id': flow.credentials.client_id,
        'client_secret': flow.credentials.client_secret,
        'scopes': flow.credentials.scopes
    }
    session['credentials'] = credentials
    print(session['credentials'])
    return "Logged in."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<pagename>')
def admin(pagename):
    return render_template(pagename+'.html')

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/get_files')
def list_drive_files(user_token):
    creds = Credentials.from_authorized_user_info(user_token)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list().execute()
    items = results.get('files', [])
    return items  # this is a list of files

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    print(files)

    this_script_path = os.path.dirname(os.path.realpath(__file__))
    
    for file in files:
        file.save(this_script_path + '/user_data/' + file.filename)

    return 'Files uploaded successfully.'


@app.route('/file-list')
def file_list():
    file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user_data')
    print("file-list called")
    files = os.listdir(file_dir)
    print("Sending files: ", files)
    return jsonify(files)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
