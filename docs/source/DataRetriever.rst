Retrieving rough data
=====================

Retrieving metar data
^^^^^^^^^^^^^^^^^^^^^
Metar data can be collected every one hour calling the script
**metar_retriever.py** each hour. This script downloads a metar report which name is
the unix time rounded to the hour where the download has been made. To call this script
every one hour, a possibility is to create a crontab wich call this script every hour.
The source of these data is `metar <https://www.aviationweather.gov/>`_.


Documentation of functions in **metar_retriever.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: metar_retriever
    :members:

---------------------------------------------------------

Retrieving flight data
^^^^^^^^^^^^^^^^^^^^^^
There are two ways to collect flight data from `OpenSky Network <https://opensky-network.org/>`_.

* Download the data archive from `<https://opensky-network.org/datasets/states/>`_. **Note**: Only the access to Monday
  data is granted. To start retrieving data by this approach, please refer to *data_fetching.py*. A useful python script 
  for splitting the data into groups according to their flight numbers is provided as well, please refer to *data_preparation.py*
  and *main.py* for details.

    .. code-block:: bash

      python data_fetching.py

    .. code-block:: bash

      python main.py
    
* Collect live flight data by calling every 10 seconds the `OpenSky Network API <https://opensky-network.org/apidoc/>`_.
  Please refer to *daily_flight_data_broker.py* for details. This script not only collects live data, but also
  carries out a filtering (pre-processing) to the data, such as keeping the flights that are operated with the targeted aircraft series (ex. A320),
  grouping the data by their flight numbers etc.

    .. code-block:: bash

      python daily_flight_data_broker.py

**Note**: before starting to retrieve data, please remember to download and to put `aircraftDatabase.csv <https://opensky-network.org/datasets/metadata/>`_ in **../data/** 

Documentation of functions in **data_fetching.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: data_fetching
    :members:

Documentation of functions in **data_preparation.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: data_preparation
    :members:

Documentation of functions in **daily_flight_data_broker.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: daily_flight_data_broker
    :members: