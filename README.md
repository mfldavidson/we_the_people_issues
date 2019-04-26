# We the People Petitions by Issue Application

Maggie Davidson

[We the People Petitions GitHub Repository](https://github.com/mfldavidson/si507_finalproj)

---

## Project Description

This program runs a Flask application that retrieves [We the People petitions](https://petitions.whitehouse.gov/) data and allows the user to explore the petitions by the issues each petition is tagged with, which is currently not possible on the We the People site. The program uses Python Anaconda, Flask, SQLAlchemy, Plotly, Flask Tables, a local database, a JSON cache file to cache data returned by the API, Jinja2 templates, and [DataTables](https://datatables.net/). A diagram showing the structure of the DB can be found [here](https://github.com/mfldavidson/si507_finalproj/blob/master/static/SI507%20Final%20Project%20ERD.png).

A note about the Plotly plots: I created online plots with Plotly using my Python program, but then commented out the code used to make the plots and embed them in the template. I did this because, in order for graders of this assignment to run the code to create/update the plots, they would have to create a Plotly credentials file with my credentials on their own computers. Thus, I left the code (commented out) so it can be seen and used in the future, but removed my credentials and "hard coded" the iframe HTML on the viz route.

When running properly, the homepage should look like this:
![A picture of the homepage of the We the People Petitions by Issue Application](https://github.com/mfldavidson/si507_finalproj/blob/master/static/index-shot.png?raw=true)

When running properly, the issues route (accessed by header link "Petitions by Issue") should look like this:
![A picture of the issues route of the We the People Petitions by Issue Application](https://github.com/mfldavidson/si507_finalproj/blob/master/static/issues-shot.png?raw=true)

When running properly, the specific issue route (accessed by clicking on an issue on the Issues page as shown above) should look like this:
![A picture of the Budget and Taxes Petitions issues route of the We the People Petitions by Issue Application](https://github.com/mfldavidson/si507_finalproj/blob/master/static/spec-issue-shot.png?raw=true)

When running properly, the visualizations route should look like this:
![A picture of the visualizations route of the We the People Petitions by Issue Application](https://github.com/mfldavidson/si507_finalproj/blob/master/static/viz-shot.png?raw=true)

## How to run

1. Fork the repository
2. Clone the repository to your computer by entering `git clone https://github.com/mfldavidson/si507_finalproj.git` in the command line
3. Create a virtual environment in a location that you want it by entering `python3 -m venv [the name you want to give the environment]` in the command line
4. Activate the virtual environment by entering `source the name you gave the environment]/bin/activate` in the command line (before you navigate away)
5. Navigate back to the repo folder and install all requirements in the virtual environment by entering `pip install -r requirements.txt` in the command line
6. Feel free to either use the sample data provided in `petitions.db` and `petitions_cache.json` or delete these files to retrieve new data and create a new database
7. Enter `python si507project.py runserver` in the command line; if running without a cache and/or db file or with a cache file that is more than 7 days old, it may take a bit for the program to be fully ready while it retrieves the data

## How to use

1. Navigate in your browser to `localhost:5000` where you will find the app running. You are welcome to do whatever you want in the app, but here are some suggestions so that you can understand what the app is capable of.
2. Sort the contents of the "Petitions Awaiting Response Over 90 Days After Deadline" by in turn clicking on the column headers. Notice that it will appropriately sort the petitions based on the type of data in the column (text, date, integer).
3. Change the number of entries being shown by clicking "Show 10 entries" and change it to another number. Notice how the number of petitions being shown in the table changes, and the number at the base of the table in "Showing x to x of x entries" changes.
4. Use the "Previous", "Next", and page number buttons at the bottom right of the table to navigate through the pages of the table.
5. Use the search bar at the top right of the table and enter "Pai". Notice that one petition is returned, "We the People Call for the Resignation of FCC Chairman Ajit Varadaraj Pai".
6. Click "Petitions by Issue" in the header, then select one of the issues (try "Civil Rights & Equality") shown to see all petitions tagged with that issue.
7. Interact with the petition tables in the same ways as #2-4 above. Try the search on Civil Rights & Equality petitions by entering the word "impeach".
8. Click "Petition Visualizations" in the header. Interact with the second graph by double-clicking on one of the issues at the right to isolate it, then click each issue in turn to add it back.

## Routes in this application
- `/` This page explains what the app is and where the data comes from, gives a brief overview of the We the People petitions site, and tells the user how many petitions have been submitted ever, the petition with the most signatures, the difference in signature counts between the first and second rated petitions by signatures, and displays a table showing petitions that have been awaiting a response from the White House for more than 90 days

- `/issues/` This page shows a list of all of the issues (tags) that can be used for We the People petitions with a link to see all petitions tagged with that issue

- `/issues/<issue id>` This page shows two tables, one with petitions that can be signed right now, and one with petitions that are closed for signing, tagged with the issue given in the URL

- `/viz` This page shows two data visualizations, one charting the count of all petitions submitted in each month over the course of the We the People site, and the other charting the count of petitions by issue tag submitted in each month over the course of the We the People site

## How to run tests
1. The 8 tests will check whether your database was properly created and populated as well as the splitPetitionsBySignable function
2. To run the tests, enter `python SI507project_tests.py` in your command line
3. In the command line, you will see the results of the tests

## In this repository:
- `si507project.py` is the main program file
- `si507project_tools.py` contains app configurations and class and function definitions
- `advanced_expiry_caching.py` contains tools for handling caching of data returned by the API
- `si507project_tests.py` contains tests
- `SI507 Final Project ERD.png` contains an entity-relationship diagram of the database `petitions.db`
- `petitions_cache.json` sample data from the API
- `petitions.db` sample database with data from the API
- `requirements.txt` to install all required modules in a virtualenv
- `.gitignore` to tell git to ignore and not track certain files
- `templates/`
  - `index.html` HTML template for the homepage
  - `issues.html` HTML template for the `/issues/` route
  - `specific_issue.html` HTML template for the `/issues/<issue id>` route
  - `viz.html` HTML template for the `/viz/` route
- `static/`
  - `styles.css` CSS file imported to each template to style HTML
  - `SI507 Final Project ERD.png` contains an entity-relationship diagram of the database `petitions.db`
  - several .png and .gif files with screenshots and screen recordings demonstrating expected functioning of the app

---
## Code Requirements for Grading

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [x] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [x] Use of a new module
- [x] Use of a second new module
- [x] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [x] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application
- [x] Templating in your Flask application
- [x] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [ ] Sourcing of data using web scraping
- [x] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [x] I included a summary of my project and how I thought it went **in my Canvas submission**!
