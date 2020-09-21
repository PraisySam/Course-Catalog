
# Course Catalog Dashboard
Web page to browse, search and filter through a database of courses.

Course dashboard API using Python Flask, SQL Alchemy and Marshmallow 

## Start With Pipenv

```python

# Activate virtual Environment 
$ pipenv shell
(or create a virtual env)
# Install dependencies
$ pipenv install

# Run Server (http://localhst:5000)
python app.py

```

## Functions
A person can Upload a Course.

Filter through courses with category(Computer,Mathematics,Engineering) as a parameter.

Serach through courses with title, instructor as search parameter.

## API Call
Local Host

http://127.0.0.1:5000

Upload a Course

http://127.0.0.1:5000/uploadCourse 

View all the Courses(JSON format)

http://127.0.0.1:5000/all_courses

View all the category(JSON format)

http://127.0.0.1:5000/all_category

