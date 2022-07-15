from flask import Flask #从flask包导入Flask类

app = Flask(__name__) #实例化

app.config['SECRET_KEY'] = <SECRET_KEY> #set secret key; protect against attack, etc.

from flaskblog import routes

