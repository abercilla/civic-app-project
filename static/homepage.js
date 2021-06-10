'use strict';

// separate JS files for each HTML page and then add in script tag to that HTML page

//Login button 

const login_button = $('#login-button');

//Log a user out 
function Logout(evt){
    if (button.html('Log In')) {
        button.on('click', () => {
            //if user_id in session, button should read 'Logout'
            //when button is clicked, user should be logged out

            button.html('Log Out');
        });
    }
}

