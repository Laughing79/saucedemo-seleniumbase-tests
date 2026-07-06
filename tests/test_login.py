"""
tests/test_login.py —— 登录模块测试用例

覆盖场景：
1. 正常登录（standard_user）
2. 锁定用户（locked_out_user）
3. 密码错误
4. 用户名为空
5. 密码为空
"""

from conftest import MyTestBase
from pages.login_page import LoginPage


class TestLogin(MyTestBase):
    """登录模块测试"""

    def test_01_login_success(self):
        """正例：正确的用户名密码，应跳转到商品列表页"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        login_page.assert_login_success()

    def test_02_login_locked_out(self):
        """反例：被锁定的用户，显示锁定错误"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("locked_out_user", "secret_sauce")
        login_page.assert_error_contains(
            "Epic sadface: Sorry, this user has been locked out."
        )

    def test_03_login_wrong_password(self):
        """反例：密码错误，显示密码不匹配"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("standard_user", "wrong_password")
        login_page.assert_error_contains(
            "Epic sadface: Username and password do not match any user in this service"
        )

    def test_04_login_empty_username(self):
        """反例：用户名为空，显示必填提示"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("", "secret_sauce")
        login_page.assert_error_contains(
            "Epic sadface: Username is required"
        )

    def test_05_login_empty_password(self):
        """反例：密码为空，显示必填提示"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("standard_user", "")
        login_page.assert_error_contains(
            "Epic sadface: password is required"
        )
