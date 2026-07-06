"""
tests/test_login_data_driven.py —— 登录模块数据驱动测试

与 test_login.py 的区别：
- test_login.py：每个场景一个方法，适合固定用例
- 本文件：一条方法遍历 JSON，新增数据只改 JSON 不碰代码
"""

import json
import os

from conftest import MyTestBase
from pages.login_page import LoginPage


def load_login_data():
    data_file = os.path.join(os.path.dirname(__file__), "..", "config", "login_test_data.json")
    data_file = os.path.abspath(data_file)
    with open(data_file, encoding="utf-8") as f:
        return json.load(f)


class TestLoginDataDriven(MyTestBase):

    def test_login_data_driven(self):
        """遍历 JSON 中所有数据行，正反例走不同断言路径"""
        all_rows = load_login_data()
        failed = []

        for i, row in enumerate(all_rows):
            print(f"\n=== [{i+1}/{len(all_rows)}] {row['scenario']} ===")

            login_page = LoginPage(self)
            login_page.navigate()
            login_page.login(row["username"], row["password"])

            try:
                if row["expected_success"]:
                    login_page.assert_login_success()
                else:
                    login_page.assert_error_contains(row["expected_error"])
                print(f"✅ PASSED")
            except AssertionError as e:
                failed.append(f"[{row['scenario']}] {e}")
                print(f"❌ FAILED: {e}")

        # 最后统一报告：有任何一个失败就整体失败
        if failed:
            self.sb.assert_true(False, f"\n{len(failed)} group(s) failed:\n" + "\n".join(failed))
