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



#------------------------- CREATE 5 USERS  ------------------------------#
users = []
user_ids = []

for n in range(5):
    fname = f'User_fname{n+1}'
    lname = f'User_lname{n+1}'
    email = f'user{n+1}@test.com'
    phone = f'{n+1}000000000'
    password = 'test'
    zipcode = f'{n+1}0000'

    user = crud.create_user(fname, lname, email, phone, password, zipcode)
    # add the new user_id into a users list so we can add it as a creator_id to new Event objs
    user_ids.append(user.user_id)
    users.append(user)


#------------------- CREATE 5 DUMMY EVENTS --------------------------
#-----------EACH CONNECTED TO ONE USER_ID VIA CREATOR_ID ------------# 

events_in_db = []
prefs_in_db = [] 

for n in range (5): 
   
    #grab a random user_id from user list (remember: one user can create multiple events)
    creator_id = choice(user_ids)
    name=f'name{n+1}'
    category = f'category{n+1}'
    start_date = "2020-09-04"
    address = f'address{n+1}'
    description = f'description{n+1}'
    image = f'image{n+1}'

    event = crud.create_event(creator_id, name, category, start_date, address, description, image)

    events_in_db.append(event)

#----------------- ADD EVENT CATEGORIES TO PREFERENCES -----------------#

    preference = crud.create_preference(category=category)
    prefs_in_db.append(preference)

#------------------- CREATE SEARCHES and ADD TO PREFERENCES ----------------#

for n in range(5):

    keyword_search = f'keyword_search{n}'

    preference = crud.create_preference(keyword_search=keyword_search)
    prefs_in_db.append(preference)


#---------------- CONNECT THE EVENT A USER CREATED TO THE USER ---------------#

#loop over user objs we just created
for user in users:
    
    crud.connect_user_to_their_event(user)
        
#--------- "SAVE" A RANDOM EVENT TO A USER --------------------------#

for user in users: 
    crud.connect_user_to_random_event(user)

#--------------- CONNECT 1 RANDOM PREFERENCE FOR EACH USER  ----------------------#

for user in users: 
    #choose random pref from list
    random_pref = choice(prefs_in_db)
    print(f'HERE IS THE RANDOM_PREFERENCE= {random_pref}')

    #connect random Preference object to User object
    crud.connect_user_to_pref(user, random_pref)        
    print(f'Here are the user.preferences objects = {user.preferences}')



