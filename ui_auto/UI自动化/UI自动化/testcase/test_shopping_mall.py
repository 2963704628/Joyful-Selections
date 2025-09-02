# -*- coding: utf-8 -*-
# @project: autu-ui
# @file： test_shopping_mall.py
# @微信：supli999
# @Author：测试小志
from time import sleep

import allure
from selenium.webdriver.common.by import By
from common.sql import MysqlAuto
from po.event import Event
from settings import DBSql, ENV


class TestShoppingMall:

    @allure.feature('提交订单')
    @allure.story('立即购买')
    def test_shopping_mall_013(self, login):
        # 实例化driver
        driver = login
        # 初始化数据，确保无地址，无订单
        MysqlAuto().execute(DBSql.sql_list)
        # 新增地址
        Event.add_address(driver)
        # 立即购买并点击提交订单
        Event.event_submit_order(driver)

        # 查数据库，检查订单
        sql = ['select * from df_order_orderinfo']
        order_id_list = MysqlAuto().execute(sql)
        assert len(order_id_list) == 1

        # 获取页面的订单信息
        order_id = order_id_list[0][0]
        text = driver.get_text((By.XPATH, "//ul[@class='order_list_th w978 clearfix']"))
        assert order_id in text

    @allure.feature('提交订单')
    @allure.story('立即购买')
    def test_shopping_mall_014(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)
        # 实例化
        driver = login
        # 立即购买并点击提交订单
        Event.event_submit_order(driver)
        # 获取alert文本信息
        result = driver.alert_text()
        # 断言
        assert result == '请填写正确的收货地址'

    @allure.feature('提交订单')
    @allure.story('加入购物车')
    def test_shopping_mall_015(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)
        # 实例化
        driver = login

        # 加入购物车1
        driver.get(ENV.url + '18/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        Event.add_address(driver)
        Event.shopping_cart_go_to_settlement(driver)

        # 查数据库，检查订单
        sql = ['select * from df_order_orderinfo']
        order_id_list = MysqlAuto().execute(sql)
        assert len(order_id_list) == 1

        # 获取页面的订单信息
        order_id = order_id_list[0][0]
        text = driver.get_text((By.XPATH, "//ul[@class='order_list_th w978 clearfix']"))
        assert order_id in text

    @allure.feature('提交订单')
    @allure.story('加入购物车')
    def test_shopping_mall_016(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login

        # 加入购物车1
        driver.get(ENV.url + '18/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        # 加入购物车2
        driver.get(ENV.url + '17/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        Event.add_address(driver)
        Event.shopping_cart_go_to_settlement(driver)

        # 查数据库，检查订单
        sql = ['select * from df_order_orderinfo']
        order_id_list = MysqlAuto().execute(sql)
        assert len(order_id_list) == 1

        # 获取页面的订单信息
        order_id = order_id_list[0][0]
        text = driver.get_text((By.XPATH, "//ul[@class='order_list_th w978 clearfix']"))
        assert order_id in text

    @allure.feature('提交订单')
    @allure.story('加入购物车')
    def test_shopping_mall_017(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login

        # 新增地址提交订单
        Event.add_address(driver)
        Event.shopping_cart_go_to_settlement(driver)

        assert driver.alert_text() == '订单提交失败'

    @allure.feature('搜索')
    @allure.story('搜索')
    def test_shopping_mall_018(self, login):
        # 实例化
        driver = login
        keyword = ['草莓', '香蕉', '刀鱼', '扇贝', '基围虾', '葡萄']
        # 搜索
        for i in keyword:
            Event.event_search_key(driver, i)
            text = driver.get_text((By.XPATH, "//ul[@class='goods_type_list clearfix']"))
            # 断言列表中搜索到商品
            assert i in text

    @allure.feature('搜索')
    @allure.story('搜索')
    def test_shopping_mall_019(self, login):
        # 实例化
        driver = login
        Event.event_search_key(driver, 'hello world')
        text = driver.alert_text()
        assert text == '您的查询结果为空，为您推荐以下商品'

    @allure.feature('搜索')
    @allure.story('搜索')
    def test_shopping_mall_020(self, login):
        # 实例化
        driver = login
        Event.event_search_key(driver, '')
        text = driver.alert_text()
        assert text == '请输入搜索内容'

    @allure.feature('我的订单')
    @allure.story('我的订单')
    def test_shopping_mall_021(self, login):
        # 实例化
        driver = login
        driver.get(ENV.url + 'user/order/1')
        text = driver.get_text((By.XPATH, "//div[@class='pagenation']"))
        assert text == '1'

    @allure.feature('购物车')
    @allure.story('购物车')
    def test_shopping_mall_022(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login

        # 加入购物车
        driver.get(ENV.url + '18/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        driver.get(ENV.url + 'cart/')
        text = driver.get_text((By.XPATH, "//li[contains(text(),'牛奶草莓')]"))
        assert '牛奶草莓' in text

    @allure.feature('购物车')
    @allure.story('购物车')
    def test_shopping_mall_023(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login

        # 加入购物车
        driver.get(ENV.url + '18/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        # 打开购物车查看金额
        driver.get(ENV.url + 'cart/')
        start = int(float(driver.get_text((By.XPATH, "//em[@id='total']"))))

        # 增加数量
        driver.sel_click((By.XPATH, "//a[normalize-space()='+']"))
        end = int(float(driver.get_text((By.XPATH, "//em[@id='total']"))))

        # 断言新增数量成功；金额增加
        assert start * 2 == end

    @allure.feature('购物车')
    @allure.story('购物车')
    def test_shopping_mall_024(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login

        # 加入购物车
        driver.get(ENV.url + '18/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        # 打开购物车查看金额
        driver.get(ENV.url + 'cart/')
        start = int(float(driver.get_text((By.XPATH, "//em[@id='total']"))))

        # 增加数量/减少数量
        [driver.sel_click((By.XPATH, "//a[normalize-space()='+']")) for i in range(3)]
        [driver.sel_click((By.XPATH, "//a[normalize-space()='-']")) for i in range(1)]

        end = int(float(driver.get_text((By.XPATH, "//em[@id='total']"))))

        # 断言新增数量成功；金额增加
        assert start * 3 == end

    @allure.feature('购物车')
    @allure.story('购物车')
    def test_shopping_mall_025(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login

        # 加入购物车
        driver.get(ENV.url + '18/')
        [driver.sel_click((By.XPATH, "//a[@id='add_cart']")) for i in range(2)]

        # 检查购物车共1件商品
        driver.get(ENV.url + 'cart/')
        text = driver.get_text((By.XPATH, "//b[@class='total_count1']"))
        assert text == '1'

        # 删除商品
        driver.sel_click((By.XPATH, "//a[contains(text(),'删除')]"))
        driver.click_alert()

        # 删除后，共0件商品
        driver.get(ENV.url + 'cart/')
        text = driver.get_text((By.XPATH, "//b[@class='total_count1']"))
        assert text == '0'

    @allure.feature('购物车')
    @allure.story('购物车')
    def test_shopping_mall_026(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login
        Event.add_address(driver)
        Event.shopping_cart_go_to_settlement(driver)
        text = driver.alert_text()
        assert text == '订单提交失败'

    @allure.feature('收货地址')
    @allure.story('收货地址')
    def test_shopping_mall_027(self, login):
        # 初始化数据
        MysqlAuto().execute(DBSql.sql_list)

        # 实例化
        driver = login
        Event.add_address(driver)
