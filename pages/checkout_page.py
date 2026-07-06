"""
CheckoutPage —— 结算页面对象（含 Step1 填信息 + Step2 确认 + Complete 完成）
"""

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # ========== Step 1: 填写收货信息 ==========
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BTN = "#continue"
    ERROR_MESSAGE = '[data-test="error"]'

    # ========== Step 2: 确认订单 ==========
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    FINISH_BTN = "#finish"

    # ========== Complete: 完成页 ==========
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME = "#back-to-products"

    # ========== Step 1 操作 ==========

    def fill_info(self, first: str, last: str, postal: str):
        """填写收货信息"""
        self.type_text(self.FIRST_NAME_INPUT, first)
        self.type_text(self.LAST_NAME_INPUT, last)
        self.type_text(self.POSTAL_CODE_INPUT, postal)
        return self

    def click_continue(self):
        self.click_element(self.CONTINUE_BTN)

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    # ========== Step 2 操作 ==========

    def get_subtotal(self) -> float:
        text = self.get_text(self.ITEM_TOTAL)
        return float(text.replace("Item total: $", ""))

    def get_tax(self) -> float:
        text = self.get_text(self.TAX_LABEL)
        return float(text.replace("Tax: $", ""))

    def get_total(self) -> float:
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.replace("Total: $", ""))

    def click_finish(self):
        self.click_element(self.FINISH_BTN)

    # ========== Complete 操作 ==========

    def get_complete_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    # ========== 断言 ==========

    def assert_error_contains(self, expected: str):
        error = self.get_error_text()
        self.assert_text_equal(
            error, expected,
            f"Error should be '{expected}', got '{error}'"
        )

    def assert_total_correct(self):
        """断言 total ≈ subtotal + tax"""
        subtotal = self.get_subtotal()
        tax = self.get_tax()
        total = self.get_total()
        self.sb.assert_true(
            abs(total - (subtotal + tax)) < 0.01,
            f"Total ${total} should ≈ subtotal ${subtotal} + tax ${tax}"
        )

    def assert_order_complete(self):
        """断言下单成功"""
        self.wait_for_visible(self.COMPLETE_HEADER)
        self.assert_text_visible("Thank you for your order", self.COMPLETE_HEADER)
