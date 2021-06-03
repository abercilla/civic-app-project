"""Define Model Classes"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Event(db.Model):
    """Data model for an event (from a source)"""
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

class UserEvent (db.Model):
    """Glue table for User and Event""" 

    __tablename__ = 'user_events'

    user_events_id = db.Column(db.Integer, 
                                primary_key=True,
                                autoincrement=True,
                                nullable=False) 
    event_id = db.Column(db.Integer, 
                        db.ForeignKey('events.event_id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    
    def __repr__(self):
        return f'<UserEvent user_events_id={self.user_events_id} event_id={self.event_id} user_id={self.user_id}>'

class CreatedEvent (db.Model):
    """A new event created by a user"""

    __tablename__ = 'created_events'

    created_event_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    event_name = db.Column(db.String)
    event_category = db.Column(db.String) #--> if event_category already exists, tag on, if not, add to event_category in preferences
    start_date = db.Column(db.DateTime)
    location = db.Column(db.String)
    event_description = db.Column(db.Text)
    image = db.Column(db.String)

    def __repr__(self):
        return f'<CreatedEvent created_event_id={self.event_id}, event_name={self.event_name}>'
    

class Preference(db.Model):
    """A preference = some combination of category and keyword searches 
            that users can save to their account"""

    __tablename__ = 'preferences'

    pref_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    event_category = db.Column(db.String, unique=True)
    keyword_search = db.Column(db.String)

    
    def __repr__(self): 
        return f'<Preference pref_id={self.pref_id} category={self.event_category} keyword={self.keyword_search}>'
    
    

class UserPreference(db.Model):
    """Glue table to connect users to their saved preferences"""

    __tablename__ = 'user_preferences'

    user_pref_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            nullable=False)
    pref_id = db.Column(db.Integer, 
                        db.ForeignKey('preferences.pref_id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    
    def __repr__(self):
        return f'<UserPref user_pref_id={self.user_pref_id} pref_id={self.pref_id} user_id={self.user_id}>'


def connect_to_db(flask_app, db_uri='postgresql:///civic', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from flask import Flask

    app=Flask(__name__)
    connect_to_db(app)