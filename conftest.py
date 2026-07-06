from seleniumbase import BaseCase
import allure
import pytest


class MyTestBase(BaseCase):
    """所有测试类的父类。"""
    pass


# 用例失败自动截图并附加到allure报告
@pytest.fixture(autouse=True)
def screenshot_when_fail(request):
    yield
    # 判断当前用例执行失败
    if request.node.rep_call.failed:
        # 获取seleniumbase浏览器驱动
        web_driver = request.instance.sb.driver
        # 截取页面图片二进制
        img_data = web_driver.get_screenshot_as_png()
        # 挂载图片到allure报告附件
        allure.attach(
            img_data,
            name="失败页面截图",
            attachment_type=allure.attachment_type.PNG
        )


# 必须保留：记录用例执行成功/失败状态
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    execute_result = yield
    report = execute_result.get_result()
    setattr(item, "rep_" + report.when, report)