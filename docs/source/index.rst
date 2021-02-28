.. AFDA documentation master file, created by
   sphinx-quickstart on Sun Feb 28 14:13:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AFDA's documentation!
================================

Installation
^^^^^^^^^^^^
Install all python requierements
   .. code-block:: bash

      pip install -r requierements.txt

In the same directory than where `AFDA` is located, create a repository
called `data` and place in it a directory `__tempo` containing the rough data
,the files `airports.csv` and `airlines.csv` and an empty directory called `metar`

At the end of installation you must the following structure:
   .. code-block:: bash

      |-data
         |-__tempo
         |-metar
         |-airlines.csv
         |-airports.csv
      |-AFDA

Documentation of python code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   DataRetriever
   PhaseComputing
   DescriptorsComputing
   Classification
   db_utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
