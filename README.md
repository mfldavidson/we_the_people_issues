# SI507 - Final Project
### Maggie Davidson

----------
## Overall

My project will create a Flask application that:
- displays data visualizations about We the People petitions
- allows a user to find We the People petitions by issue/tag

## Focus
I want to focus on sourcing data from an API, creating a database, and visualizing data.


## Interface and Routes
- Home: /
  This page will show a list of navigation links to other routes in the application, a link to the We the People website, a disclaimer that the application is not endorsed by We the People/the White House, a description of the application, and a few "teaser" pieces of information or visualizations such as the number of public petitions collecting signatures right now

- Issues: /issues/
  This page will show a list of all of the issues (tags) that can be used for We the People petitions, how many petitions each issue is used for, and a button to click to see all petitions with that issue

- Specific Issues: /issues/`<issue name>`  
  This page will show a list of all of the petitions with the issue given in the url

- Visualizations: /viz
  This page will show data visualizations representing the petitions; specific visualizations TBD

## Specifics

#### Data
I will be relying on petitions data from the We the People API

Documentation for We the People API with example response data: https://petitions.whitehouse.gov/developers/get-code

#### Database
I expect my database schema to include 3 tables

The entities each table will represent are:
- petitions
- issues (tags)
- types

There will be a many to many relationship between petitions and issues and between petitions and types

I will be populating the database by requesting the API and loading the response in to a .sqlite database file which my Flask app will rely on and have models to describe

#### Program and Application
I am planning to use the following modules in writing my code, aside from Flask and SQLAlchemy:
> - plotly - for charting/graphing data
> - matplotlib - also for charting
> - requests_cache - for caching data I scrape

I will be defining the following functions outside of Flask routes:
> - Function 1: what will it do, what input does it take, what does it return
> - Function 2: what will it do, what input does it take, what does it return

I will be defining the following classes outside of Flask routes/models:
> - Class 1: what is it, does it inherit from anything, what does the constructor require, why and how will I use it
> - Class 2: what is it, does it inherit from anything, what does the constructor require, why and how will I use it

The assignment(s) in 507 we’ve done that are most like what I want to do are:
- Project 4 Option 1 (because I created a .sqlite database as a part of it)
- Project 3 (because of the .sqlite database integrated into a Flask application)

Other useful resources for this project for me will be:
> links or references to specific things I think will be helpful to reference, including specific lecture notes, lab examples, code examples from class, readings, or anything on the internet you’ve found useful


## Other

My biggest concerns about my work on this project are:
- making the application user-friendly and visually pleasing using HTML, JavaScript, and CSS
- data visualizations, which I haven't done before in Python

I feel confident that I can complete these parts of the project I am planning:
- retrieving data from an API
- caching data returned from the API
- creating a database and storing the data returned from the API in the database
