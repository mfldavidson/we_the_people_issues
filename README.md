# We the People Petitions by Issue Application

Maggie Davidson

[We the People Petitions GitHub Repository](https://github.com/mfldavidson/si507_finalproj)

---

## Project Description

This program runs a Flask application that retrieves [We the People petitions](https://petitions.whitehouse.gov/) data and allows the user to explore the petitions by the issues each petition is tagged with, which is currently not possible on the We the People site.

## How to run

1. Fork the repository
2. Clone the repository to your computer by entering `git clone https://github.com/mfldavidson/si507_finalproj.git` in the command line
3. Create a virtual environment in a location that you want it by entering `python3 -m venv [the name you want to give the environment]` in the command line
4. Activate the virtual environment by entering `source the name you gave the environment]/bin/activate` in the command line (before you navigate away)
5. Navigate back to the repo folder and install all requirements in the virtual environment by entering `pip install -r requirements.txt` in the command line
6. Feel free to either use the sample data provided in `petitions.db` and `petitions_cache.json` or delete these files to retrieve new data and create a new database
7. Enter `python si507project.py runserver` in the command line; if running without a cache and/or db file or with a cache file that is more than 7 days old, it may take a bit for the program to be fully ready while it retrieves the data

## How to use

1. Need to write

## Routes in this application
- `/` This page will show a list of navigation links to other routes in the application, a link to the We the People website, a disclaimer that the application is not endorsed by We the People/the White House, a description of the application, and a few "teaser" pieces of information or visualizations such as the number of public petitions collecting signatures right now

- `/issues/` This page will show a list of all of the issues (tags) that can be used for We the People petitions, how many petitions each issue is used for, and a button to click to see all petitions with that issue

- `/issues/<issue id>` This page will show a list of all of the petitions with the issue given in the url

- `/viz` This page will show data visualizations representing the petitions; specific visualizations TBD

## How to run tests
1. Need to write

## In this repository:
- `si507project.py` is the main program file
- `si507project_tools.py` contains app configurations and class and function definitions
- `advanced_expiry_caching.py` contains tools for handling caching of data returned by the API
- `si507project_tests.py` contains tests
- `SI507 Final Project ERD.png` contains an entity-relationship diagram of the database `petitions.db`
- `petitions_cache.json` sample data from the API
- `petitions.db` sample database with data from the API
- `templates/`
  - `index.html` HTML template for the homepage
  - `issues.html` HTML template for the `/issues/` route
  - `specific_issue.html` HTML template for the `/issues/<issue id>` route
  - additional HTML files to be added for other routes

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
- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [x] Use of a new module
- [ ] Use of a second new module
- [x] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [x] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application
- [x] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [ ] Sourcing of data using web scraping
- [x] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
