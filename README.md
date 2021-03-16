Welcome to AFDA!
================================

## Install all python requirements

    pip install -r requirements.txt

In the repository data, place the files `airports.csv` and `airlines.csv`.
If you want to use the data that we provide, place also the repository `__tempo`
containing the flight data and the repository `metar` containing the weather data.
Once you've done that, you can perform the phase, descriptors and classification computation,
then you will be able to run the webapp to visualize the results.

---------------------------------------

## Run the web application for data visualization:
   1. install *node.js* and *npm* if it's not installed
   2. go to the **vue/client** directory

        cd webapp/vue/client

   3. execute `npm install` and wait for the packages installation

        npm install

   4. execute `npm run build` and wait for the compilation

        npm run build

   5. rename a .db file to 'descriptors.db' and put it inside **webapp/instance**
   6. go to the **webapp/** directory
   7. set up environment variables (execute `$env:FLASK_ENV="development"`; `$env:FLASK_APP="server"`)
         
        $env:FLASK_ENV="development"

        $env:FLASK_APP="server"
         
   8. run the server by executing `flask run`

        flask run