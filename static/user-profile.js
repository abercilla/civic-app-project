//----Remove SAVED event from user-profile and in db w/o redirecting-------//
const removeEvent = (evt) => {

    //prevent page from redirecting to events/event_id
    evt.preventDefault();
    console.log("We're in removeEvent");
    
    //get specific eventID from html button element 
    let eventID = (evt.target.id).split('-')[2]

    console.log(eventID);

    // take event_id from the event we're saving 
    //... and send to server to save event to user
    $.post({
        url: '/remove-event',
        data: eventID,
        contentType: 'application/json; charset=utf-8'
    })  
        
    // add success message to correct event Div based on dynamic div id

        .done((response) => {
            
            // console.log(response)
            // console.log(eventID)
            
            // find the div that matches ID of event button we clicked on
            let removeDiv = $('#remove-event-' + eventID);
            //console.log(successDiv);

            // print success message in Div for event
            removeDiv.remove();
        });
}

// for ANY save-event button and then ID changes according to event
$('.remove-button').on('click', removeEvent);


//----Delete a CREATED event from user-profile and in db w/o redirecting-------//
const deleteEvent = (evt) => {

    //prevent page from redirecting to events/event_id
    evt.preventDefault();
    console.log("We're in removeEvent");
    
    //get specific eventID from html button element 
    let eventID = (evt.target.id).split('-')[2]

    console.log(eventID);

    if (confirm("Are you sure you want to delete this event?")) {
        console.log("Confirmed!")

        $.post({
            url: '/delete-event',
            data: eventID,
            contentType: 'application/json; charset=utf-8'
        }) 

        .done((response) => {
            
            // console.log(response)
            // console.log(eventID)
           
            // find the div that matches ID of event button we clicked on
            let removeDiv = $('#delete-event-' + eventID);
            console.log(removeDiv);

            // print success message in Div for event
            removeDiv.remove();
        
        });


    }
    else {
        console.log("Not confirmed!")
    }
    // take event_id from the event we're saving 
    //... and send to server to save event to user
    
        
    // add success message to correct event Div based on dynamic div id

        
}

// for ANY save-event button and then ID changes according to event
$('.delete-button').on('click', deleteEvent);

//---------------Remove a Category as pref from user-----------//

const removeCategory = (evt) => {

    evt.preventDefault();
    console.log("We're in removeCat");
    
    //get specific eventID from html button element 
    let category = (evt.target.id).split('-')[2]

    let categoryJSON = JSON.stringify(category);

    console.log(category);
    console.log(categoryJSON);

    if (confirm("Are you sure you want to delete this filter?")) {

        console.log("Confirmed!");

        $.post({
            url: '/remove-category',
            data: categoryJSON,
            contentType: 'application/json; charset=utf-8'
        }) 

        .done((response) => {
            
            console.log(response);
            console.log(categoryJSON);
            console.log(category);
           
            // find the div that matches ID of event button we clicked on
            let removeItem = $('#remove-category-' + category);
            console.log(removeItem);

            // print success message in Div for event
            removeItem.remove();
        
        });
    }
    
    else {
        console.log("Not confirmed!")
    }
}


$('.remove-category').on('click', removeCategory);


//---------------Remove a Keyword as pref from user-----------//

const removeKeyword = (evt) => {

    evt.preventDefault();
    console.log("We're in removeKey");
    
    //get specific eventID from html button element 
    let keyword = (evt.target.id).split('-')[2]

    let keywordJSON = JSON.stringify(keyword);

    console.log(keyword);
    console.log(keywordJSON);

    if (confirm("Are you sure you want to delete this filter?")) {

        console.log("Confirmed!");

        $.post({
            url: '/remove-keyword',
            data: keywordJSON,
            contentType: 'application/json; charset=utf-8'
        }) 

        .done((response) => {
            
            console.log(response);
            console.log(keywordJSON);
            console.log(keyword);
           
            // find the div that matches ID of event button we clicked on
            let removeItem = $('#remove-keyword-' + keyword);
            console.log(removeItem);

            // print success message in Div for event
            removeItem.remove();
        
        });
    }
    
    else {
        console.log("Not confirmed!")
    }
}

$('.remove-keyword').on('click', removeKeyword);
