from flask import Blueprint

tag = Blueprint(__name__, 'tag')

from . import views
