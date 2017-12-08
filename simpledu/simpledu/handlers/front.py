from flask import Blueprint,render_template,flash,redirect,url_for

from flask import current_app,request

from simpledu.models import Course,User

from simpledu.forms import LoginForm,RegisterForm

from flask_login import login_user,logout_user,login_required

front = Blueprint('front',__name__)

@front.route('/')
#路由模块化
def index():
    # 获取参数传过来的页数
    page = request.args.get('page',default=1,type=int)
    #生成分页对象
    pagination = Course.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('index.html',pagination = pagination)

@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        #打印日志
        #current_app.logger.debug(user)
        #current_app.logger.debug(type(user))
        
        login_user(user,form.remember_me.data)
        flash("欢迎用户"+form.username.data+"登录~~~","success")
        return redirect(url_for('front.index'))

    return render_template('login.html',form=form)

@front.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash("注册成功,请登录!","success")
        #重定向
        return redirect(url_for('front.login'))
    return render_template('register.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录','success')
    return redirect(url_for('front.index'))
