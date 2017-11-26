""" rmon.views.urls

定义了所有 API 对应的 URL
"""
from flask import Blueprint

from news.views.index import IndexView
from news.views.wx import WxView

api = Blueprint('api', __name__)

# 首页
api.add_url_rule('/', view_func=IndexView.as_view('index'))

# 微信接口
api.add_url_rule('/wx/', view_func=WxView.as_view('wx_view'))
