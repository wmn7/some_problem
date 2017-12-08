from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import UserMixin

from flask import url_for

from .base_models import Base,db

class User(Base,UserMixin):
    __tablename__ = 'user'

    #用数值表示角色,方便判断是否有权限,比如有个操作要角色为员工
    #及以上的用户才可以做,那么只要判断 user.role>=ROLE_STAFF
    #就可以了，数值之间设置了１０的间隔为了方便以后加入角色
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique = True , index = True , nullable = False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    publish_courses = db.relationship('Course')
    # 默认情况下，sqlalchemy 会以字段名来定义列名，但这里是 _password, 所以明确指定数据库表列名为 password
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    job = db.Column(db.String(64))

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """python风格的getter"""
        return self._password

    @password.setter
    def password(self,orig_password):
        """python风格的setter,这样设置user.password就会自动为password生成hash值存入_password字段
        """
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        """判断用户输入的密码和存储的hash密码是否相等
        """
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF
    


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(128),unique = True , index = True , nullable = True)

    #课程描述
    description = db.Column(db.String(256))
    #课程url地址
    image_url = db.Column(db.String(256))

    #indelete = 'CASCADE'表示如果用户被删除，那么作者为他的课程也会被删除
    #首先通过ForeignKey设置外键,设置后可以通过relastionship来进行访问
    author_id = db.Column(db.Integer , db.ForeignKey('user.id',ondelete = 'CASCADE'))
    author = db.relationship('User',uselist=False)
    chapters = db.relationship('Chapter')
    
    #方便获取课程url
    @property
    def url(self):
        return url_for('course.detail',course_id=self.id)

class Chapter(Base):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),unique=True,index=True)
    description = db.Column(db.String(256))
    #课程视频的url地址
    vedio_url = db.Column(db.String(256))
    #视频时长 格式:‘30:15’　‘1:15:20’
    vedio_duration = db.Column(db.String(24))
    #关联到课程,并且课程删除就删除相关的章节
    course_id = db.Column(db.Integer,db.ForeignKey('course.id',ondelete="CASCADE"))
    course = db.relationship('Course',uselist=False)

    def __repr__(self):
        return '<Chapter:{}>'.format(self.name)

    @property
    def url(self):
        return url_for('course.chapter', course_id=self.course.id, chapter_id=self.id)



