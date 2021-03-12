Descriptors computation
=======================

The script **flight_descriptors.py** computes the descriptors of each flight which has been get.
Thus it processes every flight which phase have already been calculted one by one.
The result is a sqlite database containing 4 tables:

    + a table climb
    + a table cruise
    + a table descent
    + a table general_info

These 4 tables have the same numbers of rows. One row contains all descriptors of the
flight identified by a key which is its flight_id.

To execute this script, enter these commands from project root:

    .. code-block:: bash
    
        cd flight\ phase\ on\ dataset
        python flight_descriptors.py

.. warning::
    Before executing this script, you must have already compute the phase of all
    flights excuting **flight_phase.py**.

Documentation of functions in **flight_descriptors.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: flight_descriptors
    :members: