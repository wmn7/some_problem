from flask import Blueprint,render_template,abort
from simpledu.models import User

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/')
def index():
    return 'user'

@user.route('/<username>')
def find_user(username):
    #这是一种写法
    #user = User.query.filter(User.username == username).first_or_404()
    user = User.query.filter(User.username == username).first()
    if user == None:
        abort(404)
    return render_template('user.html',user = user)

@user.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

    