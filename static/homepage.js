'use strict';

// separate JS files for each HTML page and then add in script tag to that HTML page

alert("js is connected!");

// function FilterHomepage(evt){
//     alert("We clicked on Search by My Filters!")
//         };

//when button is clicked, call FilterHomepage function



//use this, data returned from get request will be in data and we'll append each one to list
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




//define function to add an item to existing list
// function addItem(evt){
//     list.append('<li>Item</li>'); //list item from homepage.html 


// }