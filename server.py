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
    """View homepage"""

    
    random_events = crud.get_events()

    return render_template("homepage.html", events=random_events)
    
    #-------code for if I want the homepage to display different things------#
    #------------based on whether whether someone is logged in---------------#
    

    #logged_in_user = session.get("user_id")

    # if logged_in_user:
    #     filtered_events = crud.filter_events_by_user_prefs(logged_in_user)
    #     return render_template("homepage.html", events=filtered_events)
    # else:
    #     random_events = crud.get_events()
    #     return render_template("homepage.html", events=random_events)
    #     if button is clicked, run this other thing

@app.route("/", methods=["POST"])
def filter_homepage():
    """Filter homepage by unsaved search and/or categories"""
    #-----currently runs the search all over again with each form submit----#
    #-----as opposed to adding searches on top of each other----------------#

    #take in the user's input from homepage
    keyword_search = request.form.get("keyword")
    categories = request.form.getlist("categories")

    #filter events by input 
    filtered_events = crud.filter_events_by_prefs(keyword_search, categories)

    return render_template("/homepage.html", events=filtered_events)

@app.route("/", methods=["POST"])
def save_pref_to_user():
    """Save a search filter to user's profile"""

#if the homepage is filtered by category or keyword

#"Save filter" should show up

#save criteria from form as a preference



@app.route("/events/<event_id>")
def show_event(event_id):
    """Show details of a particular event"""

    logged_in_user = session.get("user_id")
    event = crud.get_event_by_id(event_id)

    return render_template("event_details.html", event=event)

@app.route("/events/<event_id>", methods=["POST"])
def save_event_to_user(event_id):
    """Save event to current user"""

    logged_in_user = session.get("user_id")
    
    event = crud.get_event_by_id(event_id)
    print(f"****HERE IS EVENT = {event}")

    #Save event to current user's account
    if logged_in_user:
        crud.connect_user_to_event(logged_in_user, event)
        flash("* Event successfully saved! *")
        return render_template("event_details.html", event=event)
    else:
        flash("* Oops! Create an account to save an event. *")
        return render_template("event_details.html", event=event)


@app.route("/login")
def show_login():
    """Display Login form""" 

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def collect_login():
    """Process login"""

    email = request.form.get("email")
    password = request.form.get("password")  
    
    #do a db search with check_email and store returned user object in user
    user = crud.check_email(email)

    if not user or user.password != password:
        flash("Email or password doesn't match.")
        return redirect("/login")
    else:
        session["user_id"] = user.user_id

        #-----if we want to be redirected to the homepage with prefs filtered----#
        # logged_in_user = session.get("user_id")
        # print(f'******** HERE IS THE SESSION = {session} ********')
        #filtered_events = crud.filter_events_by_user_prefs(logged_in_user)
        # return render_template("/homepage.html", events=events)

        random_events = crud.get_events()
        return render_template("homepage.html", events=random_events)

@app.route("/user-profile/<user_id>")
def show_profile(user_id):
    """Show a user's profile with saved events and preferences"""
    
    logged_in_user = session.get("user_id")
    #---BUG--My Profile button doesn't work when we're already on the user's profile
    if logged_in_user:
        user = crud.get_user_by_id(user_id)
        events = crud.filter_events_by_user_prefs(logged_in_user)
        prefs = crud.get_user_prefs(user_id)
        categories = crud.get_user_categories(prefs)
        keywords = crud.get_user_prefs(prefs)

        return render_template("user-profile.html", user=user, events=events, categories=categories, keywords=keywords)
    else:
        flash("Access Denied. Create an account to access this page.")
        return redirect("/")

 

    return render_template("user-profile.html", fname=fname, lname=lname)

@app.route("/logout")   
def logout_user():
    """Process logout"""

    del session["user_id"]

    return render_template("logout.html")

   
@app.route("/create-account")
def create_account():
    """Display Create Account form"""
    
    return render_template("create-account.html")

@app.route("/create-account", methods=["POST"])
def collect_account():
    """Collect account info for user"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")
    categories = request.form.getlist("categories")

    
    #check if account already exists
    user = crud.check_email(email)

    if user:
        flash("Account already exists with this email. Try again.")
        return redirect("/create-account")
    else:
        user = crud.create_user(fname=fname, lname=lname, email=email, 
                    phone=phone, password=password, zipcode=zipcode)
        
        #collect categories chosen and connect to user
        crud.connect_user_to_multiple_prefs(user, categories)
        return render_template("feed.html", fname=fname)
    #render same template with specific events based on queries about preferences
    #or just render template with first 25 events


@app.route("/create-event")
def create_event():
    """Take in event info from user"""
    
    logged_in_user = session.get("user_id")

    if logged_in_user is None:
        flash(f"Please log in to create an event.")
    else:  
        flash(f"User with user_id =  {logged_in_user} is currently logged in")

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
    
    #connect user in session to event created
    logged_in_user = session.get("user_id")

    crud.connect_user_to_event(logged_in_user, event)

    #if session user_id = the event's creator_id 
#   call this function that saves it to their account as an event they created
# if not: 
#   save to their account as a saved event 

    return render_template("event-confirm.html", name=name)



if __name__ == "__main__":
    
    connect_to_db(app)

    app.run(host="127.0.0.1", debug=True) 