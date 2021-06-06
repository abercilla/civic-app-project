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

################ CREATE DUMMY EVENTS #############################
######## ADD EVENT CATEGORIES TO PREFERENCES ####################

events_in_db = []
prefs_in_db = []

for n in range (5): 
    
    name=f'name{n}'
    category = f'category{n}'
    start_date = "2020-09-04"
    location = f'location{n}'
    description = f'description{n}'
    image = f'image{n}'

    event = crud.create_event(name, category, start_date, location, description, image)
    print(f"We created the event with {category}")

    events_in_db.append(event)
    print(f'***Here are event objects in list =  {events_in_db}')
    #add event categories to preferences table

    preference = crud.create_preference(category=category)
    prefs_in_db.append(preference)
    print(f'***Here are the Preference (category) objects in list = {prefs_in_db}')

################ CREATE DUMMY SEARCHES & ADD TO PREFERENCES #####################

for n in range(5):

    keyword_search = f'keyword_search{n}'

    preference = crud.create_preference(keyword_search=keyword_search)
    prefs_in_db.append(preference)
    print(f'***Here are the Preference (keyword_search) objects in list = {prefs_in_db}')


################ CREATE DUMMY USERS AND CONNECT TO EVENTS and PREFERENCES #####################

for n in range(10):
    fname = f'User_fname{n}'
    lname = f'User_lname{n}'
    email = f'user{n}@test.com'
    password = 'test'
    zipcode = f'0000{n}'

    user = crud.create_user(fname, lname, email, password, zipcode)
    print(f'****HERE IS A USER = {user}')
    #append a random event to 5 users

    for _ in range(1):
        random_event = choice(events_in_db)
        print(f'HERE IS THE RANDOM_EVENT = {random_event}')
        
        crud.connect_user_event(user, random_event) #IT ERRORS OUT HERE WITH A KEYERROR 'CAN'T RECOGNIZE 'USERS'
        #print(f'Here are the user.event objects = {user.events}')

    #append a random prefernce to 3 users
    for __ in range(3):
        random_pref = choice(prefs_in_db)
        print(f'HERE IS THE RANDOM_PREFERENCE= {random_pref}')

        user.preferences.append(random_pref)        
        print(f'Here are the user.preferences objects = {user.preferences}')
