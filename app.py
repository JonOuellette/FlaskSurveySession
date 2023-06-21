from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "never-tell!"
debug =DebugToolbarExtension(app)

RESPONSES_KEY= "response"
user_responses = []

@app.route('/')
def survey_home():
    
    return render_template('start_survey.html', survey = survey)

@app.route("/start", methods=["POST"])
def start_survey():

    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_questions(qid):

    if len(user_responses) == len(survey.questions):
        """once all questions have been answered, send them to the completed page """
        return redirect("/complete")
    
    if len(user_responses) != qid:
        """a message will display if the user attempts to skip ahead or enter an invalid question number"""
        flash(f"Invalid question number: {qid}")
        return redirect(f"/questions/{len(user_responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def survey_response():
    choice = request.form['answer']
    user_responses.append(choice)

    if len(user_responses) == len(survey.questions):
        """confirms all questions have been answered and sends them to the completion page"""
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(user_responses)}")
    
@app.route("/complete")
def completed():
    """Survey has been completed, display completion page"""
    return render_template("completed.html")