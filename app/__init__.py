# -*- coding: utf-8 -*-
from flask import Flask # 引入 flask
app = Flask(__name__) # 实例化一个flask 对象
import views # 导入 views 模块
# from app import views