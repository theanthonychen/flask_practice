# Flask Practice
This is a test repository to test implementations within a basic Flask app before implementing in other projects. App is meant to be run in a virtualenv for quick testing.

### Implemented Concepts:
Web Pages
- Static web pages
- HTML pages
- Template inheritance

Flask
- Routing
- User login
- User registration

Database (SQLite3)
- Creating and reseting db file
- Storage and retrival

Flask-CAS
- RPI CAS authentication
- Equal authenticity as registered account login

## Database Set Up
Current implementation uses SQLite3. Run the provided sql.py file.
```bash
python sql.py
```

## Virtual Environment
If running app within a virtual environment, you must set up a virtual environment before running the app for the first time. Make sure you have pip before beginning.

### Installing
```bash
pip install virtualenv
```
### Set up
Build venv directory
```bash
cd flask-practice
virtualenv --no-site-packages venv
```
You now have a default virtual environment.
### Running
Activate virtual environment
```bash
source venv/bin/activate
```
(venv) should appear by username as below
```
(venv)Anthonys-Macbook-Pro:flask-intro anthonychen$
```
You are now working in the virtual environment.
### Installing Requirements
Virtual environment will not initially build with all the required dependencies. All the required dependencies are listed in requirements.txt. Pip allows for easy installation.
```bash
pip install -r requirements.txt
```
**11/25/2019 - Flask-CAS==1.0.1 still not available through pip by default. Install directly from the git repository.**
```bash
pip install git+git://github.com/cameronbwhite/Flask-CAS@master
```
Virtual Environment is now fully prepared to run app.py.
```bash
python app.py
```

## Flask
Flask code based off tutorial here: https://github.com/realpython/discover-flask

## Flask-CAS
Flask-CAS code based off example code from here: https://github.com/cameronbwhite/Flask-CAS

The module makes RPI CAS authentication straightforward. Simply set `app.config['CAS_SERVER'] = 'https://cas-auth.rpi.edu/cas'` and CAS's login and logout routes will be able to act through RPI CAS.
