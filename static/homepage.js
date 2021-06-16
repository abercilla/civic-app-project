'use strict';

// separate JS files for each HTML page and then add in script tag to that HTML page

alert("js is connected!");

// function FilterHomepage(evt){
//     alert("We clicked on Search by My Filters!")
//         };

//when button is clicked, call FilterHomepage function



//----------- DISPLAY RELEVANT EVENTS --------------------//
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
            for (const event of events) {
                console.log(events[i]["event_id"]);
                const eventAdd = "<li><a href = 'events/" + events[i]["event_id"] + "'>" + events[i]["name"] + "</a></li>";
                $('#event-list').append(eventAdd);
                i = i + 1;
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
        boxes[j].checked = localStorage.getItem(boxes[j].value) === 'true' ? true:false;
    }
}

// clear filters via localStorage
// BUG --- Clear Filters should remove filters and have all events show up again
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
//when "Apply Filters" is clicked
$('#save_to_prefs').on("click", saveUserFilter);

//when "Clear Filter" is clicked
$('#clear-button').on("click", clear);

$(document).ready(load_());

