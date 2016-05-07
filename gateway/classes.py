# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import flask.ext.login as flask_login
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired


class Object(dict):
    '''Empty attribute holder'''
    def __init__(self, **kwargs):
        super(Object, self).__init__()
        self.update(kwargs)

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]


class User(flask_login.UserMixin):
    '''User object'''
    @property
    def id(self):
        return self.get_id()

    def get_id(self):
        return getattr(self, 'email', 'Anonymous')


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
