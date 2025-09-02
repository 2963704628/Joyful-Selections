# -*- coding: utf-8 -*-
# @project: autu-ui
# @file： test_login_register.py
# @微信：supli999
# @Author：测试小志
import allure
import pytest
from selenium.webdriver.common.by import By
from common.sql import MysqlAuto
from po.event import Event
from settings import ENV


class TestLoginRegister:

    @pytest.mark.parametrize('username, password, result', [
        (ENV.user_name, ENV.pass_word, '欢迎您：test123456 | 退出'),
        ('bucunzai', ENV.pass_word, '用户名错误'),
        (ENV.user_name, 'cuowudemim', '密码错误'),
    ], ids=(
            'test_shopping_mall_001',
            'test_shopping_mall_002',
            'test_shopping_mall_003',
    ))
    @allure.feature('登录注册')
    @allure.story('登录')
    def test_shopping_mall_001(self, username, password, result, open_homepage):
        """参数化测试登录"""
        driver = open_homepage
        Event.event_login(driver, username, password)

        if '欢迎您' in result:
            # 登录成功后获取文案
            text = driver.get_text((By.XPATH, "//div[@class='login_btn fl']"))
            driver.sel_click((By.XPATH, "//a[contains(text(),'退出')]"))
            assert text == result
        elif '用户名错误' in result:
            # 不存在的账号获取文案
            text = driver.get_text((By.XPATH, "//div[@class='user_error']"))
            assert text == result
        elif '密码错误' in result:
            # 密码错误获取文案
            text = driver.get_text((By.XPATH, "//div[@class='pwd_error']"))
            assert text == result

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_004(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = 'test_mall_004'
        cpwd = 'test_mall_004'
        email = 'test_mall_004@qq.com'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 查询数据库，检查注册成功
        result = MysqlAuto().execute([f'select * FROM df_user_userinfo where uname="{user_name}"'])[0]
        assert user_name in result

        # 检查能正常登录  登录成功后获取文案
        Event.event_login(driver, user_name, pwd)
        text = driver.get_text((By.XPATH, "//div[@class='login_btn fl']"))
        driver.sel_click((By.XPATH, "//a[contains(text(),'退出')]"))
        assert text == f'欢迎您：{user_name} | 退出'

        # 删掉测试数据
        MysqlAuto().execute([f'delete FROM df_user_userinfo where uname="{user_name}"'])

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_005(self, open_homepage):
        user_name = ENV.user_name
        pwd = 'test_mall_004'
        cpwd = 'test_mall_004'
        email = 'test_mall_004@qq.com'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        # 注意该定位方式：直接查找class='error_tip'有4个，通过其兄弟节点再查找，能精确定位到
        text = driver.get_text((By.XPATH, "//input[@id='user_name']//..//*[@class='error_tip']"))
        assert text == '用户名已经存在'

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_006(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = ''
        cpwd = 'test_mall_004'
        email = 'test_mall_004@qq.com'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        text = driver.get_text((By.XPATH, "//input[@id='pwd']//..//*[@class='error_tip']"))
        assert text == '密码最少4位，最长20位'

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_007(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = 'test_mall_004'
        cpwd = 'test_mall_004'
        email = ''

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        text = driver.get_text((By.XPATH, "//input[@id='email']//..//*[@class='error_tip']"))
        assert text == '你输入的邮箱格式不正确'

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_008(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = 'test_mall_004'
        cpwd = 'test_mall_004' + '1'
        email = 'test_mall_004@qq.com'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        text = driver.get_text((By.XPATH, "//input[@id='cpwd']//..//*[@class='error_tip']"))
        assert text == '两次输入的密码不一致'

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_009(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = 'tes'
        cpwd = 'tes'
        email = 'test_mall_004@qq.com'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        text = driver.get_text((By.XPATH, "//input[@id='pwd']//..//*[@class='error_tip']"))
        assert text == '密码最少4位，最长20位'

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_010(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = 't' * 21
        cpwd = 't' * 21
        email = 'test_mall_004@qq.com'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        text = driver.get_text((By.XPATH, "//input[@id='pwd']//..//*[@class='error_tip']"))
        assert text == '密码最少4位，最长20位'

    @allure.feature('登录注册')
    @allure.story('注册')
    def test_shopping_mall_0011(self, open_homepage):
        user_name = 'test_mall_004'
        pwd = 'test_mall_004'
        cpwd = 'test_mall_004'
        email = 'test_mall_004'

        driver = open_homepage
        Event.event_register(driver, user_name, pwd, cpwd, email)

        # 检查错误提示
        text = driver.get_text((By.XPATH, "//input[@id='email']//..//*[@class='error_tip']"))
        assert text == '你输入的邮箱格式不正确'

    @allure.feature('登录注册')
    @allure.story('退出')
    def test_shopping_mall_0012(self, open_homepage):
        driver = open_homepage
        Event.event_login(driver, ENV.user_name, ENV.pass_word)
        driver.sel_click((By.XPATH, "//a[contains(text(),'退出')]"))

        # 检查首页退出登录成功
        text = driver.get_text((By.XPATH, "//div[@class='login_btn fl']"))
        assert text == '登录 | 注册'
