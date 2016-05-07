# -*- coding: utf-8 -*-
from __future__ import print_function, print_function
import os

import requests_unixsocket
import requests
from flask import (
    Flask, request, render_template, redirect, url_for,
)
import flask.ext.login as flask_login
import leancloud

from .classes import Object, User, LoginForm


requests_unixsocket.monkeypatch()
app = Flask(__name__)
DEV_SECRET = 'dev'
app.secret_key = os.environ.get('GATEWAY_FLASK_SECRET', DEV_SECRET)
if app.secret_key == DEV_SECRET:
    app.debug = True
    app.logger.warn(
        'Warning! You\'re running in DEV mode, user operations disabled!\n'
        'Set the GATEWAY_FLASK_SECRET env variable to disable this warning!'
    )
leancloud.init(
    os.environ['GATEWAY_LEANCLOUD_APP_ID'],
    os.environ['GATEWAY_LEANCLOUD_APP_KEY']
)
login_manager = flask_login.LoginManager()
login_manager.login_view = 'view_login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    if email is not None:
        user = User()
        user.email = email
        return user
    return


@app.route('/')
def view_index():
    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST', ))
def view_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        _user = Object()
        login_form.populate_obj(_user)
        # Verify login credentials
        try:
            leancloud.User().login(_user.email, _user.password)
        except:
            app.logger.warn(
                'Login failed, email: %s', _user.email, exc_info=True
            )
        else:
            user = User()
            user.email = _user.email
            flask_login.login_user(user)
    next_url = request.args.get('next', url_for('view_service_list'))
    if flask_login.current_user.is_authenticated:
        return redirect(next_url)
    # Render login page
    return render_template('login.html', form=login_form, next=next_url)


@app.route('/logout')
def view_logout():
    flask_login.logout_user()
    return redirect(url_for('view_index'))


@app.route('/services', methods=('GET', ))
@flask_login.login_required
def view_service_list():
    service = {
        'title': 'Test service',
        'description': 'Click on the button to visi this service',
        'endpoint': 'test',
    }
    services = [service, service, service, service, service, service, service]
    return render_template('services.html', services=services)


@app.route('/services/<name>')
@flask_login.login_required
def view_service(name):
    # 1. Verify authentication
    # 2. Look up in service registry
    # 3. If no such service, return 404 page
    # 4. Else return service resource
    return 'Service content for {}'.format(name)
    # return requests.get('http://z.cn').content
