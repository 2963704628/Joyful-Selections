# -*- coding: utf-8 -*-
# @project: autu-ui
# @file： settings.py
# @微信：supli999
# @Author：测试小志
import os


class ENV:
    """被测环境"""
    """这里改成你本地启动电子商城的地址和端口"""
    # url = 'http://192.168.8.21:8000/'  # 另一台电脑
    url = 'http://127.0.0.1:8000/'  # 本地
    user_name = 'test123456'
    pass_word = 'test123456'
    host_ip = url.split('/')[2].split(':')[0]


class DBSql:
    """
    初始化时清除数据sql语句
    清空：用户、购物车、订单信息
    并插入：测试用户 test123456
    """
    # sql_file = rf'\\{ENV.host_ip}\daily_fresh_demo-master\db.sqlite3'  # 另一台电脑
    sql_file = rf'D:\电子商城系统\daily_fresh_demo-master\db.sqlite3'  # 本地
    # D:\电子商城系统\daily_fresh_demo-master\db.sqlite3
    sql_list = [
        'DELETE FROM df_order_orderdetailinfo',
        'DELETE FROM df_order_orderinfo',
        'DELETE FROM df_user_userinfo',
        'DELETE FROM df_cart_cartinfo',
        "INSERT INTO 'df_user_userinfo' VALUES ('46', 'test123456', 'fb15a1bc444e13e2c58a0a502c74a54106b5a0dc', 'sadfasdfasd@qq.com', '', '', '', '');"
    ]


if __name__ == '__main__':
    print(ENV.url.split('/')[2].split(':')[0])
