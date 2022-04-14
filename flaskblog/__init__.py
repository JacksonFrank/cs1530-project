from flask import Flask #从flask包导入Flask类

app = Flask(__name__) #实例化

app.config['SECRET_KEY'] = '06fcd6fc633843ab6f98292a3ccbb5a3' #set secret key; protect against attack, etc.

from flaskblog import routes

