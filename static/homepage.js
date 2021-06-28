'use strict';

// separate JS files for each HTML page and then add in script tag to that HTML page

alert("js is connected!");

// function FilterHomepage(evt){
//     alert("We clicked on Search by My Filters!")
//         };

//when button is clicked, call FilterHomepage function



//----------- DISPLAY EVENTS FROM "SEARCH BY MY FILTERS" --------------------//
// events that fit the current user's saved preferences will be returned as (data) from get request
//... and we'll append each event to list element <li>

function filterHomepage (evt) {

    let url = "/saved-filter.json";
    let i = 0;

        evt.preventDefault();
        console.log("On submit is working!")

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
                    console.log(events[i]["event_id"]);
                    const eventAdd = "<li><a href = 'events/" + events[i]["event_id"] + "'>" + events[i]["name"] + "</a></li>";
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


const clear = () => {
    // clear filters via localStorage
    localStorage.clear();
    //reload page so all events show up again
    window.location.href = "/";
}

// Allow user to save search criteria as a filter/pref
// -- BUG -- if you click "Apply Filters" again and there is nothing applied, still shows 0 events
// --- must click 'Clear Filters' to get al events again



// Save Filter and Clear Filter should only be visible if
    //.... a filter has already been applied with Apply Filter

//if localStorage has been set, show Save Filter and Clear Filter
//if there IS a keyword OR if there IS a checked box (i.e. is "true")
if ((localStorage.getItem('keyword') != null)  || (localStorage.getItem(boxes.value) == "true")) {
    console.log("We're in if statement");
    console.log(localStorage.getItem('keyword'));
    console.log(localStorage.getItem(boxes.value));
    $('#save_to_prefs').show();
    $('#clear-button').show();
} 







const saveUserFilter = (evt) => {
    evt.preventDefault();
    //turn what's saved in localstorage into usable dict for server side
    let formData = JSON.stringify(localStorage);
    //console.log(formData);
    //console.log(typeof(formData));
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



    

    
// //if filters have been applied, THEN allow user to save filters
// if (localStorage.length !== 0) {
//     
// }
// else {
//     $('#save_to_prefs').on("click", () => {
//         alert("You must apply a filter before you can save it!");
//     });
// }

$('#save_to_prefs').on("click", saveUserFilter);

//when "Clear Filter" is clicked
$('#clear-button').on("click", clear);

//when redirected back to homepage, clear localStorage
//window.localStorage.clear();

$(document).ready(load_());

//-------------- Save event and tell user without redirecting ----------//

const saveEvent = (evt) => {

    //prevent page from redirecting to events/event_id
    evt.preventDefault();
    //console.log("We're in saveEvent");
    
    //get specific eventID from html button element 
    let eventID = (evt.target.id).split('-')[2]

    //console.log(eventID);

    // take event_id from the event we're saving 
    //... and send to server to save event to user
    $.post({
        url: '/save-event',
        data: eventID,
        contentType: 'application/json; charset=utf-8'
    })  
        
    // add success message to correct event Div based on dynamic div id

        .done((response) => {
            
            // console.log(response)
            // console.log(eventID)
            
            // find the div that matches ID of event button we clicked on
            let successDiv = $('#success-msg-' + eventID);
            //console.log(successDiv);

            // print success message in Div for event
            successDiv.html('**** Event successfully saved! ****');
        });
}

// for ANY save-event button and then ID changes according to event
$('.save-button').on('click', saveEvent);







