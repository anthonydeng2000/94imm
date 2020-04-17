# -*- encoding: utf-8 -*-
"""
@File    : download.py
@Time    : 2020/4/17 14:44
@Author  : Turnright-git
@Email   : weifeizxy@gmail.com
@Software: PyCharm
"""

import sys

sys.path.append('../')
from bs4 import BeautifulSoup
import threading, pymysql, time, requests, os, urllib3, re
from config import mysql_config

requests.packages.urllib3.disable_warnings()
# 数据库连接信息
dbhost = {
    "host": mysql_config['HOST'],
    "dbname": mysql_config['NAME'],
    "user": mysql_config['USER'],
    "password": mysql_config['PASSWORD']
}
db = pymysql.connect(dbhost.get("host"), dbhost.get("user"), dbhost.get("password"), dbhost.get("dbname"))

url_list= db.cursor('select * from images_image')
