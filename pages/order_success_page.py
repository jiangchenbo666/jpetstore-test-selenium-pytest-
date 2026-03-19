from selenium.webdriver.common.by import By
from .base_page import BasePage
import re


class OrderSuccessPage(BasePage):
    """订单成功页"""

    # 定位器
    THANK_YOU_MSG = (By.XPATH, "//*[contains(text(), 'Thank you')]")
    ORDER_NUMBER = (By.XPATH, "//*[contains(text(), 'Order #')]")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "table tr td:nth-child(2)")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "table tr td:nth-child(4)")

    def is_order_successful(self):
        """是否订单成功"""
        try:
            return "Thank you" in self.get_text(self.THANK_YOU_MSG)
        except:
            return False

    def get_order_number(self):
        """获取订单号"""
        order_text = self.get_text(self.ORDER_NUMBER)
        # 使用正则提取数字
        match = re.search(r'#(\d+)', order_text)
        return match.group(1) if match else None

    def get_product_names(self):
        """获取所有商品名称"""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_prices(self):
        """获取所有商品价格"""
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [el.text for el in elements]