"""Functions to do CRUD operations on database (civic)"""

from model import db, User, Event, UserEvent, CreatedEvent, Preference, UserPreference, connect_to_db

#Functions here


def check_pref()
    #if category/keyword already in preferences:
        #create new user_pref record and connect user_id to preference
    #if category/keyword NOT in preferences:
        #call create_pref() function
    
def create_pref(keyword):
    new_pref = Preference(keyword_search=keyword)
    # add to database
    return new_pref

#connect user to their preference in user_preference table 
def create_connection(user_id, pref_obj):
#- User_id can be in a session to keep track of who’s currently logged in
#- Create a user/preference in the user_preferences table


def create_event():
#-  Create an event object
    new_event = CreatedEvent()
    
    #query into preference table and pull out all existing event_category
    categories = Preference.query.filter(event_category).all()

#Check preferences table for that event_category
    if event_category in categories:

 #   - Add if its not there, do nothing if it is there



if __name__ == '__main__':
    from server import app
    connect_to_db(app)








