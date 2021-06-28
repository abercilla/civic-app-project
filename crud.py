"""Functions to do CRUD operations on database (civic)"""
"""CRUD = Create, Read, Update, Delete """

from model import db, User, Event, Preference, connect_to_db, user_events_association_table, user_prefs_association_table
from datetime import datetime

def create_user(fname, lname, email, phone, password, zipcode):
    
    user = User(fname=fname, lname=lname, email=email, 
                phone=phone, password=password, zipcode=zipcode)
    
    db.session.add(user)
    db.session.commit()

    return user

def create_event(creator_id, name, category, start_date, address, description, image):
    
    event = Event(creator_id=creator_id, name=name, category=category,
                    start_date=start_date, address=address,
                    description=description, image=image)
    db.session.add(event)
    db.session.commit()
    print("We're in create_event and it's been committed")
    return event


def create_preference(category=None, keyword_search=None):
    """Create a preference"""

    preference = Preference(category=category, keyword_search=keyword_search)
    print("We tried instantiating a preference")

    db.session.add(preference)
    db.session.commit()

    return preference


def check_category(category): #can i refactor this so category AND keyword are in one function to check against everything in prefernces? 
    """Figure out what to do with category entered
            by user when creating a new event"""
     
    result = Preference.query.filter_by(category=category).first()

    if not result:
        return save_category(category)
        
    return result

def save_category(category): 
    """If user saves a NEW category, add to db"""

    new_category = Preference(category=category)

    db.session.add(new_category)
    db.session.commit()
   
    return new_category
        

def check_search(keyword_search):
    """Figure out what to do with keyword_search saved"""

    result = Preference.query.filter_by(keyword_search=keyword_search).first()

    if not result:
        return save_search(keyword_search)
        
    return result

def save_search(keyword_search):
    """If user saves a NEW search, add to db"""

    new_search = Preference(keyword_search=keyword_search)

    db.session.add(new_search)
    db.session.commit()
   
    return new_search

def save_categories_as_user_prefs(user_id, categories):
    """Handle categories a user wants to save as a preference"""
    #one Pref = one category OR one keyword
    #..so we're conncting one user with multiple preferences depending on what they inputted
    user = User.query.get(user_id)

    prefs = []

    #take in category list user wants saved
    for category in categories: 
        #use check_category and save_category to check existence of a pref obj for each category (create one if not)
        #add pref objs returned to a list
       prefs.append(check_category(category))

    #return prefs

    #loop over pref objs returned
    for pref in prefs: 
        #connect each pref obj to the user
        connect_user_to_pref(user, pref)
    
    print(f"-------Here are user_prefs from categories = {user.preferences}-----")

    
def save_keyword_as_user_pref(user_id, keyword):
    """Handle keyword user wants to save as a preference"""

    user = User.query.get(user_id)

    pref = check_search(keyword)

    connect_user_to_pref(user, pref)

    print(f"-------Here are user_prefs from keyword = {user.preferences}-----")


def get_user_by_id(user_id):
    """Get user by user_id"""

    return User.query.get(user_id)

def connect_user_to_event(user_id, event_obj):
    """Connect a User to an Event"""

    #this will just connect user_id to Event...
    #...but not make a distinction whether they created it or not
    print("********WE ARE IN CONNECT_USER_TO_EVENT***********")
    user_obj = User.query.get(user_id)
    # event_obj = Event.query.get(event_id)
    
    user_obj.events.append(event_obj) #BUG -- event_obj is coming in as <event_id>

    db.session.commit()
    print(f"-----HERE IS THE EVENT WE COMMITTED = {event_obj}-----")
    print("**********WE COMMITTED THE USER_EVENT RELATIONSHIP*********")

    return event_obj

def get_user_saved_events(user_id):
    """Get all events a user has saved (not created)"""
    
    #get user obj from user_id
    user = User.query.get(user_id)
    
    #get events that are connected to this user
    events_saved = user.events

    events_to_return = []
      
    #loop over events, pull out creator_ids
    for event_saved in events_saved:
        #pull out events this user saved that were NOT created by the user
        if event_saved.creator_id != user_id:
            events_to_return.append(event_saved)

    return events_to_return
    

def get_user_created_events(user_id):
    """Get events a user created"""
    
    user = User.query.get(user_id)
    
    #get events that are connected to this user
    events_saved = user.events

    events_to_return = []
    
    #loop over events, pull out creator_ids
    for event_saved in events_saved:
        #pull out events this user saved that WERE created by the user
        if event_saved.creator_id == user_id:
            events_to_return.append(event_saved)

    return events_to_return
    


def connect_user_to_their_event(user):
    """Connect event(s) a user created to them via user.events"""
    #print("We are in crud.connect_user_to_their_event")
    #find the events that were created by that user
    event_to_add = Event.query.filter_by(creator_id=user.user_id).all()
    #print(f"------Here is event_to_add = {event_to_add}-----")
    #if the user didn't create any events (event_to_add = [])
    if len(event_to_add) < 1:
        print("No Events Created By User") 
    else:
        user.events.extend(event_to_add)

    return user.events

def connect_user_to_random_event(user):
    """For seed_database.py"""
    
    #grab the first event found that was NOT created by that user
    event_to_save = Event.query.filter(Event.creator_id != user.user_id).first()
    user.events.append(event_to_save)
    
    return user.events


