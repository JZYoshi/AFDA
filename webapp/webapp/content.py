import functools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from scipy.stats import gaussian_kde

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
            fig = plt.figure()

            plt.hist(df[df['airline']==airline1][descriptor],color='blue', bins=20, density=True, alpha=0.5, label=airline1)
            plt.hist(df[df['airline']==airline2][descriptor],color='red', bins=20, density=True, alpha=0.5, label=airline2)
            
            kde1=gaussian_kde(df[df['airline']==airline1][descriptor])
            kde2=gaussian_kde(df[df['airline']==airline2][descriptor])
            
            borne_inf, borne_sup=(min(df[descriptor]),max(df[descriptor]))
            x = np.linspace(borne_inf,borne_sup,200)
            
            plt.plot(x, kde1(x), 'b--', label='kernel estimation')
            plt.plot(x, kde2(x), 'r--', label='kernel estimation')
            
            dist = np.linalg.norm(kde1(x)-kde2(x))**2/(np.linalg.norm(kde1(x))+np.linalg.norm(kde2(x)))**2

            plt.xlabel(descriptor)
            plt.legend()
            fig = mpld3.fig_to_html(fig)
            
            return render_template('./content/compare_airline.html', 
            airlines=airlines, descriptors=descriptors, compute_chart=compute_chart,
            airline1=airline1, airline2=airline2, descriptor=descriptor, fig=fig)


    return render_template('./content/compare_airline.html', airlines=airlines, descriptors=descriptors, compute_chart=compute_chart)