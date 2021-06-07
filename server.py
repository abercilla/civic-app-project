"""Server with all routes"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "DEV" #need to change this and add to secrets.sh
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Return homepage"""
    #if user has already signed in, redirect to feed
    #if not, prompt them to create an account and show unfiltered list of events

    # if 'name' in session:
    #     return redirect("/feed")
    # else:
    #     return 
    return render_template('homepage.html')

@app.route('/create-account')
def create_account():
    """Form for user to create"""

    
    
    return render_template('/create-account.html')


@app.route('/feed', methods=['POST'])
def collect_account():
    """Collect account info for user"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")
    
    user = crud.create_user(fname=fname, lname=lname, email=email, 
                    phone=phone, password=password, zipcode=zipcode)

    #print(f'HERE IS THE USER = {user}')

    #collect categories chosen and connect to user
    categories = request.form.getlist("categories")
    crud.connect_user_to_multiple_prefs(user, categories)

    #print(f'HERE ARE THE USER_PREFS= {user.preferences}')

    
    #session[user.user_id]
    
    return render_template('/feed.html',fname=fname)


if __name__ == "__main__":
    
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True) 