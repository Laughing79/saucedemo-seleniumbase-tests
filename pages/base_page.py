"""
BasePage —— 所有页面对象的基类
"""

import os
import time

import allure
from seleniumbase import BaseCase


class BasePage:
    def __init__(self, sb: BaseCase):
        self.sb = sb

    # ========== 基础操作 ==========

    def open_page(self, url: str):
        self.sb.open(url)

    def get_title(self) -> str:
        return self.sb.get_title()

    def get_current_url(self) -> str:
        return self.sb.get_current_url()

    # ========== 元素交互 ==========

    def type_text(self, selector: str, text: str):
        self.sb.type(selector, text)

    def click_element(self, selector: str):
        self.sb.click(selector)

    def get_text(self, selector: str) -> str:
        return self.sb.get_text(selector)

    # ========== 等待 ==========

    def wait_for_visible(self, selector: str, timeout: int = 10):
        self.sb.wait_for_element_visible(selector, timeout=timeout)

    def wait_for_url_contains(self, partial_url: str, timeout: int = 10):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if partial_url in self.sb.get_current_url():
                return
            time.sleep(0.5)
        raise TimeoutError(
            f"URL did not contain '{partial_url}' within {timeout}s. "
            f"Current URL: {self.sb.get_current_url()}"
        )

    # ========== 断言（失败自动截图 + 附加 Allure） ==========

    def _do_assert(self, assert_fn):
        try:
            assert_fn()
        except Exception:
            self._capture_failure()
            raise

    def _capture_failure(self):
        """失败时截图 + 附加到 Allure（此处浏览器绝对开着）"""
        try:
            os.makedirs("screenshots", exist_ok=True)
            filename = f"FAILED_{int(time.time())}.png"
            filepath = os.path.join("screenshots", filename)
            self.sb.save_screenshot(filepath)
            print(f"\n📸 失败截图: {filepath}")

            # 附加到 Allure
            allure.attach.file(
                filepath,
                name="失败截图",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print(f"\n⚠️ 截图失败: {e}")

    def assert_url_contains(self, expected: str):
        def _check():
            current = self.sb.get_current_url()
            if expected not in current:
                raise AssertionError(
                    f"URL should contain '{expected}', but got '{current}'"
                )
        self._do_assert(_check)

    def assert_element_visible(self, selector: str):
        self._do_assert(lambda: self.sb.assert_element_visible(selector))

    def assert_text_visible(self, text: str, selector: str = "body"):
        self._do_assert(lambda: self.sb.assert_text_visible(text, selector))

    def assert_text_equal(self, actual: str, expected: str, message: str = ""):
        def _check():
            if actual != expected:
                raise AssertionError(message or f"Expected '{expected}', got '{actual}'")
        self._do_assert(_check)

    # ========== 截图 ==========

    def take_screenshot(self, name: str):
        self.sb.save_screenshot(f"screenshots/{name}")
