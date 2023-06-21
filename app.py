from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "never-tell!"
debug =DebugToolbarExtension(app)

responses = []

@app.route('/')
def survey_home():
    
    return render_template('start_survey.html', survey = survey)

@app.route("/start")
def start_survey():

    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def view_questions(qid):

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)