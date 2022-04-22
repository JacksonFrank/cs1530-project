from functools import wraps
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    session,
)
from flask_wtf import FlaskForm
from wtforms import fields, validators
from database_access.lctdb import LCTDB


class UserForm(FlaskForm):
    username = fields.StringField("Username", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=20)
    ])
    password = fields.PasswordField("Password", validators=[
        validators.DataRequired()
    ])


class RegisterForm(UserForm):
    password_confirm = fields.PasswordField("Password Confirm", validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Password not matched')
    ])
    submit = fields.SubmitField("Register")


class LoginForm(UserForm):
    submit = fields.SubmitField("Login")


def forum_user_mount(app: Flask):
    @app.context_processor
    def context_processor():
        return dict(current_user=ForumUser.current_user())

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            if ForumUser.login(username=form.username.data, password=form.password.data):
                return redirect(url_for('about'))
            flash("Incorrect username/passowrd", "warning")
        return render_template("login.html", form=form, title='Login')

    @app.route("/logout")
    def logout():
        ForumUser.logout()
        return redirect(url_for("login"))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if ForumUser.register(form.username.data, form.password.data):
                flash("User has been created successfully", 'success')
                return redirect(url_for("login"))
            flash('"%s" User already exists' % form.username.data, 'warning')
        return render_template("register.html", form=form, title='register')


class ForumUser:
    @staticmethod
    def login(username: str, password: str):
        db_connection = LCTDB()
        result = db_connection.authenticateUser(username, password)
        db_connection.closeCon()
        if result:
            session["_username"] = username
        return result

    @staticmethod
    def logout():
        session.pop('_username')

    @staticmethod
    def register(username, password):
        db_connection = LCTDB()
        exist = db_connection.doesUserExist(username)
        success = False
        if not exist:
            db_connection.registerUser(username, password)
            success = True
        db_connection.closeCon()
        return success


    @staticmethod
    def getQuizLevel(username):
        db_connection = LCTDB()
        level = db_connection.getQuizzesCompleted(username)
        db_connection.closeCon()
        return level

    @staticmethod
    def current_user():
        return session.get("_username")

   

    @staticmethod
    def login_require(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not ForumUser.current_user():
                return redirect(url_for("login"))
            return func(*args, **kwargs)
        return decorated_view