def connect_user_to_pref(user, pref):
    """Connect a User to an Preference"""
    #add in functionality to make sure we are 
    #...only adding the preference to the user in session
    user.preferences.append(pref)

    db.session.commit()

def connect_user_to_multiple_prefs(user, categories):
    """Connect User to Multiple Preference(s)"""
    
    #print('************we are in connect_user_to_multiple_prefs**********')
    #pull out the Preference object associated with each category in pref_list
    pref_objs = []

    for category in categories:
        pref_obj = Preference.query.filter_by(category=category).first()
        pref_objs.append(pref_obj)
    
   # print(f'HERE ARE THE PREF_OBJS = {pref_objs}')

    #attach Preference object to User object
    for pref in pref_objs:
        user.preferences.append(pref)
    
    db.session.commit()

def remove_event_from_user(user, event):
    """Remove saved event from user profile"""

    user.events.remove(event)
    db.session.commit()

def delete_event(event_id):
    """Delete event from db"""
    event = Event.query.get(event_id)
    print(f'----event to delete = {event}-----')

    db.session.delete(event)
    db.session.commit()

def remove_keyword_from_user(user_id, keyword):
    """Remove keyword as pref from user"""

    user = User.query.get(user_id)
    print(f'----USER = {user}-------')

    delete_keyword = Preference.query.filter(Preference.keyword_search == keyword).first()
    print(f'----delete keyword = {delete_keyword}-------')
    
    user.preferences.remove(delete_keyword)
    db.session.commit()
    

def remove_category_from_user(user_id, category):
    """Remove category as pref from user"""

    user = User.query.get(user_id)
    print(f'----USER = {user}-------')

    
    delete_category = Preference.query.filter(Preference.category == category).first()
    print(f'----delete category = {delete_category}-------')

    user.preferences.remove(delete_category)
    db.session.commit()

    


#add search functionality in here
#search by user_Id so they can see what things they've saved
def search_by_user_id(user_id):
    """Search for user_id based on sign-in info"""

def check_email(email):
    """See if input matches user info in db"""

    return User.query.filter(User.email == email).first()

def get_events():
    """Return all events"""
    
    return Event.query.all()

def get_event_by_id(event_id):
    """Return event by event_id"""

    return Event.query.get(event_id)

def filter_events_by_prefs(keyword_search=None, categories=None):
    """Filter homepage events based on non-user search"""
    print("**********WE ARE IN FILter_BY_PREFS*****")
    print(f"-----------KEYWORD_SEARCH IN FUNCTION = {keyword_search}------")
    print(f"-----------CATEGORY LIST IN FUNCTION = {categories}------")
    events = []

    
    if categories: 
        #pull out events that fit chosen categories
        for category in categories:
                events.extend(Event.query.filter_by(category=category).all())
        #categories.append(user_pref.category)
    
    if keyword_search:
        #pull out events that have chosen keyword (KEY SENSITIVE)
        events.extend(Event.query.filter((Event.description.like(f'%{keyword_search}%')) | (Event.name.like(f'%{keyword_search}%'))).all())

    
    print(f"**********HERE ARE EVENTS = {events}*****")

    return events

def filter_events_by_user_prefs(user_id):
    """Pull out events that fit a user's preferences"""
    
    #Get list of Preference objects for user based on user_id
    user_prefs = Preference.query.join(user_prefs_association_table).join(User).filter((user_prefs_association_table.c.pref_id == Preference.pref_id) & (user_prefs_association_table.c.user_id == user_id)).all()
    
    categories = []
    keywords = []
    events = []
    
    #loop over Preference objects in user_prefs list...
    #...pull out any categories or keywords the user saved
    for user_pref in user_prefs:
        if user_pref.category: 
            categories.append(user_pref.category)
        if user_pref.keyword_search != None:
            keywords.append(user_pref.keyword_search)
    
    #pull out events tied to those categories and keywords
    for category in categories:
        events.extend(Event.query.filter_by(category=category).all())
            
    for keyword in keywords:
        events.append(Event.query.filter((Event.description.like(f'%{keyword}%')) | 
                                            (Event.name.like(f'%{keyword}'))).all())

    print(f"--------HERE ARE THE EVENTS FROM CRUD= {events}--------")
    return events




def get_user_prefs(user_id):
    """Grab prefs for a user"""

    user = User.query.get(user_id)
    prefs = user.preferences

    print(f"------HERE ARE USER PREFS from CRUD = {prefs}----")
    return prefs
    

def get_user_categories(prefs):
    """Get categories from user's preferences"""
    
    categories = []
    #loop over list of pref objects
    for pref in prefs: 
        #if that pref object has a category attached, pull it out
        if pref.category:
            categories.append(pref.category)
    
    print(f'----HERE ARE CATEGORIES IN CRUD = {categories}-----')
    return categories
   
    
def get_user_keywords(prefs):
    """Get keywords from user preferences"""
    
    keywords = []
    #loop over list of pref objects
    for pref in prefs: 
        #if that pref object has a category attached, pull it out
        if pref.keyword_search:
            keywords.append(pref.keyword_search)

    print(f'----HERE ARE KEYWORDS IN CRUD = {keywords}-----')

    return keywords


def convert_start_dates(events):

    """Convert datetime object to be readable to user"""
    #don't think i need this actually since they display correctly with Jinja        
    converted_date = start_date.strftime("%A, %B %d %Y")

    return converted_date

if __name__ == '__main__':
    from server import app
    connect_to_db(app)








