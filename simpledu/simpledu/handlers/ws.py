from flask import Blueprint
import redis
import gevent
import json

ws = Blueprint('ws',__name__,url_prefix='/ws')

#创建redis连接
redis = redis.from_url('redis://127.0.0.1:6379')

class Chatroom(object):
    def __init__(self):
        self.clients = []
        #初始化pubsub系统
        self.pubsub = redis.pubsub()
        #订阅chat频道
        self.pubsub.subscribe('chat')

    def register(self,client):
        self.clients.append(client)
        redis.publish('chat', 'New user come in, people count: ')

    def send(self,client,data):
        #给每个客户端client发送消息data
        try:
            #python3接受到的消息是二进制的，先使用decode函数转换为字符串
            client.send(data.decode('utf-8'))
        except:
            #发送错误可能是客户端已经关闭,移除该客户端
            self.clients.remove(client)

    def run(self):
        #依次将接收到的消息再发送给客户端
        for message in self.pubsub.listen():
            data = message.get('data')
            for client in self.clients:
                #使用gevent异步发送
                gevent.spawn(self.send,client,data)
    
    def start(self):
        #异步执行run函数
        gevent.spawn(self.run)

#初始化聊天室
chat = Chatroom()
#异步启动聊天室
chat.start()

@ws.route('/send')
def inbox(cr):
    #使用 flask-sockets，cr 链接对象会被被自动注入到路由处理函数
    while not cr.closed:
        #进行上下文切换
        gevent.sleep(0.1)
        message = cr.receive()

        if message:
            #发送消息到chat频道
            redis.publish('chat',message)

@ws.route('/recv')
def outbox(cr):
    chat.register(cr)
    redis.publish('chat', json.dumps(dict(username='New user come in, people count',text=len(chat.clients))))
    while not cr.closed:
        gevent.sleep(0.1)





    



