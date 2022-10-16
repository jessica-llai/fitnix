from flask import Flask, render_template, url_for, redirect, request
from googleapiclient.discovery import build
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from dotenv import load_dotenv
# constant

load_dotenv()
API_KEY = os.getenv('API_KEY')
base_video_url = 'https://www.youtube.com/watch?v='
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap4(app)
video_res = None





class FitnessForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired()])
    exercise = StringField('Exercise', validators=[DataRequired()])
    setting = StringField('Setting', validators=[DataRequired()])
    submit = SubmitField('submit')


class Video_Finder:
    def __init__(self):
        self.video_finder_name = 'abc'

    def video_finder(self, body, exercise, setting):
        # request video
        body_part = body
        exercise_type = exerciseq
        setting = setting


        yt = build('youtube', 'v3', developerKey=API_KEY)

        request = yt.search().list(
            part="id,snippet",
            type='video',
            q=f'{body_part} {exercise_type} training {setting}',
            videoDuration='long',
            videoDefinition='high',
            maxResults=20,
        )
        response = request.execute()
        items = response['items']
        video_id = []
        video_title = []
        for i in items:
            video_title.append(i['snippet']['title'])
            video_id.append(i['id']['videoId'])

        video_links = []
        for v in video_id:
            v_url = f'{base_video_url}{v}'
            video_links.append(v_url)

        title_and_link = dict(zip(video_title, video_links))
        return title_and_link


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FitnessForm()
    if form.validate_on_submit():
        body = form.body.data
        exercise = form.body.data
        setting = form.setting.data
        v = Video_Finder()
        global video_res
        video_res = v.video_finder(body=body, exercise=exercise, setting=setting)
        return redirect('display')
    return render_template('index.html', form=form)


@app.route('/display', methods=['GET', 'POST'])
def display():
    return render_template('display.html', videos=video_res)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
