"""Server with all routes"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "DEV" #need to change this and add to secrets.sh
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def index():
    """Return homepage"""
    #if user has already signed in, redirect to feed
    #if not, prompt them to create an account and show unfiltered list of events

    # if 'name' in session:
    #     return redirect("/feed")
    # else:
    #     return 
    return render_template("homepage.html")

@app.route("/create-account")
def create_account():
    """Form for user to create account"""
    
    return render_template('/create-account.html')


@app.route("/feed", methods=["POST"])
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
    
    return render_template("/feed.html",fname=fname)


@app.route("/create-event")
def create_event():
    """Take in event info from user"""

    return render_template("create-event.html")

@app.route("/event-confirm", methods=["POST"])
def confirm_added_event():
    """Commit event to DB and present confirm page"""
    
    name = request.form.get("name")
    category = request.form.get("category")
    start_date = request.form.get("start_date")
    address = request.form.get("address")
    description = request.form.get("description")
    image = "https://unsplash.com/photos/Evo4wmtRaPI" #how to capture whatever they want to upload

    event = crud.create_event(name=name, category=category, start_date=start_date, 
                                address=address, description=description, image=image)
    
    #connect user to event
    #user = user[session] 

    return render_template("event-confirm.html", name=name)



if __name__ == "__main__":
    
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True) 