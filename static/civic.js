'use strict';

how do we connect this to the right html file???
separate JS files for each HTML page and then add in script tag to that HTML page

//Login button 

const button = $('#login-button');

//define function to 'Log Out' if btuton reads 'Log In'
function Logout(evt){
    if (button.html('Log Out')) {
        button.on('click', () => {
            button.html('Log In');
        });
    }
}

