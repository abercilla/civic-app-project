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

#------------------- CREATE 5 DUMMY EVENTS -------------------------#

events_in_db = []
prefs_in_db = [] 

for n in range (5): 
    
    name=f'name{n+1}'
    category = f'category{n+1}'
    start_date = "2020-09-04"
    address = f'address{n+1}'
    description = f'description{n+1}'
    image = f'image{n+1}'

    event = crud.create_event(name, category, start_date, address, description, image)

    events_in_db.append(event)

#----------------- ADD EVENT CATEGORIES TO PREFERENCES -----------------#

    preference = crud.create_preference(category=category)
    prefs_in_db.append(preference)

#------------------- CREATE SEARCHES and ADD TO PREFERENCES ----------------#

for n in range(5):

    keyword_search = f'keyword_search{n}'

    preference = crud.create_preference(keyword_search=keyword_search)
    prefs_in_db.append(preference)

#------------------------- CREATE 5 USERS  ------------------------------#

for n in range(5):
    fname = f'User_fname{n+1}'
    lname = f'User_lname{n+1}'
    email = f'user{n+1}@test.com'
    phone = f'{n+1}000000000'
    password = 'test'
    zipcode = f'{n+1}0000'

    user = crud.create_user(fname, lname, email, phone, password, zipcode)

#---------------- CONNECT 1 RANDOM EVENT FOR EACH USER  -------------------#
    
    #get a random event, then remove from list 
    #...because an Event can only be created by one User
    #...(but many Events can be associated with one User)
    random_event = choice(events_in_db) 
    events_in_db.remove(random_event)

    # #create Event object for CreatedEvent object
    # new_event_obj = crud.create_event_id(random_event.created_event_id)

    #connect Event object to User object 
    crud.connect_user_to_event(user, random_event) 

#--------------- CONNECT 1 RANDOM PREFERENCE FOR EACH USER  ----------------------#
    
    #choose random pref from list
    random_pref = choice(prefs_in_db)
    print(f'HERE IS THE RANDOM_PREFERENCE= {random_pref}')

    #connect random Preference object to User object
    crud.connect_user_to_pref(user, random_pref)        
    print(f'Here are the user.preferences objects = {user.preferences}')
