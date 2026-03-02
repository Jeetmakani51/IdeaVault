from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Idea(db.Model):
        __tablename__ = "ideas"
        id = db.Column(db.Integer,primary_key = True)
        title = db.Column(db.String(200),nullable = False)
        description = db.Column(db.Text,nullable = False)

@app.route("/")
def home():
    ideas = Idea.query.all()    #fetch all ideas
    return render_template("index.html",ideas = ideas)

@app.route("/add", methods=["GET","POST"])
def add_idea():
        if request.method == "POST":
                title = request.form["title"]
                description = request.form["description"]

                new_idea = Idea(title = title, description = description)
                db.session.add(new_idea)
                db.session.commit()

                return redirect("/")
        return render_template("post.html")

if __name__ == "__main__":
    app.run(debug=True)

'''
User clicks submit
        ↓
Browser sends POST
        ↓
Flask receives data
        ↓
Flask saves to DB
        ↓
Flask redirects to /
        ↓
Flask fetches all ideas
        ↓
Template renders updated list
        ↓
User sees new idea
'''

'''
GET / → Fetch → Render

GET /add → Show form

POST /add → Save → Redirect

GET / → Fetch updated data → Render again
'''