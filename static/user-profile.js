const removeEvent = (evt) => {

    //prevent page from redirecting to events/event_id
    evt.preventDefault();
    console.log("We're in removeEvent");
    
    //get specific eventID from html button element 
    let eventID = (evt.target.id).split('-')[2]

    // console.log(eventID);

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
