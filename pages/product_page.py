from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    """商品详情页"""

    PRODUCT_NAME = (By.CSS_SELECTOR, "h2")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "td.price")
    ADD_TO_CART_BTN = (By.LINK_TEXT, "Add to Cart")

    def get_product_name(self):
        """获取商品名称"""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self):
        """获取商品价格"""
        return self.get_text(self.PRODUCT_PRICE)

    def add_to_cart(self):
        """加入购物车"""
        self.click(self.ADD_TO_CART_BTN)
        from .cart_page import CartPage
        return CartPage(self.driver)