from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "never-tell!"
debug =DebugToolbarExtension(app)

RESPONSES_KEY= "response"

@app.route('/')
def survey_home():
    
    return render_template('start_survey.html', survey = survey)


@app.route("/start", methods=["POST"])
def start_survey():
    """redirects the user to the first question of the survey"""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_questions(qid):
    """Displays the current questions"""
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        """ redirects the user back to the home page if they attempt to access questions before clicking start"""
        return redirect("/")

    if len(responses) == len(survey.questions):
        """once all questions have been answered, send them to the completed page """
        return redirect("/complete")
    
    if len(responses) != qid:
        """a message will display if the user attempts to skip ahead or enter an invalid question number"""
        flash(f"Invalid question number: {qid}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def survey_response():
    """adds the user responses to the response list"""

    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        """confirms that all the questions have been answered and send the user to the completion page"""
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/complete")
def completed():
    """Survey has been completed, display completion page"""
    return render_template("completed.html")