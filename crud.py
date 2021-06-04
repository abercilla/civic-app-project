"""Functions to do CRUD operations on database (civic)"""

from model import db, User, Event, CreatedEvent, Preference, connect_to_db
from datetime import datetime

def create_user(fname, lname, email, password, zipcode):
    
    user = User(fname=fname, lname=lname, email=email, 
                    password=password, zipcode=zipcode)
    
    db.session.add(user)
    db.session.commit()

    return user

def create_event(name, category, start_date, location, description, image):
    
    event = CreatedEvent(name=name, category=category,
                            start_date=start_date, location=location,
                            description=description, image=image)
    db.session.add(event)
    db.session.commit()
    #print("We're in create_event and it's been committed")
    return event


def create_preference(category=None, keyword_search=None):
    """Create a preference"""

    preference = Preference(category=category, keyword_search=keyword_search)
    #print("We tried instantiating a preference")

    db.session.add(preference)
    db.session.commit()

    return preference


def check_category(category): #can i refactor this so category AND keyword are in one function to check against everything in prefernces? 
    """Figure out what to do with category entered
            by user when creating a new event"""
     
    result = Preference.query.filter_by(category=category).first()

    if not result:
        save_search(category)
        

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
        save_search(keyword_search)


def save_search(keyword_search):
    """If user saves a NEW search, add to db"""

    new_search = Preference(keyword_search=keyword_search)

    db.session.add(new_search)
    db.session.commit()
   
    return new_search

# def connect_user_pref(user_id, pref_obj):
#     """Connect saved category/keyword to user"""
#     #user[session] = 
#     user[session].preferences.append(pref)


#connect user to their preference in user_preference table 
#def create_connection(user_id, pref_obj):
#- User_id can be in a session to keep track of who’s currently logged in


#connect created_event to events
def create_event_id(created_event_id):

    new_event = Event(created_event_id=created_event_id, 
                        eventbrite_event_id=None,
                        mobilize_event_id=None)
    
    db.session.add(new_event)
    db.session.commit()

    return new_event

def connect_user_event(user, event):
    
    user.events.append(event)
    

#add search functionality in here
#search by user_Id so they can see what things they've saved







if __name__ == '__main__':
    from server import app
    connect_to_db(app)








