Airline Classification
======================

In this section, a classification is proposed based on weather and operation flight data. The classification process consists of three major steps:
    + preprocessing of data
    + feature selection
    + aggregation of data on airline level
    + proposition of a clustering affiliation for each airline

Preprocessing
^^^^^^^^^^^^^^^^^^^^^
The descriptor database obtained from the precedent step, descriptors computing, is imported.

Then preprocessing has following steps:
    + eliminate the effects of abnormal values by deleting maximums and minimums as descriptors
    + delete useless columns identified by business expert
    + encode airline names to create numerical label
    + keep only the airlines with a minimal number of flights (100 by default)
    + create three dataframes: one with whole dataset, one with only weather data, and one with only operation data

Feature Selection
^^^^^^^^^^^^^^^^^^^^^
As some columns are highly correlated, for instance




Documentation of functions in **pretreatment.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: data_preparation
    :members:

Documentation of functions in **cluster.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: cluster
    :members: