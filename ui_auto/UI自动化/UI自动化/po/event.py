# -*- coding: utf-8 -*-
# @project: autu-ui
# @file： event.py
# @微信：supli999
# @Author：测试小志
from time import sleep

import allure
from selenium.webdriver.common.by import By

from common.log import log
from settings import ENV


class Event:

    @staticmethod
    @allure.step('立即购买并点击提交订单')
    def event_submit_order(driver):
        """
        立即购买并点击提交订单
        :param driver:
        :return:
        """
        try:
            driver.get(ENV.url + '18/')
            # driver.sel_click((By.XPATH, '//body/div[5]/div[2]/ul[1]/li[1]/a[1]/img[1]'))
            driver.sel_click((By.XPATH, "(//a[contains(text(),'立即购买')])[1]"))
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))
            driver.sel_click((By.XPATH, "//a[@id='order_btn']"))
            sleep(1)
        except Exception as e:
            log.error(f'立即购买并点击提交订单事件异常，为：{e}')
            raise e

    @staticmethod
    @allure.step('登录')
    def event_login(driver, username, password):
        """
        登录
        :param driver:
        :param username:
        :param password:
        :return:
        """
        try:
            driver.get(ENV.url)
            driver.sel_click((By.XPATH, "//a[contains(text(),'登录')]"))
            driver.sel_send_keys((By.XPATH, "//input[@placeholder='请输入用户名']"), username)
            driver.sel_send_keys((By.XPATH, "//input[@placeholder='请输入密码']"), password)
            driver.sel_click((By.XPATH, "//input[@value='登录']"))
        except Exception as e:
            log.error(f'登录异常，为：{e}')
            raise e

    @staticmethod
    @allure.step('注册')
    def event_register(driver, user_name, pwd, cpwd, email):
        """
        注册
        :param driver:
        :param user_name:
        :param pwd:
        :param cpwd:
        :param email:
        :return:
        """
        try:
            driver.get(ENV.url)
            driver.sel_click((By.XPATH, "//a[contains(text(),'注册')]"))
            driver.sel_send_keys((By.XPATH, "//input[@id='user_name']"), user_name)
            driver.sel_send_keys((By.XPATH, "//input[@id='pwd']"), pwd)
            driver.sel_send_keys((By.XPATH, "//input[@id='cpwd']"), cpwd)
            driver.sel_send_keys((By.XPATH, "//input[@id='email']"), email)
            driver.sel_click((By.XPATH, "//input[@value='注 册']"))
        except Exception as e:
            log.error(f'登录异常，为：{e}')
            raise e

    @staticmethod
    @allure.step('新增收货地址')
    def add_address(driver, ushou='张三', uphone='18667678909', uyoubian='998989', uaddress='人民路10号'):
        """
        新增收货地址
        :param driver:
        :param ushou:
        :param uphone:
        :param uyoubian:
        :param uaddress:
        :return:
        """
        try:
            driver.get(ENV.url)
            driver.sel_click((By.XPATH, "//a[contains(text(),'用户中心')]"))
            driver.sel_click((By.XPATH, "//a[contains(text(),'· 收货地址')]"))
            driver.sel_send_keys((By.XPATH, "//input[@name='ushou']"), ushou)
            driver.sel_send_keys((By.XPATH, "//input[@name='uphone']"), uphone)
            driver.sel_send_keys((By.XPATH, "//input[@name='uyoubian']"), uyoubian)
            driver.sel_send_keys((By.XPATH, "//textarea[@name='uaddress']"), uaddress)
            driver.sel_click((By.XPATH, "//input[@value='修改地址']"))
        except Exception as e:
            log.error(f'登录异常，为：{e}')
            raise e

    @staticmethod
    @allure.step('从购物车中去结算')
    def shopping_cart_go_to_settlement(driver):
        """
        从购物车中去结算
        :param driver:
        :return:
        """
        try:
            driver.get(ENV.url + 'cart/')
            driver.sel_click((By.XPATH, "//a[contains(text(),'去结算')]"))
            driver.sel_click((By.XPATH, "//a[@id='order_btn']"))
        except Exception as e:
            log.error(f'登录异常，为：{e}')
            raise e

    @staticmethod
    @allure.step('搜索')
    def event_search_key(driver, keyword):
        """
        搜索
        :param driver:
        :param keyword:
        :return:
        """
        try:
            driver.get(ENV.url)
            driver.sel_send_keys((By.XPATH, "//input[@placeholder='搜索商品']"), keyword)
            driver.sel_click((By.XPATH, "//input[@value='搜索']"))
            sleep(0.5)
        except Exception as e:
            log.error(f'登录异常，为：{e}')
            raise e
