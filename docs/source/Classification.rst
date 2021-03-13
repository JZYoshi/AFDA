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
As some columns are highly correlated which may have a negative impact on the results, we carry out a feature selection process.
Feature selection can be done by principal component analysis or by tree-based models using scores distributed for each feature.
In order to keep a good explicability of the results, a tree-based model, random forest, is used to conduct feature selection.

For this part, the flights with at least one null value are deleted for the model training. The airline categorical code is used
as labels. The baseline model is created by using all available columns. Then the feature importance scores are used to sort the columns by their importance.
The features are eliminated gradually until the model trained with less features shows a poorer score than the baseline.

Clustering
^^^^^^^^^^^^^^^^^^^^^
Data on flight level is aggregated on airline level by extracting only mean value or median value for each feature. Clustering
can be then carried out on the data on airline level.

Clustering is conducted mainly by hierarchical clustering in which Ward's method is used to define the distance between two clusters,
and Euclidean distance is used. K-means associated with silhouette analysis is employed to propose an optimal number of clusters.

For the visualisation part, principal component analysis is used to show the distribution of airlines and the clustering situation
on the principal plane.

Three clusterings are proposed :
    + using the whole dataset
    + using only weather data issued from METAR
    + using only operational data issued from ADS-B


Documentation of functions in **pretreatment.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: data_preparation
    :members:

Documentation of functions in **cluster.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: cluster
    :members: