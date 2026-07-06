"""
tests/test_inventory.py —— 商品列表页测试用例

覆盖场景：
1. 商品列表加载（6 个商品）
2. 名称排序 A→Z
3. 名称排序 Z→A
4. 价格排序 低→高
5. 价格排序 高→低
6. 添加单个商品到购物车
7. 添加多个商品 → 购物车徽标
8. 移除商品 → 购物车徽标递减

每个用例先登录，再操作，保证独立可运行。
"""

from conftest import MyTestBase
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventory(MyTestBase):
    """商品列表页测试"""

    def _login(self):
        """辅助方法：登录并进入商品列表页"""
        login_page = LoginPage(self)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")

    def test_01_product_list_loaded(self):
        """商品列表页应加载 6 个商品"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.assert_product_count(6)

    def test_02_sort_by_name_asc(self):
        """排序：名称 A→Z"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.sort_by("az")
        inventory.assert_sorted_by_name_asc()

    def test_03_sort_by_name_desc(self):
        """排序：名称 Z→A"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.sort_by("za")
        inventory.assert_sorted_by_name_desc()

    def test_04_sort_by_price_asc(self):
        """排序：价格 低→高"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.sort_by("lohi")
        inventory.assert_sorted_by_price_asc()

    # ============================================================
    # 下面 4 条由你完成：排序高→低，加购1个，加购多个，移除商品
    # ============================================================

    def test_05_sort_by_price_desc(self):
        """排序：价格 高→低"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.sort_by("hilo")
        inventory.assert_sorted_by_price_desc()

    def test_06_add_single_item(self):
        """添加 1 个商品到购物车，徽标应显示 1"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.add_item_to_cart(0)
        inventory.assert_cart_count(1)

    def test_07_add_multiple_items(self):
        """添加 3 个商品到购物车，徽标应显示 3"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.add_items_to_cart(3)
        inventory.assert_cart_count(3)

    def test_08_remove_item(self):
        """添加 1 个后移除，徽标应归零"""
        self._login()
        inventory = InventoryPage(self)
        inventory.wait_for_page_load()
        inventory.add_item_to_cart(0)
        inventory.remove_item_from_cart(0)
        inventory.assert_cart_count(0)
