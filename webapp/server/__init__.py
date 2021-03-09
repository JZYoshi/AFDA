from flask import Flask, render_template, current_app, request
import os
from flask.json import jsonify
import numpy as np
from scipy.stats import gaussian_kde, entropy
from . import db

def create_app(test_config=None):
    # create and configure the app
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

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/generalinfo', methods=['GET'])
    def general_info():
        df = db.db_to_pandas(current_app.config['DATABASE'])
        nb_flights = df[['airline','flight_id']].groupby('airline').count().rename(columns={'flight_id':'number of flights'})
        nb_flights.sort_values('number of flights', ascending=False, inplace=True)

        fig_data = nb_flights.to_dict('list')

        nb_airlines = len(nb_flights)
        tt_flights = int(nb_flights['number of flights'].sum())

        return jsonify({
            'nb_airlines': nb_airlines,
            'tt_flights': tt_flights,
            'fig_data': fig_data
        })

    @app.route('/flightsnumbers', methods=['GET'])
    def get_flights_numbers():
        df = db.db_to_pandas(current_app.config['DATABASE'])
        nb_flights = df[['airline','flight_id']].groupby('airline').count().rename(columns={'flight_id':'number of flights'})
        nb_flights.sort_values(by='number of flights', ascending=False, inplace=True)
        nb_flights.info()
        nb_flight_dict = { 'airlines': nb_flights.index.tolist(), 'flight_number': nb_flights['number of flights'].tolist() }
        return jsonify(nb_flight_dict)

    @app.route('/airlinestat', methods=['POST'])
    def get_airline():
        post_data = request.get_json()
        airline = post_data.get('airline')
        df = db.db_to_pandas(current_app.config['DATABASE'])
        my_airline = df[df['airline']==airline]

        my_airline.drop(columns=['flight_id','icao','airline', 'icao_airline'], inplace=True)
        descriptors = my_airline.columns

        figlist=[]
        for descriptor in descriptors:
            figlist.append({ 'label': descriptor, 'values': my_airline[descriptor].dropna().tolist() })
        return jsonify(figlist) 

    @app.route('/allairlines', methods=['GET', 'POST'])
    def get_all_airlines():
        df = db.db_to_pandas(current_app.config['DATABASE'])
        airlines = []
        if (request.method == 'GET'):
            airlines = list(set(df[df['airline'].notnull()]['airline'].tolist()))
        else:
            threshold = request.get_json().get('threshold')
            s = df['airline'].value_counts()
            s = s[s >= threshold]
            airlines = s.index.tolist()
        return jsonify({
            'airlines': airlines
        })

    @app.route('/descriptors', methods=['GET'])
    def get_all_descriptors():
        df = db.db_to_pandas(current_app.config['DATABASE'])
        descriptors = list(df.drop(columns=['flight_id','icao','airline', 'icao_airline']).columns)
        return jsonify({
            'descriptors': descriptors
        })

    @app.route('/compareairlines', methods=['POST'])
    def get_airlines_compare_res():
        df = db.db_to_pandas(current_app.config['DATABASE'])
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        post_data = request.get_json()
        airlines = post_data.get('airlines')
        descriptors = post_data.get('descriptors')
        figlist = []
        for descriptor in descriptors:
            x_min = min(df[descriptor])
            x_max = max(df[descriptor])
            x = np.linspace(x_min,x_max, 100)
            airline_stat_list = []
            kde_values_list = []
            for airline in airlines:
                values = df[df['airline']==airline][descriptor].dropna()
                kde = gaussian_kde(values)
                kde_values = kde(x)
                airline_stat_list.append({
                    'airline': airline,
                    'descriptor_values': values.tolist(),
                    'kde_values': list(kde_values),
                    'x_kde': list(x) 
                })
                kde_values_list.append(kde_values)
            step = x[1] - x[0]
            n = len(airlines)
            mat_dist = np.zeros((n,n))
            for i in range(n):
                for j in range(n):
                    mat_dist[i, j] = step*entropy(pk=kde_values_list[i], qk=kde_values_list[j])
            mat_dist = np.where(~np.isfinite(mat_dist), None, mat_dist) 
            figlist.append({
                'descriptor': descriptor,
                'airlines': airline_stat_list,
                'kde_entropy': mat_dist.tolist()
            })
        return jsonify(figlist)

    return app