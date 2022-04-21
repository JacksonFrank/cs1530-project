from datetime import timezone, datetime
from flask import render_template, request, url_for, flash, redirect #
from flaskblog import app
from flaskblog.forms import PostForm, CommentForm   #forms is in flaskblog
from forum_user import forum_user_mount, ForumUser

from database_access.lctdb import LCTDB
from forum_post import ForumPost
from forum_comment import ForumComment

import sys
sys.path.append("..")

db_connection = LCTDB()

forum_user_mount(app)

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
        post.createPost(form.title.data, ForumUser.current_user(), form.content.data)

        print(form.title.data)
        flash('Post has been created successfully', 'success')
        return redirect(url_for('home'))        

    return render_template('create_post.html', title='New Post', form=form) 

@app.route("/post/<post_title>", methods=['GET', 'POST'])
def post(post_title):
    #get a post
    author = request.args.get('post_author')
    time = request.args.get('post_time')
    post = ForumPost.getPost(post_title, author, time)

    #comments
    form = CommentForm()
    if form.validate_on_submit():
        #create a new comment
        comment = ForumComment()
        comment.createComment(ForumUser.current_user(), form.content.data)
        post.addComment(comment)
        print(comment.content)
        flash('Comment has been created successfully', 'success')
        return redirect(url_for('post', post_title=post_title, post_author=author, post_time=time))

    comments = post.getRecentComments()
    return render_template('post.html', title=post_title, post=post, comments=comments, form=form)

@app.route("/post/<post_title>/delete", methods=['POST'])
def delete_post(post_title):
    #get a post
    author = request.args.get('post_author')
    time = request.args.get('post_time')
    post = ForumPost.getPost(post_title, author, time)

    #only the user who wrote it can update
    #if post.author != current_user: abort(403)
    post.deletePost()
    flash('Post has been deleted successfully!', 'success')

    return redirect(url_for('home'))

@app.route("/post/<post_title>/<comment_author>/deleteCmt", methods=['POST'])
def delete_comment(post_title, comment_author):
    #get a post
    author = request.args.get('post_author')
    time = request.args.get('post_time')
    post = ForumPost.getPost(post_title, author, time)
    #get and delete a comment
    comment_time = request.args.get('comment_time')
    comment = post.getComment(comment_author, comment_time)
    post.deleteComment(comment)

    #only the user who wrote it can update
    #if post.author != current_user: abort(403)
    flash('Comment has been deleted successfully!', 'success')

    return redirect(url_for('post', post_title=post_title, post_author=author, post_time=time))