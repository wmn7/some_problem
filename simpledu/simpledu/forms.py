from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError,TextAreaField,IntegerField
from wtforms.validators import Length,Email,EqualTo,Required,URL,NumberRange

from simpledu.models import db,User,Course,Live

#注册界面的表格
class RegisterForm(FlaskForm):
    #Form为每个输入框声明一个对应的Field，Field有两个参数，
    #第一个是输入框在html中的label
    #第二个是wtforms验证器
    username = StringField('用户名',validators=[Required(),Length(3,24)])
    email = StringField('邮箱',validators=[Required(),Email(message='请输入合法的email地址')])
    password = PasswordField('密码',validators=[Required(),Length(6,26,message="密码长度要在6-24个字符之间")])
    repeat_password = PasswordField('重复密码',validators=[Required(),EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self,field):
        #用户名只能包含字母和数字
        if not field.data.isalnum():
            raise ValidationError('用户名只能包含数字和字母')
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
        
    
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

#登录界面的表格
class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[Required(),Length(3,24)])
    password = PasswordField('密码',validators=[Required(),Length(6,26)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username(self,field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名未注册')
    
    def validate_password(self,field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

#增加和修改课程信息的表格
class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[Required(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[Required(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[Required(), URL()])
    author_id = IntegerField('作者ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        # 使用课程表单数据填充 course 对象
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

#增加和修改用户信息的表格
class UserForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(2, 32)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码',validators=[Required()])
    role = IntegerField('权限', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    job = StringField('职业',validators=[Required(),Length(2,24)])
    submit = SubmitField('提交')

    def validate_author_name(self,field):
        #用户名只能包含字母和数字
        if not field.data.isalnum():
            raise ValidationError('用户名只能包含数字和字母')
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
        
    
    def validate_author_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_user(self):
        user = User()
        # 使用课程表单数据填充 course 对象
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


#增加直播的表格
class LiveForm(FlaskForm):
    name = StringField('直播名称', validators=[Required(), Length(2, 32)])
    author_id = StringField('用户名称', validators=[Required()])
    submit = SubmitField('提交')
    #检测直播的名字是否存在
    def validate_name(self,field):
        if Live.query.filter_by(name=field.data).first():
            raise ValidationError('直播已经存在')
    #检测直播的用户是否存在
    def validate_author_id(self,field):
        if User.query.filter_by(id = field.data).first()==None:
            raise ValidationError('用户id不存在')
    #用来创建直播
    def create_live(self):
        live = Live()
        # 使用课程表单数据填充 course 对象
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live

# 群发消息的表单
class MessageForm(FlaskForm):
    test = TextAreaField('管理员发言', validators=[Required(), Length(1, 256)])
    submit = SubmitField('提交')

