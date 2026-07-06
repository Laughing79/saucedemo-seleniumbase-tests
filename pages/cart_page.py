"""
CartPage —— 购物车页面对象
"""

from pages.base_page import BasePage


class CartPage(BasePage):
    # ========== 元素定位器 ==========
    CART_ITEMS = ".cart_item"
    ITEM_NAMES = ".inventory_item_name"
    REMOVE_BTN = 'button[id^="remove"]'
    CONTINUE_SHOPPING = "#continue-shopping"
    CHECKOUT_BTN = "#checkout"

    def wait_for_page_load(self):
        """等待购物车页加载"""
        self.wait_for_visible(self.CHECKOUT_BTN)
        return self

    def get_item_count(self) -> int:
        """获取购物车中商品数量"""
        return len(self.sb.find_elements(self.CART_ITEMS))

    def get_item_names(self) -> list:
        """获取购物车中所有商品名称"""
        elements = self.sb.find_elements(self.ITEM_NAMES)
        return [el.text for el in elements]

    def remove_item(self, index: int = 0):
        """移除购物车中第 index 个商品"""
        buttons = self.sb.find_elements(self.REMOVE_BTN)
        if index < len(buttons):
            buttons[index].click()

    def click_continue_shopping(self):
        """点击 Continue Shopping → 返回商品列表"""
        self.click_element(self.CONTINUE_SHOPPING)

    def click_checkout(self):
        """点击 Checkout → 进入结算页"""
        self.click_element(self.CHECKOUT_BTN)

    def assert_item_count(self, expected: int):
        actual = self.get_item_count()
        self.assert_text_equal(
            str(actual), str(expected),
            f"Cart should have {expected} items, but got {actual}"
        )

    def assert_item_in_cart(self, item_name: str):
        """断言购物车中包含指定商品"""
        names = self.get_item_names()
        self.sb.assert_true(
            item_name in names,
            f"Cart should contain '{item_name}', but got: {names}"
        )
