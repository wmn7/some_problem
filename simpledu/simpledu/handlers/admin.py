from flask import Blueprint,render_template
from flask import request,current_app,url_for,flash,redirect
from simpledu.models import Course,User,Live
from simpledu.forms import CourseForm,UserForm,LiveForm,MessageForm
from simpledu.decorators import admin_required
from simpledu.models import db
admin = Blueprint('admin',__name__,url_prefix='/admin')
import json
from .ws import redis

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

#课程管理
@admin.route('/courses')
@admin_required
def courses():
    #获得页数
    page = request.args.get('page',default=1,type=int)
    pagination = Course.query.paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('admin/courses.html',pagination = pagination)

#课程增加
@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_course.html', form=form)

#课程修改
@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    #在创建form对象的时候传入course对象,则表单会自动在对于位置填入数据
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)

#课程删除,不需要页面，删除成功后直接跳转到课程页面
@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('课程删除成功', 'success')
    return redirect(url_for('admin.courses'))




#成员管理
@admin.route('/users')
@admin_required
def users():
    #获得页数
    page = request.args.get('page',default=1,type=int)
    pagination = User.query.paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('admin/users.html',pagination = pagination)

#成员增加
@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('成员创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)

#成员修改
@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    #在创建form对象的时候传入course对象,则表单会自动在对于位置填入数据
    #current_app.logger.debug('1 : '+user.password)
    form = UserForm(obj=user)
    #current_app.logger.debug('2 : '+form.password.data)
    if form.validate_on_submit():
        form.update_user(user)
        flash('成员更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)

#课程删除,不需要页面，删除成功后直接跳转到课程页面
@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('成员删除成功', 'success')
    return redirect(url_for('admin.users'))





#直播管理台
@admin.route('/live')
@admin_required
def live():
    #获得页数
    page = request.args.get('page',default=1,type=int)
    pagination = Live.query.paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False
    )
    return render_template('admin/live.html',pagination = pagination)

#增加直播
@admin.route('/live/create', methods=['GET', 'POST'])
@admin_required
def create_live():
    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('直播创建成功', 'success')
        return redirect(url_for('admin.live'))
    return render_template('admin/create_live.html', form=form)


#群发直播消息
@admin.route('/message',methods=['GET','POST'])
@admin_required
def message():
    form = MessageForm()
    if form.validate_on_submit():
        #redis.publish('chat',json.dumps(dict(username='System',text=form.text.data)))
        redis.publish('chat',json.dumps(dict(username='System',text='test')))
        flash('发言成功', 'success')
        return redirect(url_for('admin.message'))
    return render_template('admin/message.html', form=form)

