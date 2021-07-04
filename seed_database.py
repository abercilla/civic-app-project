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



# #------------------------- CREATE 5 USERS  ------------------------------#
# users = []
# user_ids = []

# for n in range(5):
#     fname = f'User_fname{n+1}'
#     lname = f'User_lname{n+1}'
#     email = f'user{n+1}@test.com'
#     phone = f'{n+1}000000000'
#     password = 'test'
#     zipcode = f'{n+1}0000'

#     user = crud.create_user(fname, lname, email, phone, password, zipcode)
#     # add the new user_id into a users list so we can add it as a creator_id to new Event objs
#     user_ids.append(user.user_id)
#     users.append(user)


# #------------------- CREATE 5 DUMMY EVENTS --------------------------
# #-----------EACH CONNECTED TO ONE USER_ID VIA CREATOR_ID ------------# 

# events_in_db = []
# prefs_in_db = [] 

# for n in range (5): 
   
#     #grab a random user_id from user list (remember: one user can create multiple events)
#     creator_id = choice(user_ids)
#     name=f'name{n+1}'
#     category = f'category{n+1}'
#     start_date = "2020-09-04"
#     address = f'address{n+1}'
#     description = f'description{n+1}'
#     image = f'image{n+1}'

#     event = crud.create_event(creator_id, name, category, start_date, address, description, image)

#     events_in_db.append(event)

# #----------------- ADD EVENT CATEGORIES TO PREFERENCES -----------------#

#     preference = crud.create_preference(category=category)
#     prefs_in_db.append(preference)

# #------------------- CREATE SEARCHES and ADD TO PREFERENCES ----------------#

# for n in range(5):

#     keyword_search = f'keyword_search{n}'

#     preference = crud.create_preference(keyword_search=keyword_search)
#     prefs_in_db.append(preference)


# #---------------- CONNECT THE EVENT A USER CREATED TO THE USER ---------------#

# #loop over user objs we just created
# for user in users:
    
#     crud.connect_user_to_their_event(user)
        
# #--------- "SAVE" A RANDOM EVENT TO A USER --------------------------#

# for user in users: 
#     crud.connect_user_to_random_event(user)

# #--------------- CONNECT 1 RANDOM PREFERENCE FOR EACH USER  ----------------------#

# for user in users: 
#     #choose random pref from list
#     random_pref = choice(prefs_in_db)
#     print(f'HERE IS THE RANDOM_PREFERENCE= {random_pref}')

#     #connect random Preference object to User object
#     crud.connect_user_to_pref(user, random_pref)        
#     print(f'Here are the user.preferences objects = {user.preferences}')








#-----------------------------------------------------------------------#
#------------------------- CREATE 5 USERS  ------------------------------#
users = []
user_ids = []

user1 = crud.create_user(fname="Anne", lname="Bercilla", email="anneb@gmail.com",
                            phone="555-925-7834", password="anneb", zipcode="94598")

user_ids.append(user1.user_id)
users.append(user1)

user2 = crud.create_user(fname="Belinda", lname="Huang", email="belindah@gmail.com", 
                            phone="555-902-3948", password="belindah", zipcode="94598")

user_ids.append(user2.user_id)
users.append(user2)

user3 = crud.create_user(fname="Alaina", lname="Bercilla", email="alainab@gmail.com",
                            phone="555-925-4847", password="alainab", zipcode="30093")

user_ids.append(user3.user_id)
users.append(user3)

user4 = crud.create_user(fname="Nat", lname="Austin", email="naustin@gmail.com",
                            phone="555-684-2938", password="nata", zipcode="40039")

user_ids.append(user4.user_id)
users.append(user4)

user5 = crud.create_user(fname="Margarito", lname="Tobilla", email="margaritot@gmail.com",
                            phone="555-394-3847", password="margaritot", zipcode="90026")

user_ids.append(user5.user_id)
users.append(user5)


#------------------- CREATE 5 EVENTS --------------------------
#-----------EACH CONNECTED TO ONE USER_ID VIA CREATOR_ID -----# 

events_in_db = []
prefs_in_db = [] 



event1 = crud.create_event(creator_id=choice(user_ids), name="Black Lives Matter Protest", category="Protest",
                            start_date="2021-09-10 16:30", address="1666 North Main Street, Walnut Creek, CA, 94596",
                            description="We are planning to honor the first anniversary of George Floyd's murder by protesting police violence at Walnut Creek City Hall. We'll be making signs from 5-6pm at Civic Park #blm", 
                            image="https://www.nhpr.org/sites/nhpr/files/styles/x_large/public/202006/GeorgeFloydImage_JimUrquhartNPR.jpg")

