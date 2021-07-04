'use strict';

//----------- DISPLAY EVENTS FROM "SEARCH BY MY FILTERS" --------------------//

// events that fit the current user's saved preferences will be returned as (data) from get request
//... and we'll append each event to list element <li>

function filterHomepage (evt) {

    let url = "/saved-filter.json";
    let i = 0;

        evt.preventDefault();
        console.log("On submit is working!")
        clear;

        $.get(url, (data) => {
            $('#event-list').empty();
            let events = data;
            //console.log(events)
            //figure out the size of the JSON obj
            const objSize = Object(events).length;
            //console.log(objSize);
            // if the JSON obj size is 0 (i.e. dict is empty / no events were found based on user's prefs)
            if (objSize < 1) {
                //console.log("No Events Found")
                const errorMsg = "<p>No Events Found</p>"
                $('#event-list').append(errorMsg);
            } 
            else {
                for (const event of events) {
                    console.log(event);
                    console.log(events[i]["event_id"]);
                    
                
                    let eventID = events[i]["event_id"];
                    console.log(typeof(eventID));

                    const saveEventButton = "<button type = 'submit' class = 'save-button' name = 'button' id ='save-event-" + eventID + "'>Save Event</button>"

                    const eventAdd = "<div class= 'success-msg' id ='success-msg-" + eventID + 
                                        "'><h3>" + events[i]['name'] + "</h3><p>" + events[i]['category'] + "</p><p>" + events[i]['start_date'] + 
                                        "</p><img src='" + events[i]['image'] + "' width='300' onerror='this.onerror=null; this.remove();'><p>" + 
                                        events[i]['address'] + "</p><p>" + events[i]['description'] + "</p>" + 
                                        "<span class = 'buttons'><form action='/events/" + eventID + "' method='POST'>" +
                                        saveEventButton +
                                        "</form><br><form action='events/" + eventID + "'>" + 
                                        "<button>See Event Details</button></form></span><br><br><br></div>";

                    //how can we get it to save on the page again with this new behavior instead of redirecting
                    //are we clicking on this in JS instead of HTML on the page, and if so, how can we add a listener to the JS itself to then reference anther JS function

                    console.log(eventAdd);
                    
                    $('#event-list').append(eventAdd);



                    i = i + 1;
                }  
            }   
        });
}

$('#saved_filters').on('click', filterHomepage);




// --------------Make user's search criteria STICKY----------//

//this will listen for all checkboxes on homepage.html
// var i is a number of checkboxes
var j, boxes = document.querySelectorAll('input[type="checkbox"]');
//grab input from any text box from this file
var keyword = document.querySelector('#keyword');

//create dict items in localStorage to store user's input 
function save() {
    
    //grab what user entered in search box and store in localStorage 
    //...as {key = 'keyword': value = keyword.value}
    localStorage.setItem('keyword', keyword.value);
    
    //loop over all the checkboxes 
    for (j = 0; j < boxes.length; j++) {
        //create dict in localStorage where {key = 'category': value = 'true/false'}
        localStorage.setItem(boxes[j].value, boxes[j].checked); 
        
    } 
}

//load what the user entered on the page from localStorage 
function load_() {
    
    //refill the HTML element with what was stored in localStorage
    keyword.value = localStorage.getItem('keyword');

    //loop over checkboxes again to check for values
    for (j = 0; j < boxes.length; j++) {
        //set the dict value for boxes to whether or not they're checked (??) 
        // snippet from: https://jsfiddle.net/sQuEy/4/
        // === is the value 'true', if not, put false
        boxes[j].checked = localStorage.getItem(boxes[j].value) === 'true' ? true:false;
    }
}

//-------------------- Clear LocalStorage --------------------------------//

const clear = () => {
    // clear filters via localStorage
    localStorage.clear();
    //reload page so all events show up again
    window.location.href = "/";
}

//when "Clear Filter" is clicked
$('#clear-button').on("click", clear);


//if localStorage has been set, show Save Filter and Clear Filter
//if there IS a keyword OR if there IS a checked box (i.e. is "true")
if ((localStorage.getItem('keyword') != null)  || (localStorage.getItem(boxes.value) == "true")) {
    console.log("We're in if statement");
    console.log(localStorage.getItem('keyword'));
    console.log(localStorage.getItem(boxes.value)); // this console.logs "null" but somehow still works
    $('#save_to_prefs').show();
    $('#clear-button').show();
} 

//Filters should stick as long as we are still on homepage
//once all DOM objects are loaded, repopulate localStorage in search filters
$(document).ready(load_());
//console.log(localStorage);

//------------Only show Save Filter and Clear Filter after Apply Filter is clicked-----//

//if localStorage has been set, show Save Filter and Clear Filter
//if there IS a keyword OR if there IS a checked box (i.e. is "true")
// if ((localStorage.getItem('keyword') != null)  || (localStorage.getItem(boxes.value) == "true")) {
//     console.log("We're in if statement");
//     console.log(localStorage.getItem('keyword'));
//     console.log(localStorage.getItem(boxes.value));
//     $('#save_to_prefs').show();
//     $('#clear-button').show();
// } 



//-------------------Save whatever is in localStorage as prefs for user ---------------//

const saveUserFilter = (evt) => {
    evt.preventDefault();
    //turn what's saved in localstorage into usable dict for server side
    let formData = JSON.stringify(localStorage);
    console.log(formData);
    console.log(typeof(formData));
    alert("Filter saved to user's account!")
    
    //send data to a Flask route
    $.post({
        url: '/save-filter',
        data: formData,
        contentType: 'application/json; charset=utf-8'
    })
        .done((response) => {
            console.log(response)
        });
}


$('#save_to_prefs').on("click", saveUserFilter);

//-------------- Save event and tell user without redirecting ----------//

const saveEvent = (evt) => {

    //prevent page from redirecting to events/event_id
    evt.preventDefault();
    console.log("We're in saveEvent");
    
    //get specific eventID from html button element 
    let eventID = (evt.target.id).split('-')[2]

    console.log(eventID);

    // take event_id from the event we're saving 
    //... and send to server to save event to user
    $.post({
        url: '/save-event',
        data: eventID,
        contentType: 'application/json; charset=utf-8'
    })  
        
    // add success message to correct event Div based on dynamic div id

        .done((response) => {
            
            console.log(response)
            // console.log(eventID)
            
            // find the div that matches ID of event button we clicked on
            let successDiv = $('#success-msg-' + eventID);
            console.log(successDiv);

            // print success message in Div for event
            // -- TO DO --  make this a temporary message and change Save Event button to "Saved"
            // successDiv.prepend("<p id='success-message'>**** Event successfully saved! ****</p>");
            successDiv.prepend("<div class='alert alert-primary' role='alert'>Event successfully saved!</div>");
        });
}

// deprecated: for events preloaded on page via HTML 
//$('.save-button').on('click', saveEvent);

//if any button on the save-button class is clicked... 
//...(including dynicamlly created events via "Search by My Filters"), do saveEvent
$(document).on('click', '.save-button', saveEvent); 

//$('#saved_filters').on('click', localStorage.clear());



// --TO FIX-- 
// If we leave homepage and come back, filters should clear via localStorage
// currently this messes with the Save Filter feature

// $(document).ready(function() {
//     let previousURL = document.referrer;
//     console.log(previousURL);
//     console.log(localStorage);
//     if (previousURL !== "/") {
//         localStorage.clear();
//     }
// });


