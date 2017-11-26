""" rmon.views.wx

微信相关视图控制器
"""
import hashlib

from flask import request, current_app, abort, render_template, make_response
from flask.views import MethodView
from wechatpy import parse_message,create_reply


class WxView(MethodView):
    """ 微信相关视图控制器
    """

    def check_signature(self):
        """ 验证请求是否来自于微信请求
        """
        signature = request.args.get('signature')
        if signature is None:
            abort(403)

        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')

        #msg = [current_app.config['WX_TOKEN'], timestamp, nonce]
        msg = ["WMN_777", timestamp, nonce]
        msg.sort()

        sha = hashlib.sha1()
        sha.update(''.join(msg).encode('utf-8'))
        # 首先将 Token、timestamp、nonce三个参数按字典进行排序； 
        # 接着将三个参数字符串拼接成一个字符串并进行 sha1 哈希； 
        # 然后将哈希结果与 signature 做对比，如果一致则表示前面正确，请求确实来自于微信服务器；
        if sha.hexdigest() != signature:
            abort(403)

    def get(self):
        """ 用于验证在微信公众号后台设置的URL
        """
        self.check_signature()
        return request.args.get('echostr')

    def post(self):
        """ 处理微信消息
        """
        self.check_signature()

        msg = parse_message(request.data)

        #print(msg.content.strip())
        
        #iptest = IPLocationHandler()
        #reply = iptest.handle(msg)

        #给用户回复相同的东西
        reply = create_reply(msg.content,msg)
        #reply = wx_dispatcher.dispatch(msg)
        return reply.render()


