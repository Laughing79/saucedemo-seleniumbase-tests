"""
结算全流程测试用例
"""

from conftest import MyTestBase
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckout(MyTestBase):

    def _login_and_go_to_checkout(self):
        """辅助：登录 → 加购 1 个 → 进购物车 → 点 Checkout"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")

        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.add_item_to_cart(0)

        cart = CartPage(self)
        inventory.go_to_cart()
        cart.wait_for_page_load()
        cart.click_checkout()

        return CheckoutPage(self)

    def test_01_checkout_success(self):
        """完整结算流程：填信息 → 确认 → 下单成功"""
        checkout = self._login_and_go_to_checkout()
        checkout.fill_info("Zhang", "San", "100000")
        checkout.click_continue()
        checkout.click_finish()
        checkout.assert_order_complete()

    def test_02_missing_first_name(self):
        """缺 First Name 应报错"""
        checkout = self._login_and_go_to_checkout()
        checkout.fill_info("", "San", "100000")
        checkout.click_continue()
        checkout.assert_error_contains("Error: First Name is required")

    def test_03_total_correct(self):
        """总价 = 商品小计 + 税"""
        checkout = self._login_and_go_to_checkout()
        checkout.fill_info("Zhang", "San", "100000")
        checkout.click_continue()
        checkout.assert_total_correct()

    # ============================================================
    # 下面由你补充 2 条：
    # 1. 缺 Last Name → 报错 "Error: Last Name is required"
    # 2. 缺 Postal Code → 报错 "Error: Postal Code is required"
    # 模板参考 test_02_missing_first_name
    # ============================================================
    def test_04_missing_last_name(self):
        checkout = self._login_and_go_to_checkout()
        checkout.fill_info("Zhang", "", "100000")
        checkout.click_continue()
        checkout.assert_error_contains("Error: Last Name is required")
    def test_05_missing_PostalCode(self):
        checkout = self._login_and_go_to_checkout()
        checkout.fill_info("Zhang", "San", "")
        checkout.click_continue()
        checkout.assert_error_contains("Error: Postal Code is required")
