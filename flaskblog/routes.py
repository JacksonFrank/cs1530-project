from datetime import timezone, datetime
from flask import render_template, url_for, flash, redirect #从flask包导入Flask类
from flaskblog import app
from flaskblog.forms import PostForm, CommentForm   #forms is in flaskblog

from database_access.lctdb import LCTDB
from forum_post import ForumPost
import sys
sys.path.append("..")

#db_connection = LCTDB()
'''
posts = [
    {
        'id': 1,
        'author': 'Zirui Huang',
        'title': 'Post 1',
        'date': '2022/4/11',
        'reply': 2,
        'content': 'This is my first post!'
    },

    {   
        'id': 2,
        'author': 'Haoxuan Huang',
        'title': 'Post 2',
        'date': '2022/4/10',
        'reply': 4,
        'content': 'This is my second post!'


    }
]
'''
@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/forum")
def home():
    posts = ForumPost.getRecentPosts()
    return render_template('home.html', posts=posts, title='Forum')


@app.route("/post/new", methods=['GET', 'POST']) #accept get and post request
def new_post():
    form = PostForm() #initialize a form

    if form.validate_on_submit():               #check if validated when submitted (create post)
        post = ForumPost()
        post.createPost(form.title.data, "Zirui", form.content.data)
        flash('Post has been created successfully', 'success')
        return redirect(url_for('home'))                        

    return render_template('create_post.html', title='New Post', form=form) 

@app.route("/post/<int:post_id>")
def post(post_id):
    #post = posts[0] #get post from database
    return render_template('post.html', title=post['title'], post=post)