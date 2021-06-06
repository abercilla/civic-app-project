"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb civic')
os.system('createdb civic')

model.connect_to_db(server.app)
model.db.create_all()

#----------------- CREATE DUMMY CREATED_EVENTS -------------------#

created_events_in_db = []
prefs_in_db = [] 

for n in range (5): 
    
    name=f'name{n}'
    category = f'category{n}'
    start_date = "2020-09-04"
    location = f'location{n}'
    description = f'description{n}'
    image = f'image{n}'

    created_event = crud.user_creates_event(name, category, start_date, location, description, image)

    created_events_in_db.append(created_event)

#----------------- ADD EVENT CATEGORIES TO PREFERENCES -----------------#

    preference = crud.create_preference(category=category)
    prefs_in_db.append(preference)

#------------------- CREATE SEARCHES, ADD TO PREFERENCES ----------------#

for n in range(5):

    keyword_search = f'keyword_search{n}'

    preference = crud.create_preference(keyword_search=keyword_search)
    prefs_in_db.append(preference)

#------------------------- CREATE 5 USERS  ------------------------------#

for n in range(5):
    fname = f'User_fname{n}'
    lname = f'User_lname{n}'
    email = f'user{n}@test.com'
    password = 'test'
    zipcode = f'0000{n}'

    user = crud.create_user(fname, lname, email, password, zipcode)

#---------------- CONNECT 1 RANDOM EVENT FOR EACH USER  -------------------#
    
    #get a random created_event, then remove from list 
    #...because a CreatedEvent can only be created by one User
    #...(but many *Events* can be associated with one User)
    random_event = choice(created_events_in_db) 
    created_events_in_db.remove(random_event)

    #create Event object for CreatedEvent object
    new_event_obj = crud.create_event_id(random_event.created_event_id)

    #connect new Event object to User object 
    crud.connect_user_to_event(user, new_event_obj) 

#--------------- CONNECT 1 RANDOM PREFERENCE FOR EACH USER  ----------------------#
    
    #choose random pref from list
    random_pref = choice(prefs_in_db)
    print(f'HERE IS THE RANDOM_PREFERENCE= {random_pref}')

    #connect random Preference object to User object
    crud.connect_user_to_pref(user, random_pref)        
    print(f'Here are the user.preferences objects = {user.preferences}')
