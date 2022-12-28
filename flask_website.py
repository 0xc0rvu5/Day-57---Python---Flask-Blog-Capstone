import datetime, requests
from post import Post
from flask import Flask
from genderize import Genderize
from flask import render_template


#initialize global variables
#create flask APP global variable and direct it to the templates/static folders
APP = Flask(__name__, template_folder='templates', static_folder='static')
BLOGS_URL = requests.get('https://api.npoint.io/bc7837b0a5fdaf19962b').json()
POST_LIST = []


#populate POST_LIST with relevant key/value pairs from BLOGS_URL endpoint
for post in BLOGS_URL:
    temp = Post(post['id'], post['title'], post['subtitle'], post['body'])
    POST_LIST.append(temp)


@APP.route('/')
def main():
    year = datetime.date.today().year
    return render_template('index.html', year=year, posts=POST_LIST)


@APP.route('/post/<int:num>')
def post(num):
    year = datetime.date.today().year
    for post in POST_LIST:
        if post.id == num:
            requested = post
    return render_template('post.html', post=requested, year=year)


@APP.route('/<name>')
def name(name):
    year = datetime.date.today().year
    get_gender = Genderize().get([name])[0].get('gender')
    response = requests.get(f'https://api.agify.io/?name={name}')
    get_age = response.json()['age']
    return render_template('name.html', name=name, get_gender=get_gender, get_age=get_age, year=year)


#turn on debugging to allow for `some` dynamic updates
if __name__ == '__main__':
    APP.run(debug=True)


#to start run
#export FLASK_APP=name_of_flask_file
#flask run