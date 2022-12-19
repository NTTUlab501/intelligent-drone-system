# -*- coding:utf-8 -*-

from flask import Blueprint

user_access = Blueprint('user_access', __name__, template_folder = 'templates', static_folder='static', url_prefix = '/user_access')

robots = {
    'UAV': []
}

from . import views, events
