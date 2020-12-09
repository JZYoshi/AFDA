import functools
import pandas as pd

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.db import get_db, db_to_pandas

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route("/all_flights/")
def all_flights():
    db = get_db()
    flights = db.execute("SELECT * FROM general_info").fetchall()
    db.close()
    return render_template('content/index.html', flights=flights)

@bp.route('/gen_stats/')
def gen_stats():
    db = get_db()
    airlines = db.execute("SELECT airline FROM general_info WHERE airline NOT NULL GROUP BY airline").fetchall()
    nb_airlines = len(airlines)
    nb_flights = db.execute("SELECT COUNT(flight_id) AS n FROM general_info").fetchone()['n']
    
    durations = pd.read_sql_query("SELECT flight_duration FROM general_info", db)
    intervals = pd.cut(durations['flight_duration'],100)
    durations = intervals.groupby(intervals).count()
    durations.index = [i.mid for i in durations.index]

    db.close()
    return render_template('content/gen_stats.html', 
        airlines=airlines,
        nb_airlines=nb_airlines,
        nb_flights=nb_flights,
        durations=durations,
        
        )

@bp.route('/compare_airline/', methods=['GET','POST'])
def compare_airline():
    db = get_db()
    airlines = db.execute("SELECT airline FROM general_info WHERE airline NOT NULL GROUP BY airline").fetchall()
    df = db_to_pandas(current_app.config['DATABASE'])
    descriptors = df.columns
    compute_chart=False
    if request.method == 'POST':
        airline1 = request.form.get('airline1')
        airline2 = request.form.get('airline2')
        descriptor = request.form.get('descriptor')

        if not airline1:
            error = 'enter airline 1'
        elif not airline2:
            error = 'enter airline 2'
        elif not descriptor:
            error = 'enter a descriptor'
        else:
            compute_chart = True
            intervals = pd.cut(df[descriptor],50)
            df['interval'] = [inter.mid for inter in intervals]
            df = df[[descriptor,'interval','airline']].groupby(by=['interval','airline']).count()
            df = df.unstack(fill_value=0).stack()
            data1 = df.xs(airline1, level='airline')[descriptor]
            data1 = data1/sum(data1)
            data2 = df.xs(airline2, level='airline')[descriptor]
            data2 = data2/sum(data2)
            index = map(int, data1.index)

            return render_template('./content/compare_airline.html', 
                    airlines=airlines, descriptors=descriptors, compute_chart=compute_chart, data1 = data1, data2=data2,index=index, xlabel=descriptor, title=descriptor, airline1=airline1, airline2=airline2)

    return render_template('./content/compare_airline.html', airlines=airlines, descriptors=descriptors, compute_chart=compute_chart)