## There are two ways to get flight data

### Data archive
We can simply download the data archive available at https://opensky-network.org/datasets/states/
1. Run *data_fetching.py* to download files
2. Run *main.py* to extract files

### Live API
We can also retrieve flight data by calling the API offered by Opensky Network every 10 seconds
1. Run *daily_flight_data_broker.py* to collect data on live
**P.S.** this script not only calls the API to collect data, but also applies a first filtering to the data on the fly 