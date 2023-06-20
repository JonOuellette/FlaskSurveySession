from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug =DebugToolbarExtension(app)

responses = []

@app.route('/')
def survey_home():
    return render_template('start_survey.html', survey = survey)