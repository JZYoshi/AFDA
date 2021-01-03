To start the web application:

1. install node.js if it's not installed
2. go to the vue/client directory
3. execute `node run build` and wait for the compilation
4. rename a .db file to 'descriptors.db' and put it inside webapp/instance
5. go to the webapp/webapp directory
6. set up environment variables (execute `$env:FLASK_ENV="development"`; `$env:FLASK_APP="t"`; `set FLASK_APP=t.py`)
7. run the server by executing `flask run`