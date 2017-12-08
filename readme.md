# 说明

## 疑问

这个代码暂时是可以运行的，但是我想知道这个代码应该需要如何进行调试

##　另一个问题

在handlers中的admin.py里最后有一个FIXME,那句被我注释的语句是有错误的

我感觉错误原因是我在forms.py中定义的`test = TextAreaField('管理员发言', validators=[Required(), Length(1, 256)])`，但是咋admin.py中`form.text.data`中好像没有`text`，应该改成`StringField`就没问题了

但是我现在想要和之前能使用`current.logger.debug`一样能方便进行调试，比如我想输出`dir(form)`来看一下

想问一下应该如何方便进行**调试**，现在我是使用`gunicorn -k flask_sockets.worker -b 127.0.0.1:5000 manage:app`来启动网站的。