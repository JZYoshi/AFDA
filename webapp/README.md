To start the web application:

1. install node.js and npm if it's not installed
2. go to the vue/client directory
3. execute `npm install` and wait for the packages installation
4. execute `npm run build` and wait for the compilation
5. rename a .db file to 'descriptors.db' and put it inside webapp/instance
6. go to the webapp/webapp directory
7. set up environment variables (execute `$env:FLASK_ENV="development"`; `$env:FLASK_APP="t"`; `set FLASK_APP=t.py`)
8. run the server by executing `flask run`