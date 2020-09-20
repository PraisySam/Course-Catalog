from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
from flask import url_for, redirect, render_template, request, send_from_directory
from flask_wtf import FlaskForm 
from sqlalchemy import or_
from wtforms_sqlalchemy.fields import QuerySelectField


app = Flask(__name__)
app.static_folder = 'static'

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Course Class/Model
class Courses(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), unique=True)
  instructor = db.Column(db.String)
  category = db.Column(db.String)
  description = db.Column(db.String)
  filename = db.Column(db.String)
  type = db.Column(db.String)
  startDate = db.Column(db.Integer)
  endDate = db.Column(db.Integer)


  def __init__(self, title, instructor, category, description, filename, type, startDate, endDate):
    self.title = title
    self.description = description
    self.category = category
    self.instructor = instructor
    self.filename = filename
    self.type = type
    self.startDate = startDate
    self.endDate = endDate

# Product Schema
class CourseSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'description', 'instructor','category', 'filename','type','startDate','endDate')

# Init schema
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

#Upload course 
@app.route('/uploadCourse')
def uploadCourse():
  return render_template("upload.html")

  
@app.route('/', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page):
    page = page
    pages = 5
    courses = Courses.query.order_by(Courses.id.asc()).paginate(page,pages,error_out=False)
  
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       courses = Courses.query.filter(or_(Courses.title.like(search), Courses.category.like(search))).paginate(per_page=pages, error_out=True)      
       return render_template('index.html', courses=courses, tag=tag)
    return render_template('index.html', courses=courses)
 
# Get All Courses
@app.route('/Computer', methods=['GET'] , defaults={"page": 1})
def get_courses(page):
   page = page
   pages = 5
   courses = Courses.query.order_by(Courses.category == 'Maths').paginate(page,pages,error_out=False)  
   
   if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       courses = Courses.query.filter(Courses.title.like(search)).paginate(per_page=pages, error_out=True)      
       return render_template('Category.html', courses=courses, tag=tag)
   return render_template('Category.html', courses=courses)
   


# Get Single Products
@app.route('/all_courses/<id>', methods=['GET']) 
def get_course(id):
  course = Courses.query.get(id)
  return render_template('course.html', title="Course(ID)" ,  course = course )

# upload a course

@app.route("/upload", methods=["POST"])
def upload():
    print("Praisy:"+str(request.form))
    
    title = request.form["name"]
    instructor = request.form["Iname"]
    category = request.form["Cname"]
    description = request.form["Dname"]
    type = request.form["type"]
    startDate = request.form["Bdate"]
    endDate = request.form["Fdate"]

    target = os.path.join(basedir, "static/imageuploads/")
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print("PraisyUpload1"+str(upload))
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            print("File not supported")
            return
            
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        
    new_course = Courses(title, description, instructor, category, filename, type, startDate, endDate)
    db.session.add(new_course)
    db.session.commit()
    
    return render_template("complete.html", image_name=filename )


def choice_query():
    return Course.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='name')

 
# Run Server
if __name__ == '__main__':
  app.run(debug=True)

 