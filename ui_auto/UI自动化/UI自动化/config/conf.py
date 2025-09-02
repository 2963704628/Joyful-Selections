# -*- coding: utf-8 -*-
# @project: autu-ui
# @file： conf.py
# @微信：supli999
# @Author：测试小志
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "log")
ALLURE_IMG_DIR = os.path.join(LOG_DIR, "image_allure")  # allure报告截图目录
if __name__ == '__main__':
    print(BASE_DIR)
    print(LOG_DIR)
    print(ALLURE_IMG_DIR)