events_in_db.append(event1)

event2 = crud.create_event(creator_id=choice(user_ids), name="Women's March Berkeley", category="March",
                            start_date="2021-01-16 11:00", address="2180 Milvia St, Berkeley, CA 94704", 
                            description="Join us for the fifth annual Women's March starting at Berkeley City Hall on Milvia! Bring a sign and water!",
                            image="https://www.washingtonpost.com/rf/image_1484w/2010-2019/WashingtonPost/2017/01/21/Others/Images/2017-01-21/DSC_1255.jpg")
events_in_db.append(event2)

event3 = crud.create_event(creator_id=choice(user_ids), name="Kamala Organizing Meeting!", category="Meeting",
                            start_date="2021-08-10 18:30", address="3810 Ingersoll Ave, Des Moines IA 50312", 
                            description="We're two weeks away from the caucuses! Come to the Kamala HQ office and strategize where to canvass in your neighborhood. Bring a notebook and any other Kamala supporters you know!",
                            image="https://lasentinel.net/wp-content/uploads/sites/5/2019/09/USbvcZLQ.jpeg")
events_in_db.append(event3)

event4 = crud.create_event(creator_id=choice(user_ids), name="Republicans for Biden Canvass", category="Canvass", 
                            start_date="2020-10-24 10:00", address="609 Colby Court, Walnut Creek CA 94598",
                            description="We're finding and persuading Republicans in Walnut Creek to vote Blue in 2020! Come meet some fellow Republicans for Biden and bring your walking shoes. We'll do a training at 10:00AM and hit the streets at 11:00AM. See you there!",
                            image="https://cdn.vox-cdn.com/thumbor/m5WrMfyKmx7sVfH-HWTR1ccJhqg=/0x0:3900x2596/1200x800/filters:focal(1465x582:2089x1206)/cdn.vox-cdn.com/uploads/chorus_image/image/67346469/GettyImages_1228140228t.0.jpg")
events_in_db.append(event4)

event5 = crud.create_event(creator_id=choice(user_ids), name="Being a Better Ally", category="Workshop",
                            start_date="2021-10-11 19:00", address="100 Larkin St, San Francisco, CA 94102",
                            description="What can we do as white people to be better allies to the Black community and other POC? We will be hosting a workshop to discuss Robin Diangelo's book, 'White Fragility'. We'll be joined by a few special guests, so bring your friends and let's get to work.",
                            image="https://img.apmcdn.org/fadc6810ccb845c54c3a9c154fc0473ddd7c4e34/uncropped/309bec-20180705-diangelo-whitefragility-2-collage.jpg")
events_in_db.append(event5)





#----------------- ADD EVENT CATEGORIES TO PREFERENCES -----------------#

preference1 = crud.create_preference(category=event1.category)
prefs_in_db.append(preference1)

preference2 = crud.create_preference(category=event2.category)
prefs_in_db.append(preference2)

preference3 = crud.create_preference(category=event3.category)
prefs_in_db.append(preference3)

preference4 = crud.create_preference(category=event4.category)
prefs_in_db.append(preference4)

preference5 = crud.create_preference(category=event5.category)
prefs_in_db.append(preference5)


#------------------- CREATE SEARCHES and ADD TO PREFERENCES ----------------#

keyword_search1 = "social justice"
keyword_search2 = "blm"
keyword_search3 = "Biden"
keyword_search4 = "Kamala"
keyword_search5 = "Organizing"

preference6 = crud.create_preference(keyword_search=keyword_search1)
prefs_in_db.append(preference6)

preference7 = crud.create_preference(keyword_search=keyword_search2)
prefs_in_db.append(preference7)

preference8 = crud.create_preference(keyword_search=keyword_search3)
prefs_in_db.append(preference8)

preference9 = crud.create_preference(keyword_search=keyword_search4)
prefs_in_db.append(preference9)

preference10 = crud.create_preference(keyword_search=keyword_search5)
prefs_in_db.append(preference10)


#---------------- CONNECT THE EVENT A USER CREATED TO THE USER ---------------#

#loop over user objs we just created
#...and attach them to the events where user.user_id == creator_id
for user in users:
    
    crud.connect_user_to_their_event(user)
        
#---------------- "SAVE" A RANDOM EVENT TO A USER -------------------------------#

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