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


# Required for services which bind to unix socket
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
# All data is storede on LeanCloud
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
            lc_user = leancloud.User()
            lc_user.login(_user.email, _user.password)
        except:
            app.logger.warn(
                'Login failed, email: %s', _user.email, exc_info=True
            )
        else:
            # Credential verified, query user roles
            role_query = leancloud.Query(leancloud.Role)
            role_query.contains_all('users', [lc_user, ])
            roles = [r.get_name() for r in role_query.find()]

            # Login succeeded
            user = User()
            user.email = _user.email
            user.roles = roles
            flask_login.login_user(user)
    next_url = request.args.get('next', url_for('view_service_list'))
    if flask_login.current_user.is_authenticated:
        return redirect(next_url)
    # Render login page for anonymous users
    return render_template('login.html', form=login_form, next=next_url)


@app.route('/logout')
def view_logout():
    flask_login.logout_user()
    return redirect(url_for('view_index'))


@app.route('/dashboard')
@flask_login.login_required
def view_dashboard():
    '''
    Dashboard view, C/R/U/D operations for services.
    Notice: Only users with Admin role can access this view.
    '''
    if 'Admin' not in getattr(flask_login.current_user, 'roles', []):
        return 'You don\'t have the permission to view this page.'
    return 'Under construction'


@app.route('/services', methods=('GET', ))
@flask_login.login_required
def view_service_list():
    service = {
        'title': 'Test service',
        'description': 'Click on the button to visit this service',
        'endpoint': 'test',
        'type': 'http',
        'uri': '127.0.0.1:1234',
    }
    services = [service, service, service, service, service, service, service]
    return render_template('services.html', services=services)


@app.route('/services/<name>')
@flask_login.login_required
def view_service(name):
    # 1. Look up in service registry
    # 2. If no such service, return 404 page
    # 3. Else return service resource
    return 'Service content for {}'.format(name)
    # return requests.get('http://z.cn').content
