"""Server with all routes"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for, abort)

#for handling images
import os
from werkzeug.utils import secure_filename

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "DEV" #need to change this and add to secrets.sh

#GOOGLE_MAPS_API_KEY = os.environ['API_KEY']




#set a max size for images uploaded--anything larger than 1MB will be rejected
#app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

#set acceptable file extensions for images uploaded
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif", ".PNG", ".JPEG", ".jpeg"]

#UPLOAD_IMAGE_PATH = "/static/images/"
app.config["UPLOAD_IMAGE_PATH"] = "static/images/"


app.jinja_env.undefined = StrictUndefined




@app.route("/")
def index():
    """View homepage"""

    
    random_events = crud.get_events()


    
    #grab images from Event objects so they can be loaded on homepage 
    
    #event_images = crud.get

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

    keyword_search = request.form.get("keyword")
    #print(f"---- KEYWORD RECEIVED BY SERVER = {keyword_search}------")
    categories = request.form.getlist("categories")
    #print(f"---- CATEGORIES RECEIVED BY SERVER = {categories}------")

    filtered_events = crud.filter_events_by_prefs(keyword_search, categories)

    return render_template("/homepage.html", events=filtered_events)



@app.route("/save-filter", methods=["POST"]) 
def save_pref_to_user():
    """Save a search filter to user's profile"""
    
    logged_in_user = session["user_id"]
    
    #get JSON string from JS and turn into Python ob
    data = request.get_json()
    print(data)

    categories = []

    #loop over items in dict returned by JSON request 
    for stored_key, stored_value in data.items():
        #if a checkbox was checked (i.e. "true")
        if stored_value == "true":
            #add the associated key into a list of categories
            categories.append(stored_key)
       #if the value of a keyword_key is NOT empty
        if (stored_key == "keyword") and (stored_value != ""):
           #keyword = stored_value
           #save keyword as user_pref in db
           crud.save_keyword_as_user_pref(logged_in_user, stored_value)
    
            
    #save list of categories just built as user_prefs in db
    crud.save_categories_as_user_prefs(logged_in_user, categories)
    
    
    return jsonify("items saved") # delete this after debugging 

#if the homepage is filtered by category or keyword
#"Save filter" should show up

@app.route("/save-event", methods=["POST"]) 
def save_event_to_user_from_homepage():
    """Save an event to a user without redirecting to event page"""

    logged_in_user = session["user_id"]
    
    # get JSON string from JS and turn into Python ob
    data = request.get_json()
    # print(f'HERE IS DATA = {data}-------')
    # print(f'HERE IS LOGGED_IN_USER = {logged_in_user}')
    
    #get event object from event ID pulled from button ID
    event = crud.get_event_by_id(data)
    #print(f'EVENT_OBJ = {event}')
    
    #connect user to event 
    crud.connect_user_to_event(logged_in_user, event)

    return jsonify("items saved") # delete this after debugging 

@app.route("/saved-filter.json") 
def filter_homepage_by_prefs():
    """Filter homepage based on user's prefs"""

    #-----Compiles list of relevant events for user 
    #-----------and sends back to JS in JSON object

    events = crud.filter_events_by_user_prefs(session["user_id"])
    print(f'HERE ARE EVENTS FROM SERVER = {events}------')
    
    event_list = []
    # print(f"------JSONIFY LIST = {jsonify(event_list)}-------")

    #open list of event objs and loop over 
    for event in events: 
        #if event obj is an empty list
        if event == []:
            continue
        else:
            #create dict for each event obj with attributes as values
            print(f"HERE IS THE EVENT LOOPING = {event}")
            event_dict = {"event_id": event.event_id, "creator_id": event.creator_id, "name": event.name, "category": event.category, 
                        "start_date": event.start_date, "address": event.address,
                        "description": event.description, "image": event.image}
            event_list.append(event_dict)
    
    #key will be the field names, what js identifies
    #append each dict to a list
    #jsonify that list 

    print(f"***EVENT LIST = {event_list}****")
    print(f"***JSONIFIED EVENT LIST = {jsonify(event_list)}****")
    return jsonify(event_list)

