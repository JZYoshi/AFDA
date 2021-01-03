from flask import Flask, render_template, current_app, request
import os
from flask.json import jsonify
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from scipy.stats import gaussian_kde
from . import db

app = Flask(__name__, template_folder="../vue/client/dist", static_folder="../vue/client/dist/static")

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'descriptors.db'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


# -------------------ROUTE CONFIG-------------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generalinfo', methods=['GET'])
def general_info():
    df = db.db_to_pandas(current_app.config['DATABASE'])
    nb_flights = df[['airline','flight_id']].groupby('airline').count().rename(columns={'flight_id':'number of flights'})
    nb_flights.sort_values('number of flights', ascending=False, inplace=True)

    fig = plt.figure(figsize=(4, 3), dpi=200)
    plt.barh(nb_flights.index,nb_flights['number of flights'], color='red', alpha=0.7, label='number of flights')
    ax=plt.gca()
    ax.set_yticks(nb_flights.index)
    ax.set_yticklabels(nb_flights.index)
    plt.legend()
    fig = mpld3.fig_to_dict(fig)

    nb_airlines = len(nb_flights)
    tt_flights = int(nb_flights['number of flights'].sum())

    return jsonify({
        'nb_airlines': nb_airlines,
        'tt_flights': tt_flights,
        'fig_raw': fig
    })

@app.route('/flightsnumbers', methods=['GET'])
def get_flights_numbers():
    df = db.db_to_pandas(current_app.config['DATABASE'])
    nb_flights = df[['airline','flight_id']].groupby('airline').count().rename(columns={'flight_id':'number of flights'})
    nb_flight_list = list(nb_flights.iterrows())
    nb_flight_dict = { airline: int(N[0]) for airline, N in nb_flight_list }
    return jsonify(nb_flight_dict)

@app.route('/airlinestat', methods=['POST'])
def get_airline():
    post_data = request.get_json()
    airline = post_data.get('airline')
    df = db.db_to_pandas(current_app.config['DATABASE'])
    my_airline = df[df['airline']==airline]

    my_airline.drop(columns=['flight_id','flight_start','flight_end','icao','airline'], inplace=True)
    descriptors = my_airline.columns

    figlist=[]
    for descriptor in descriptors:
        fig = plt.figure(figsize=(5, 4), dpi=80)
        plt.hist(my_airline[descriptor],color='blue', bins=20, density=True, alpha=0.8, label=descriptor)
        plt.legend()
        figlist.append(mpld3.fig_to_dict(fig))
    
    return jsonify({
        'fig_raw_list': figlist
    })

@app.route('/allairlines', methods=['GET'])
def get_all_airlines():
    df = db.db_to_pandas(current_app.config['DATABASE'])
    airlines = list(set(df[df['airline'].notnull()]['airline'].tolist()))
    return jsonify({
        'airlines': airlines
    })

@app.route('/descriptors', methods=['GET'])
def get_all_descriptors():
    df = db.db_to_pandas(current_app.config['DATABASE'])
    descriptors = list(df.columns)
    return jsonify({
        'descriptors': descriptors
    })

@app.route('/compareairlines', methods=['POST'])
def get_airlines_compare_res():
    df = db.db_to_pandas(current_app.config['DATABASE'])
    post_data = request.get_json()
    airline1 = post_data.get('airline_1')
    airline2 = post_data.get('airline_2')
    descriptors = post_data.get('descriptors')
    figlist = []
    for descriptor in descriptors:
        fig = plt.figure(figsize=(4, 3), dpi=160)
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
        figlist.append(mpld3.fig_to_dict(fig))

    return jsonify({
        'fig_raw_list': figlist
    })
