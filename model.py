"""Define Model Classes"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################# MODEL DEFINITIONS ###############
#-- User can have many Events
#-- Event can have many Users

#-- User can have many Preferences 
#-- One Preference can have many Users

#-- Users can create many CreatedEvents
#-- CreatedEvent is created by one User

#-- Event can have multiple CreatedEvents
#-- CreatedEvent only has one Event 


#-- Association table between User and Event
user_events_association_table = db.Table('user_events', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.event_id'))
    )

#-- Association table between User and Preference
user_prefs_association_table = db.Table('user_prefs', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('pref_id', db.Integer, db.ForeignKey('preferences.pref_id'))
    )

class User(db.Model):
    """Data model for a user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)

    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False,
                                        unique=True)
    password = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    
    #-- list of associated events
    #-- must append an event object to link user to event 
    events = db.relationship('Event',
                            secondary=user_events_association_table,
                            backref='users')
    
    #-- list of associated preferences
    #-- must append a preference object to link user to preference
    preferences = db.relationship('Preference',
                                    secondary=user_prefs_association_table,
                                    backref='users')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Event(db.Model):
    """An event (from a source)"""
    """Has many-to-many re'lp with User"""

    __tablename__ = 'events'

    event_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    created_event_id = db.Column(db.Integer, 
                        db.ForeignKey('created_events.created_event_id')) 
    eventbrite_event_id = db.Column(db.Integer) #Event ID is returned from Eventbrite 
    mobilize_event_id = db.Column(db.Integer) #Event ID returned from Mobilize
                                            #Event ID from additional source?
    
    created_events = db.relationship ('CreatedEvent', backref='events') #on created_event_id

    def __repr__(self):
        return f'<Event event_id={self.event_id} created_event_id={self.created_event_id} eventbrite_id={self.eventbrite_event_id} mobilize_id={self.mobilize_event_id}>' 

# class UserEvent (db.Model):
#     """Glue table for User and Event""" 

#     __tablename__ = 'user_events'

#     user_events_id = db.Column(db.Integer, 
#                                 primary_key=True,
#                                 autoincrement=True,
#                                 nullable=False) 
#     event_id = db.Column(db.Integer, 
#                         db.ForeignKey('events.event_id'),
#                         nullable=False)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.user_id'),
#                         nullable=False)

    
#     def __repr__(self):
#         return f'<UserEvent user_events_id={self.user_events_id} event_id={self.event_id} user_id={self.user_id}>'

class CreatedEvent (db.Model):
    """A new event created by a user"""

    __tablename__ = 'created_events'

    created_event_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    name = db.Column(db.String)
    category = db.Column(db.String) #--> if category already exists, tag on, if not, add to category in preferences
    start_date = db.Column(db.DateTime)
    location = db.Column(db.String)
    description = db.Column(db.Text)
    image = db.Column(db.String)

    def __repr__(self):
        return f'<CreatedEvent created_event_id={self.created_event_id}, name={self.name}>'
    

class Preference(db.Model):
    """A preference = some combination of category and keyword searches 
            that users can save to their account"""

    __tablename__ = 'preferences'

    pref_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    category = db.Column(db.String, unique=True)
    keyword_search = db.Column(db.String)

    def __repr__(self): 
        return f'<Preference pref_id={self.pref_id} category={self.category} keyword={self.keyword_search}>'
    


# class UserPreference(db.Model):
#     """Glue table to connect users to their saved preferences"""

#     __tablename__ = 'user_preferences'

#     user_pref_id = db.Column(db.Integer,
#                             primary_key=True,
#                             autoincrement=True,
#                             nullable=False)
#     pref_id = db.Column(db.Integer, 
#                         db.ForeignKey('preferences.pref_id'),
#                         nullable=False)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.user_id'),
#                         nullable=False)
    
#     def __repr__(self):
#         return f'<UserPref user_pref_id={self.user_pref_id} pref_id={self.pref_id} user_id={self.user_id}>'

#connect server to db with SQLAlchemy
def connect_to_db(flask_app, db_uri='postgresql:///civic', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app
    #from flask import Flask 

    #app=Flask(__name__)
    connect_to_db(app)