""" rmon.app

该模块主要实现了 app 创建函数
"""
import os
from flask import Flask
from news.views import api


def create_app(config=None):
    """ 创建并初始化 Flask app

    Args:
        config(dict): 配置字典

    Returns:
        app (object): Flask App 实例
    """

    app = Flask('wx_dev')

    # 注册 Blueprint
    app.register_blueprint(api)
    return app
