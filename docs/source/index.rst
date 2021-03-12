.. AFDA documentation master file, created by
   sphinx-quickstart on Sun Feb 28 14:13:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AFDA's documentation!
================================

Installation
^^^^^^^^^^^^
Install all python requirements
   .. code-block:: bash

      pip install -r requirements.txt

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

---------------------------------------

Run the web application for data visualization:
   1. install *node.js* and *npm* if it's not installed
   2. go to the **vue/client** directory
   3. execute `npm install` and wait for the packages installation
   4. execute `npm run build` and wait for the compilation
   5. rename a .db file to 'descriptors.db' and put it inside **webapp/instance**
   6. go to the **webapp/** directory
   7. set up environment variables (execute `$env:FLASK_ENV="development"`; `$env:FLASK_APP="server"`)
   8. run the server by executing `flask run`

----------------------------------------

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
