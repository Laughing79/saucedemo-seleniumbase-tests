"""
LoginPage —— SauceDemo 登录页面对象

封装登录页的所有元素定位和操作：
- 输入用户名 / 密码
- 点击登录
- 获取错误提示
- 一步登录（组合操作）
"""

from pages.base_page import BasePage


class LoginPage(BasePage):
    # ========== 构造 ==========
    URL = "https://www.saucedemo.com"

    # ========== 元素定位器（集中管理，改一处全局生效） ==========
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = '[data-test="error"]'

    # ========== 页面操作 ==========

    def navigate(self):
        """打开登录页"""
        self.open_page(self.URL)
        return self

    def enter_username(self, username: str):
        """输入用户名"""
        self.type_text(self.USERNAME_INPUT, username)
        return self  # 返回 self 实现链式调用

    def enter_password(self, password: str):
        """输入密码"""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """点击 Login 按钮"""
        self.click_element(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """
        一步完成登录（组合操作）

        Args:
            username: 用户名
            password: 密码
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ========== 结果获取 ==========

    def get_error_text(self) -> str:
        """
        获取页面上显示的错误提示文本
        返回空字符串表示没有错误
        """
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """判断错误提示是否显示"""
        return self.sb.is_element_visible(self.ERROR_MESSAGE)

    # ========== 断言 ==========

    def assert_login_success(self):
        """
        断言登录成功：URL 应跳转到 /inventory.html
        """
        self.wait_for_url_contains("/inventory.html", timeout=5)
        self.assert_url_contains("/inventory.html")

    def assert_error_contains(self, expected_text: str):
        """
        断言错误提示包含指定文本
        """
        error = self.get_error_text()
        self.assert_text_equal(
            error, expected_text,
            f"Error message should be '{expected_text}', but got '{error}'"
        )
