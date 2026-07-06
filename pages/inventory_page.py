"""
InventoryPage —— SauceDemo 商品列表页面对象

封装商品列表页的元素和操作：
- 商品列表加载验证
- 排序（价格/名称）
- 添加/移除商品
- 购物车徽标读取
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    # ========== 元素定位器 ==========
    PRODUCT_SORT_DROPDOWN = ".product_sort_container"
    PRODUCT_ITEMS = ".inventory_item"
    PRODUCT_NAMES = ".inventory_item_name"
    PRODUCT_PRICES = ".inventory_item_price"
    ADD_TO_CART_BTN = 'button[id^="add-to-cart"]'
    REMOVE_BTN = 'button[id^="remove"]'
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    # ========== 页面加载 ==========

    def wait_for_page_load(self):
        """等待商品列表页加载完成"""
        self.wait_for_visible(self.PRODUCT_SORT_DROPDOWN)
        return self

    # ========== 排序操作 ==========

    def sort_by(self, option: str):
        """
        选择排序方式
        option 可选值:
          'az'       → Name (A to Z)
          'za'       → Name (Z to A)
          'lohi'     → Price (low to high)
          'hilo'     → Price (high to low)
        """
        # 直接构造 CSS 选择器定位 option 元素
        option_selector = f'option[value="{option}"]'
        self.sb.click(self.PRODUCT_SORT_DROPDOWN)
        self.sb.click(option_selector)
        return self

    # ========== 数据读取 ==========

    def get_product_count(self) -> int:
        """获取商品总数"""
        return len(self.sb.find_elements(self.PRODUCT_ITEMS))

    def get_all_product_names(self) -> list:
        """获取所有商品名称列表"""
        elements = self.sb.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_all_product_prices(self) -> list:
        """获取所有商品价格列表（float）"""
        elements = self.sb.find_elements(self.PRODUCT_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    # ========== 购物车操作 ==========

    def add_item_to_cart(self, index: int = 0):
        """添加第 index 个商品到购物车（按商品容器定位，避免按钮索引漂移）"""
        items = self.sb.find_elements(self.PRODUCT_ITEMS)
        if index < len(items):
            # 从商品容器内找 Add to Cart 按钮，不受其他商品按钮变化影响
            btn = items[index].find_elements(By.CSS_SELECTOR, 'button[id^="add-to-cart"]')
            if btn:
                btn[0].click()

    def add_items_to_cart(self, count: int):
        """添加前 count 个商品到购物车"""
        for i in range(count):
            self.add_item_to_cart(i)

    def remove_item_from_cart(self, index: int = 0):
        """从购物车移除第 index 个商品"""
        items = self.sb.find_elements(self.PRODUCT_ITEMS)
        if index < len(items):
            btn = items[index].find_elements(By.CSS_SELECTOR, 'button[id^="remove"]')
            if btn:
                btn[0].click()

    def get_cart_count(self) -> int:
        """获取购物车徽标数字（空购物车返回 0）"""
        if self.sb.is_element_visible(self.CART_BADGE):
            return int(self.sb.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        """点击购物车图标，跳转到购物车页"""
        self.sb.click(self.CART_LINK)

    # ========== 断言 ==========

    def assert_product_count(self, expected_count: int):
        """断言商品数量"""
        actual = self.get_product_count()
        self.assert_text_equal(
            str(actual), str(expected_count),
            f"Product count should be {expected_count}, but got {actual}"
        )

    def assert_sorted_by_name_asc(self):
        """断言商品按名称 A→Z 排序"""
        names = self.get_all_product_names()
        self.sb.assert_true(
            names == sorted(names),
            f"Names should be sorted A→Z, got: {names}"
        )

    def assert_sorted_by_name_desc(self):
        """断言商品按名称 Z→A 排序"""
        names = self.get_all_product_names()
        self.sb.assert_true(
            names == sorted(names, reverse=True),
            f"Names should be sorted Z→A, got: {names}"
        )

    def assert_sorted_by_price_asc(self):
        """断言商品按价格 低→高 排序"""
        prices = self.get_all_product_prices()
        self.sb.assert_true(
            prices == sorted(prices),
            f"Prices should be sorted low→high, got: {prices}"
        )

    def assert_sorted_by_price_desc(self):
        """断言商品按价格 高→低 排序"""
        prices = self.get_all_product_prices()
        self.sb.assert_true(
            prices == sorted(prices, reverse=True),
            f"Prices should be sorted high→low, got: {prices}"
        )

    def assert_cart_count(self, expected: int):
        """断言购物车徽标数字"""
        actual = self.get_cart_count()
        self.assert_text_equal(
            str(actual), str(expected),
            f"Cart count should be {expected}, but got {actual}"
        )

    def assert_items_removable(self):
        """断言商品可移除（REMOVE 按钮可见）"""
        self.assert_element_visible(self.REMOVE_BTN)
