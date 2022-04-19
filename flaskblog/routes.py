from turtle import title
from flask import render_template, url_for, flash, redirect #从flask包导入Flask类
from flaskblog import app
from flaskblog.forms import PostForm, CommentForm   #forms is in flaskblog

posts = [
    {
        'author': 'Zirui Huang',
        'title': 'Post 1',
        'date': '2022/4/11',
        'reply': 2
    },

    {
        'author': 'Haoxuan Huang',
        'title': 'Post 2',
        'date': '2022/4/10',
        'reply': 4

    }
]

@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/forum")
def home():
    return render_template('home.html', posts=posts, title='Forum')


@app.route("/post/new", methods=['GET', 'POST']) #accept get and post request
def new_post():
    form = PostForm() #initialize a forum
    if form.validate_on_submit(): #check if validated when submitted
        #add to database
        flash('Post has been created successfully', 'success')
        return redirect(url_for('home'))   #redirect to 'about' route (name of template)

    return render_template('create_post.html', title='New Post', form=form) 


'''
@app.route("/quiz", methods=['GET'])
def get_quiz():
    quizzes_taken = x
    new_quiz = Quiz(quizzes_taken + 1)
    first_question = new_quiz.popQuizQuestion()
    return [first_question.getQuestion(), first_question.getRandomAnswers()]
'''
