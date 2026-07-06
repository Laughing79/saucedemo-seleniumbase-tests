"""
购物车测试用例
"""

from conftest import MyTestBase
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart(MyTestBase):

    def _login_and_add_items(self, count: int = 1):
        """辅助：登录 → 添加 count 个商品 → 记录名称 → 进入购物车
        返回 (cart, added_names)
            cart:       CartPage 对象
            added_names: 添加的商品名称列表（跳转前记录，之后仍可用）
        """
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")

        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        # 在跳转到购物车之前，先记录要加购的商品名称
        added_names = inventory.get_all_product_names()[:count]
        inventory.add_items_to_cart(count)

        cart = CartPage(self)
        inventory.go_to_cart()
        cart.wait_for_page_load()
        return cart, added_names

    def test_01_cart_has_items(self):
        """添加 2 个商品，购物车应有 2 个"""
        cart, _ = self._login_and_add_items(2)
        cart.assert_item_count(2)

    def test_02_remove_item(self):
        """添加 1 个后移除，购物车应空"""
        cart, _ = self._login_and_add_items(1)
        cart.remove_item(0)
        cart.assert_item_count(0)

    def test_03_continue_shopping(self):
        """Continue Shopping 应返回商品列表页"""
        cart, _ = self._login_and_add_items(1)
        cart.click_continue_shopping()
        # 此时页面回到商品列表，创建新的 InventoryPage 对象
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.assert_product_count(6)

    # ============================================================
    # 下面由你补充：
    # _login_and_add_items 返回 (cart, added_names)
    #   cart        → 购物车页对象
    #   added_names → 添加时记录的商品名称列表
    # 用 cart.get_item_names() 和 added_names 做对比断言
    # ============================================================

    def test_04_item_name_matches(self):
        cart, added_names = self._login_and_add_items(2)
        for name in added_names:
            cart.assert_item_in_cart(name)