# @app.route
# def remove_event_from_user():
#     """Remove event from user"""

#     get event id, turn into event object, get the user object, 
#     db.session.commit()

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
    #print(f"****HERE IS EVENT = {event}")

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
        
        saved_events = crud.get_user_saved_events(logged_in_user)
        
        #print(f'----HERE ARE EVENTS FROM SERVER = {events}-----')
        
        created_events = crud.get_user_created_events(logged_in_user)

        prefs = crud.get_user_prefs(user_id)
        #print(f'----HERE ARE PREFS FROM SERVER = {prefs}-----')

        categories = crud.get_user_categories(prefs)
        keywords = crud.get_user_keywords(prefs)

        return render_template("user-profile.html", user=user, saved_events=saved_events, created_events=created_events, prefs = prefs, categories=categories, keywords=keywords)
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
    #add logic to give error if not enough fields are filled out
    
    logged_in_user = session.get("user_id")

    name = request.form.get("name")
    category = request.form.get("category")
    start_date = request.form.get("start_date")
    address = request.form.get("address")
    description = request.form.get("description")
    #image = request.files["image"] #how to capture whatever they want to upload
    
    #print(f'----HERE IS IMAGE = {image}---')
    #upload_file()
    
    #HANDLE IMAGE
    def upload_file():
        print("===We're in upload_file===")
        uploaded_file = request.files["image"]

        print(f'===uploaded_file = {uploaded_file}====')

        filename = secure_filename(uploaded_file.filename)
        print(f'====here is filename = {filename} ====')

        #if the filename is not empty
        if filename != " ":
            #pull out the file extension by splitting filename and indexing to suffix
            # file_ext = os.path.splitext(filename)[1]
           # print(f'===file_ext = {file_ext}====')
            #if the file's ext is not in our list of accepted exts, give 500 
            # if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                # flash("Make sure image has an extension of .jpg, .png, .gif, .PNG, .JPEG, or .jpeg.")
            
            uploaded_file.save(os.path.join(app.config["UPLOAD_IMAGE_PATH"], filename))
            print("-----Image was correctly stored!------")

        return uploaded_file, filename

    #allow users to not uploaded images
    uploaded_file, filename = upload_file()
    # print(f'----output from upload_file = {uploaded_file, filename}------')

    #need to figure out how to create URL from upload_file output !
    image_url = url_for("static", filename= "images/" + filename)
    #image_url = url_for('static')  
    print(f'====image_url = {image_url}====')


    #crud.upload_image(image)

    #set up logic to turn the image from user into a filepath so we can display it on homepage

    event = crud.create_event(creator_id=logged_in_user,name=name, category=category, start_date=start_date, 
                                address=address, description=description, image=image_url)
    
    #connect user in session to event created
    logged_in_user = session.get("user_id")

    crud.connect_user_to_event(logged_in_user, event)

    #if session user_id = the event's creator_id 
#   call this function that saves it to their account as an event they created
# if not: 
#   save to their account as a saved event 

    return render_template("event-confirm.html", event=event, name=name)

@app.route("/remove-event", methods=["POST"])
def remove_event_from_user():
    """Remove event from user logged in"""

    logged_in_user = session.get("user_id")

    data = request.get_json()
    
    #get event object from event ID pulled from button ID
    event = crud.get_event_by_id(data)
 
    #get user object
    user = crud.get_user_by_id(logged_in_user)
    
    #remove event from user in db
    crud.remove_event_from_user(user, event)

    return jsonify("items removed")


@app.route("/delete-event", methods=["POST"])
def delete_created_event():
    """Delete an event the user created"""

    logged_in_user = session.get("user_id")

    data = request.get_json()
    
    #if the user confirms that they want to delete the event
    if data != None:
         #delete event from db
        crud.delete_event(data)

        print(f"----DATA = {data}-------")
    #get event object from event ID pulled from button ID
    #event = crud.get_event_by_id(data)
 
    # #get user object
    #user = crud.get_user_by_id(logged_in_user)
    
   


    return jsonify("items removed")

if __name__ == "__main__":
    
    connect_to_db(app)

    app.run(host="127.0.0.1", debug=True) 