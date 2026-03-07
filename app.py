from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import UUID
import uuid
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

class Comment(db.Model):
        __tablename__ = "comments"

        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        content = db.Column(db.Text, nullable=False)

        idea_id = db.Column(
                UUID(as_uuid=True),
                db.ForeignKey("ideas.id"),
                nullable=False
        )

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


@app.route("/comment/<uuid:idea_id>", methods = ["GET","POST"])
def add_comment(idea_id):
        idea = Idea.query.get_or_404(idea_id)
        if request.method == "POST":
                content = request.form.get("content")
                new_comment = Comment(
                        content=content,
                        idea_id=idea_id
                )
                db.session.add(new_comment)
                db.session.commit()

                return redirect(f"/comment/{idea_id}")
        comments = Comment.query.filter_by(idea_id=idea_id).all()

        return render_template(
                "comment.html",
                idea=idea,
                comments=comments
        )

'''
User clicks comment button
        ↓
GET /send/<idea_id>
        ↓
Flask loads idea
        ↓
Flask loads comments
        ↓
Render comment.html
        ↓
User writes comment
        ↓
Form POST /send/<idea_id>
        ↓
Flask receives POST
        ↓
Create Comment object
        ↓
Save to database
        ↓
Redirect to page
        ↓
Page reloads with new comment
'''

'''
1 Get resource ID from URL
2 Fetch object from database
3 if POST:
        - read form data
        - create/update/delete object
        - commit
        - redirect
4. If GET:
        - fetch data
        - render template
'''


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