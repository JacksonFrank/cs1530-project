from datetime import timezone, datetime
from xml.etree.ElementTree import Comment
from flask import render_template, request, url_for, flash, redirect #从flask包导入Flask类
from flaskblog import app
from flaskblog.forms import PostForm, CommentForm   #forms is in flaskblog

from database_access.lctdb import LCTDB
from forum_post import ForumPost
from forum_comment import ForumComment

import sys
sys.path.append("..")

db_connection = LCTDB()

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
        db_connection.registerUser("Zirui", "123456789")
        post = ForumPost()
        post.createPost(form.title.data, "Zirui", form.content.data)
        print(form.title.data)
        flash('Post has been created successfully', 'success')
        return redirect(url_for('home'))        

    return render_template('create_post.html', title='New Post', form=form) 

@app.route("/post/<post_title>", methods=['GET', 'POST'])
def post(post_title):
    #post information
    author = request.args.get('post_author')
    time = request.args.get('post_time')
    post = ForumPost.getPost(post_title, author, time)

    #comments
    form = CommentForm()
    if form.validate_on_submit():
        #create a new comment
        comment = ForumComment()
        comment.createComment("Zirui", form.content.data)
        post.addComment(comment)
        print(comment.content)
        flash('Comment has been created successfully', 'success')
        return redirect(url_for('home'))

    comments = post.getRecentComments()
    return render_template('post.html', title=post_title, post=post, comments=comments, form=form)