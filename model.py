"""Define Model Classes"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Data model for a user."""

    __tablename__ = 'users'

    user_id = db.Columm(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        nullable=False)

    fname = db.Column(db.String(25), nullable=False)
    lname = db.Colummn(db.String(25), nullable=False)
    email = db.Collumn(db.String(100), nullable=False,
                                        unique=True)
    password = db.Column(db.String)
    zipcode = db.Column(db.Integer) #do I need anything else here?

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Event(db.Model):
    """Data model for an event (from a source)"""
    """Has many-to-many re'lp with User"""

    __tablename__ = 'events'

    search_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        nullable=False)
    event_id = db.Column(db.Integer, 
                        db.ForeignKey('created_events.event_id'),
                        nullable=False) #record for this field will be "NULL" unless this is specificied I think
    eventbrite_event_id = db.Column(db.Integer) #Do I need something else specifiied here if it's coming from an API? 
    mobilize_event_id = db.Column(db.Integer) #ID from Mobilize API?


    users = db.relationship ('User', secondary = "users_events", backref='users')

    def __repr__(self):
        return f'<Event search_id={self.search_id} event_id={self.event_id} 
                eventbrite={self.eventbrite_event_id}
                mobilize={self.mobilize_event_id}>' 

class UserEvent (db.Model):
    """Glue table for User and Event"""

    __tablename__ = 'user_events'

    user_events_id = db.Column(db.Integer, 
                                primary_key=True,
                                autoincrement=True,
                                nullable=False) #when do we add nullable vs not?
    event_id = db.Column(db.Integer, 
                        db.ForeignKey('created_events.event_id'),
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    def __repr__(self):
        return f'<UserEvent user_events_id={self.user_events_id},
                event_id={self.event_id} user_id={self.user_id}>'

class CreatedEvent (db.Model):
    """A new event created by a user"""

    __tablename__ = 'created_events'

    event_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    event_name = db.Column(db.String)
    event_category = 
    start_date = db.Column(db.dateTime)
    location = db.Column(db.String)
    event_description = db.Column(db.Text)
    image = db.Column(db.String) #just added this

    def __repr__(self):
        return f'<CreatedEvent event_id={self.event_id} name={self.event_name}>'
    

