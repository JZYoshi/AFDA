Descriptors computation
=======================

The scripts **flight_descriptors.py** and **flight_descriptors_mpi.py** compute the descriptors of each flight which has been get.
Thus they processe every flights which phase have already been calculted one by one.
The result is a sqlite database containing 4 tables:

    + a table climb
    + a table cruise
    + a table descent
    + a table general_info

These 4 tables have the same numbers of rows. One row contains all descriptors of the
flight identified by a key which is its flight_id.

.. Note::
    Since this script can be very long to execute, the two algorithms use parallel computing.
    We have written two version: **flight_descriptor.py** wich uses threads
    and **flight_descriptors_mpi.py** wich uses MPI.

To execute these script, enter these commands from project root:

    .. code-block:: bash
    
        cd PhaseAndDescComputation
        mpiexec -n "number of thread" python flight_descriptors_mpi.py
        (or)
        python flight_descritors.py

.. warning::
    Before executing this script, you must have already compute the phase of all
    flights excuting **flight_phase.py**.

Documentation of functions in **flight_descriptors.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: flight_descriptors
    :members: