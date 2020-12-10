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
            airline1=airline1, airline2=airline2, descriptor=descriptor, fig=fig, dist=dist)


    return render_template('./content/compare_airline.html', airlines=airlines, descriptors=descriptors, compute_chart=compute_chart)

@bp.route('/airlines/')
def airlines():
    df = db_to_pandas(current_app.config['DATABASE'])
    nb_flights = df[['airline','flight_id']].groupby('airline').count().rename(columns={'flight_id':'number of flights'})
    nb_flights.sort_values('number of flights', ascending=False, inplace=True)

    fig = plt.figure()
    plt.barh(nb_flights.index,nb_flights['number of flights'], color='red', alpha=0.7, label='number of flights')
    ax=plt.gca()
    ax.set_yticks(nb_flights.index)
    ax.set_yticklabels(nb_flights.index)
    plt.legend()
    fig = mpld3.fig_to_html(fig)

    nb_airlines = len(nb_flights)
    tt_flights = nb_flights['number of flights'].sum()

    return render_template('./content/airlines.html', airlines=nb_flights, fig=fig,
        nb_airlines=nb_airlines, nb_flights=tt_flights)

@bp.route('/airline/<airline>/')
def desc_airline(airline):
    df = db_to_pandas(current_app.config['DATABASE'])
    my_airline = df[df['airline']==airline]

    my_airline.drop(columns=['flight_id','flight_start','flight_end','icao','airline'], inplace=True)
    descriptors = my_airline.columns

    figlist=[]
    for descriptor in descriptors:
        fig = plt.figure()
        plt.hist(my_airline[descriptor],color='blue', bins=20, density=True, alpha=0.8, label=descriptor)
        plt.legend()
        figlist.append(mpld3.fig_to_html(fig))
    return render_template('./content/airline.html',airline=airline, figlist=figlist)