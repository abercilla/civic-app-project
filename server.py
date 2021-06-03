# """Server for civic app"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "anne" #need to change this and add to secrets.sh
app.jinja_env.undefined = StrictUndefined

# #Replace with routes and view functions!


if __name__ =='__main__':
    app.run(host='0.0.0.0', debug=True)