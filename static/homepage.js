'use strict';

// separate JS files for each HTML page and then add in script tag to that HTML page

alert("js is connected!");

// function FilterHomepage(evt){
//     alert("We clicked on Search by My Filters!")
//         };

//when button is clicked, call FilterHomepage function



// DISPLAY RELEVANT EVENTS
// events that fit the current user's saved preferences will be returned as (data) from get request
//... and we'll append each event to list element <li>

let url = "/saved-filter.json";
let i = 0;

$('#saved_filters').on('click', (evt) => {
    evt.preventDefault();
    console.log("On submit is working!")
    $.get(url, (data) => {
        $('#event-list').empty();
        let events = data;
        for (const event of events) {
            console.log(events[i]["event_id"]);
            const eventAdd = "<li><a href = 'events/" + events[i]["event_id"] + "'>" + events[i]["name"] + "</a></li>";
            $('#event-list').append(eventAdd);
            i = i + 1;
        }     
    })
});


//-------
// Make user's search criteria STICKY
//this will listen for all checkboxes on homepage.html
// var i is a number of checkboxes
var j, boxes = document.querySelectorAll('input[type="checkbox"]');
//var keyword = document.querySelectorAll('input[type="text"]');

//create items in localStorage to store user's input 
function save() {
    //loop over all the checkboxes 
    for (j = 0; j < boxes.length; j++) {
        //create dict in localStorage where {key = 'category': value = 'true/false'}
        localStorage.setItem(boxes[j].value, boxes[j].checked); 
    }
    //create dict in localStorage where {key = 'keyword': value= user input}
    //localStorage.setItem(keyword, keyword.value);
}

//load what the user entered on the page from localStorage 
function load_() {
    //loop over checkboxes again to check for values 
    for (j = 0; j < boxes.length; j++) {
        //set the dict value for boxes to whether or not they're checked (??) 
        // snippet from: https://jsfiddle.net/sQuEy/4/
        boxes[j].checked = localStorage.getItem(boxes[j].value) === 'true' ? true:false;
    }
    //keep keyword textbox entered on page
    //fill in whatever keyword is stored in localStorage 
    //localStorage.getItem(keyword.value === 
}

//clear filters via localStorage
const clear = () => {
    localStorage.clear();
    location.reload();
}

// Allow user to save search criteria as a filter/pref
const saveUserFilter = (evt) => {
    evt.preventDefault();
    //turn what's saved in localstorage into usable
    let formData = JSON.stringify(localStorage);
    console.log(formData);
    console.log(typeof(formData));

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
$('#clear-button').on("click", clear);
$(document).ready(load_());

