# Study Map
Study Map is a social study tracking application built for Swarthmore College. Its goals are to coordinate study sessions among groups of students as well as give students an interactive map of study spaces on campus.

[See the wiki for more](https://github.swarthmore.edu/cs71-s19/project-echen1-kkakkar1-xluo1-yzhang1/wiki)

# Obtaining the source

How to get the source:
1. git clone the repository

# How to build
* The instructions are taken from this tutorial:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
* Before you start to build, make sure you have Python3 installed.

**The follow instructions assume Linux System.**
1. Inside the terminal, create a directory for the project.
2. Inside of the project directory, create a virtual environment (here called "venv"). This is to ensure all the dependencies are contained and consistent within the project directory. (The $ symbol denotes the terminal and the command should be run in the terminal.)
    ```
      $ python3 -m venv venv
    ```
3. Each time you want to interact with the project, activate the virtual environment:
    ```
      $ source venv/bin/activate
      (venv) $ _
    ```
4. Install necessary packages in the virtual environment using our setup.sh script:
    ```
      chmod +x setup.sh
      ./setup.sh
    ```
    * flask: the framework for Python we use to develop the web application
    * flask-wtf: a flask extension that is a wrapper for the WTForms package that handles web forms
    * flask-sqlalchemy: an ORM (object relational mapper) that lets you interact with databases using high level constructs like classes and methods
    * flask-bootstrap: a flask extension that provides basic Bootstrap CSS functionality
    * flask-migrate: a flask extension that manages database migration
    * python-dotenv: allows environment variables to be automatically set
    * flask-login: a flask extension that manages user login states
    * flask-moment: a flask extension that incorporates the javascript library moment.js; it takes care of date and time rendering
    * pandas: manages reading and importing csv to database
    
# How to run

1. Activate the virtual environment and run Flask:
    ```
      $ source venv/bin/activate
      (venv) $ flask run
    ```
# Testing 

1. To run our unit tests, just run the following:
    ```
      $ python tests.py
    ```
 
