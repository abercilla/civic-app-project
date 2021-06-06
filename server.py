"""Server with all routes"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "DEV" #need to change this and add to secrets.sh
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Return homepage"""
    #if user has already signed in, redirect to feed
    #if not, prompt them to create an account and show unfiltered list of events

    # if 'name' in session:
    #     return redirect("/feed")
    # else:
    #     return 
    return render_template('homepage.html')

@app.route('/create-account', methods=['POST'])
def create_account():
    """Create account for user"""

    session['fname'] = request.form.get('fname')
    
    return render_template('/feed')


if __name__ == "__main__":
    
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)