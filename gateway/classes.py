# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import flask.ext.login as flask_login
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired


class Object(dict):
    '''Empty attribute holder'''

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None


class User(flask_login.UserMixin):
    '''User object'''

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._roles = []
        self._lc_session_token = None

    @property
    def id(self):
        return self.get_id()

    def get_id(self):
        return getattr(self, 'email', 'Anonymous')

    @property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, values):
        self._roles = values

    def get_lc_session_token(self):
        return self._lc_session_token

    def link_lc_user(self, user):
        self._lc_session_token = user.get_session_token()


class LoginForm(Form):
    '''Login form'''
    email = StringField(
        'email',
        validators=[DataRequired(), Email(), ],
        render_kw={
            'class': 'form-control login-field',
            'placeholder': 'Email',
            'required': '',
        }
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), ],
        render_kw={
            'class': 'form-control login-field',
            'placeholder': 'Password',
            'required': '',
        }
    )
    remember = BooleanField('remember')
