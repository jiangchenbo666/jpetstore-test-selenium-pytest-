from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support.ui import Select
import time


class PaymentPage(BasePage):
    """支付信息页 - 基于真实源代码"""

    # ===== 准确定位器（直接从源代码复制）=====
    CARD_TYPE = (By.NAME, "order.cardType")
    CARD_NUMBER = (By.NAME, "order.creditCard")
    EXPIRY_DATE = (By.NAME, "order.expiryDate")
    FIRST_NAME = (By.NAME, "order.billToFirstName")
    LAST_NAME = (By.NAME, "order.billToLastName")
    ADDRESS1 = (By.NAME, "order.billAddress1")
    ADDRESS2 = (By.NAME, "order.billAddress2")
    CITY = (By.NAME, "order.billCity")
    STATE = (By.NAME, "order.billState")
    ZIP = (By.NAME, "order.billZip")
    COUNTRY = (By.NAME, "order.billCountry")
    CONTINUE_BTN = (By.NAME, "newOrder")
    SHIP_CHECKBOX = (By.NAME, "shippingAddressRequired")

    def fill_payment_info(self, card_type="Visa", card_number="999 9999 9999 9999",
                          expiry="12/03", first="ABC", last="XYZ",
                          addr1="901 San Antonio Road", addr2="MS UCUP02-206",
                          city="Palo Alto", state="CA", zip="94303", country="USA"):
        """填写支付信息"""
        print("   [调试] 开始填写支付信息")

        # 等待页面加载
        time.sleep(2)

        # 1. 选择卡类型
        try:
            select_element = self.find_element(self.CARD_TYPE)
            select = Select(select_element)
            select.select_by_visible_text(card_type)
            print(f"   ✅ 选择卡类型: {card_type}")
        except Exception as e:
            print(f"   ❌ 选择卡类型失败: {e}")

        # 2. 输入卡号
        self.enter_text(self.CARD_NUMBER, card_number)
        print(f"   ✅ 输入卡号")

        # 3. 输入有效期
        self.enter_text(self.EXPIRY_DATE, expiry)
        print(f"   ✅ 输入有效期")

        # 4. 输入账单地址
        self.enter_text(self.FIRST_NAME, first)
        self.enter_text(self.LAST_NAME, last)
        self.enter_text(self.ADDRESS1, addr1)
        self.enter_text(self.ADDRESS2, addr2)
        self.enter_text(self.CITY, city)
        self.enter_text(self.STATE, state)
        self.enter_text(self.ZIP, zip)
        self.enter_text(self.COUNTRY, country)
        print(f"   ✅ 填写地址信息")

        return self

    def click_continue(self):
        """点击继续按钮"""
        print("   [调试] 点击Continue按钮")
        self.click(self.CONTINUE_BTN)
        time.sleep(2)
        from .order_page import OrderPage
        return OrderPage(self.driver)

    def ship_to_different_address(self):
        """勾选'寄送到不同地址'复选框"""
        self.click(self.SHIP_CHECKBOX)
        return self