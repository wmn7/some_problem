""" rmon.views.wx

微信相关视图控制器
"""
import hashlib
from flask import Blueprint,make_response
from flask import request, current_app, abort, render_template, make_response
from wechatpy import parse_message,create_reply


#定义一个处理微信信息的函数
def check_signature():
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

def get():
    """ 用于验证在微信公众号后台设置的URL
    """
    check_signature()
    current_app.logger.debug(request.args.get('echostr'))
    return make_response(str(request.args.get('echostr')))

def post():
    """ 处理微信消息
    """
    check_signature()

    msg = parse_message(request.data)

    #print(msg.content.strip())
    
    #iptest = IPLocationHandler()
    #reply = iptest.handle(msg)

    #给用户回复相同的东西
    reply = create_reply(msg.content,msg)
    #reply = wx_dispatcher.dispatch(msg)
    return str(reply.render())


wechat = Blueprint('wechat',__name__,url_prefix='/wechat')

@wechat.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        get()
    else:
        post()




