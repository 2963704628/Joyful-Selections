# -*- coding: utf-8 -*-
# @project: autu-ui
# @file： conftest.py
# @微信：supli999
# @Author：测试小志

import pytest
from common.log import log
from po.event import Event
from po.home_page import HomePage
from settings import *


@pytest.fixture(scope="class")
def login():
    global driver
    driver = HomePage()
    Event.event_login(driver, ENV.user_name, ENV.pass_word)
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def open_homepage():
    global driver
    driver = HomePage()
    driver.get(ENV.url)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 失败后执行
    :param item: 测试用例
    :param call: 测试步骤
    :return:
    """
    out = yield
    result = out.get_result()
    log.info(f"test report:{result}")
    log.info(f"execution time-consuming:{round(call.duration, 2)} second")
    # if result.failed and result.when == 'call':
    if result.failed:
        try:
            log.info('error.screenshot.')
            driver.allure_save_screenshot('error_screenshot')
        except Exception as e:
            log.error(e)
            pass
