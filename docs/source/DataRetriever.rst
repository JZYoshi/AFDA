Retrieving rough data
=====================

Retrieving metar data
=====================
Metar data can be collected every one hour calling the script
**metar_retriever.py** each hour. This script downloads a metar report which name is
the unix time rounded to the hour where the download has been made. To call this script
every one hour, a possibility is to create a crontab wich call this script every hour.
The source of these data is `metar <https://www.aviationweather.gov/>`_.

.. automodule:: metar_retriever
    :members: