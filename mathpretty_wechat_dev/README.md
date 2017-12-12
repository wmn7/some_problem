#数据库初始化

## 使用 flask-migrate 初始化数据库
$ FLASK_APP=manage.py flask db init
$ FLASK_APP=manage.py flask db migrate -m 'init database'
$ FLASK_APP=manage.py flask db upgrade

## 使用脚本生成测试数据

$ FLASK_APP=manage.py flask shell
$ from mathpretty_wechat.scripts.gengerate_data import run
$ run()

##
./ngrok http 5000