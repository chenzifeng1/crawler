# -*- coding: utf-8 -*-
from flask import Flask # 引入 flask
app = Flask(__name__) # 实例化一个flask 对象
import views # 导入 views 模块
# from app import views
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir

app = Flask(__name__)
app.config.from_object('config') # 载入配置文件
db = SQLAlchemy(app) # 初始化 db 对象

# from app import views, models # 引用视图和模型
  import views, models