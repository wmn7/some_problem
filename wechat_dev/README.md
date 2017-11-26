# 简单连接微信公众号项目

## 启动应用

基于 Python3 开发，通过 virtualenv 建立开发环境

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ source venv/bin/activate
```

依赖软件包安装完成后，通过以下命令启动应用：

```
$ FLASK_APP=app.py flask run
```

或者

```
$ FLASK_DEBUG=1 FLASK_APP=app.py flask init_db 
$ FLASK_DEBUG=1 FLASK_APP=app.py flask run

```


接着访问 `http://127.0.0.1:5000` 查看效果。

## 测试用例

暂时没有测试用例
