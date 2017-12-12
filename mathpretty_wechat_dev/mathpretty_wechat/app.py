from flask import Flask,render_template
from mathpretty_wechat.config import configs
from mathpretty_wechat.models import db

from flask_migrate import Migrate


#注册蓝图的函数
def register_blueprints(app):  
    from .handlers import wechat
    app.register_blueprint(wechat)



#用于将flask拓展注册到app
def register_extensions(app):
    db.init_app(app)
    Migrate(app,db)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    #SQLAlchemy的初始化方式改为使用init_app
    register_extensions(app)
    #注册蓝图
    register_blueprints(app)

    return app