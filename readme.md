# About Civic App 
(Version 1 - July 2021)

The Civic App is based on an idea a friend and I had after the 2016 election when people were angry but didn't know how to direct their energy (including us). We hypothesized that if people had a centralized place to find events related to issues they were passionate about, people would take action, and on a regular basis. 

I built this app on my own over two 2-week sprints at the end of the Hackbright program.

Note: [Mobilize](https://www.mobilize.us/) created a version of this that was widely used by established organizations during the 2018 election cycle, and I drew a lot of inspiration from their website for this project!

# Tech Stack
Python, JavaScript(AJAX, JQuery), PostgreSQL, Flask, SQLAlchemy, HTML, CSS, Bootstrap

# APIs
Google Maps

# Features
I designed the functionality of this app to allow users to search for and save events as well as save their search criteria as a filter. 

## Create An Account
![create-account](https://user-images.githubusercontent.com/69096063/124669714-b3888b00-de67-11eb-8cd2-054893a3bf37.gif)

Anyone can browse events, but in order to save events and filters, users need to create an account. During this process, they can choose any event categories they're interested in and they will be saved to their account as a Filter.

## Apply Search Criteria 
![apply filter](https://user-images.githubusercontent.com/69096063/124665892-25f66c80-de62-11eb-944b-c9828fa146eb.gif)

Users can enter a search term and/or category and my CRUD function will return any events that match either the search term OR category in event name or description. The filter will "stick" after applied so the user can then save it to their account. 

## Save Filter
![save-filter](https://user-images.githubusercontent.com/69096063/124666390-d2d0e980-de62-11eb-8b96-b245808de3c8.gif)

Users can then click Save Filter to save the search terms and/or categories to their account. This will add to their existing list of saved categories they chose when creating an account. 

Clear Filter empties the applied filter and reverts the page back to the full list of events.

## Edit Filters
![ezgif com-gif-maker](https://user-images.githubusercontent.com/69096063/124664226-fcd4dc80-de5f-11eb-946f-9a5945a67b0a.gif)

I wanted users to have a lot of control over the search words and categories they save as a filter. On the user's profile page, they can view and remove individual search words and/or categories from their filter. The item will be removed in real time on the profile page with JavaScript. 

## Search by My Filters
![search-by-my-filters](https://user-images.githubusercontent.com/69096063/124668162-4e339a80-de65-11eb-96ad-3395c6405931.gif)

Once a user has saved filters, they can click Search by My Filters instead of reapplying all of their preferred search criteria and see the most relevant events to them. 

## Save Event 
![save-events-homepage](https://user-images.githubusercontent.com/69096063/124665144-3528ea80-de61-11eb-9311-ae5902c42b6b.gif)

Users can save events directly on the homepage. They will get a confirmation message within the event box once the event is successfully saved on the backend. 

## View and Remove Saved / Created Events
![remove-event](https://user-images.githubusercontent.com/69096063/124669096-b040cf80-de66-11eb-9566-cb91c25f1f1e.gif)

On the user's profile page, they can view all events they have saved and created. Removing an event disconnects the user from the event, and deleting a created event removes the event from the app completely. 

## Plans for Version 2

- Implementing Google Maps Direction API for a Search For Events Near Me feature
- Allowing user to create and name multiple filters as Views
