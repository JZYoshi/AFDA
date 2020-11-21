import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.db import get_db

bp = Blueprint('blueprint1', __name__, url_prefix='/blueprint1')

@bp.route("/index/")
def index():
    l=['column1','column2','column3']
    ll = [1,2,3]
    return render_template('blueprint1/index.html', l=l,ll=ll)