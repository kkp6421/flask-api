from flask import Blueprint

task = Blueprint(__name__, 'task')

from . import views

