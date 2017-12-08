from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import UserMixin

from flask import url_for
from .base_models import Base,db
from .user_models import User

class Live(Base):
    __tablename__ = 'live'
    #直播id
    id = db.Column(db.Integer , primary_key = True)
    #直播名称
    name = db.Column(db.String(128),unique = True , index = True , nullable = True)

    #indelete = 'CASCADE'表示如果用户被删除，那么作者为他的直播也会被删除
    #首先通过ForeignKey设置外键,设置后可以通过relastionship来进行访问
    author_id = db.Column(db.Integer , db.ForeignKey('user.id',ondelete = 'CASCADE'))
    author = db.relationship('User',uselist=False)

