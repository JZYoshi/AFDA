Flight phase computation
========================

The computation of flight phase is achieved thanks to the script **flight_phase.py**.
This script processes each file containing rough flight data. Each file contains the data
of flights which has a specific flight number. Thus, each file contains potentially
several flights.

The script processes each file one by one applying the same algorithm. For each files, it splits
it into several flight. Then for each file, it applies a function in openap library which associates to
each data a label to indicate in which phase the plane is. Then, since the data is often bad quality,
it applies several rules to determines which phase of the flight can be kept. Finally, the algorithm
save every phase which are considered as clean in a directory.

.. Note::
    Since this script can be very long to execute, the algorithm uses parallel computing (MPI). So,
    you must execute this script with this library.

To execute this script, enter these commands from project root:

    .. code-block:: bash
    
        cd flight\ phase\ on\ dataset
        mpiexec -n "number of thread" python flight_phase.py

Documentation of functions in **flight_phase.py**:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: flight_phase
    :members: