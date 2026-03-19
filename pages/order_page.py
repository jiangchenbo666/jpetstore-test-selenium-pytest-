from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class OrderPage(BasePage):
    """订单确认页"""

    # 定位器 - 尝试多种可能
    CONFIRM_BTN_1 = (By.NAME, "confirm")
    CONFIRM_BTN_2 = (By.XPATH, "//input[@value='Confirm']")
    CONFIRM_BTN_3 = (By.XPATH, "//button[contains(text(), 'Confirm')]")
    CONFIRM_BTN_4 = (By.LINK_TEXT, "Confirm")

    PRODUCT_NAMES = (By.XPATH, "//table[contains(@summary, 'Order')]//td[2]")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "table tr td:nth-child(4)")

    def confirm_order(self):
        print("   [调试] 当前页面标题:", self.driver.title)
        print("   [调试] 当前URL:", self.driver.current_url)

        # 打印所有按钮
        buttons = self.driver.find_elements(By.TAG_NAME, "input")
        print(f"   [调试] 找到 {len(buttons)} 个input按钮")
        for btn in buttons:
            print(
                f"      type={btn.get_attribute('type')}, value={btn.get_attribute('value')}, name={btn.get_attribute('name')}")
        """点击确认订单（多定位器轮询）"""
        print("   [调试] 开始查找Confirm按钮")
        time.sleep(2)  # 等页面加载

        # 尝试多种定位器
        locators = [
            self.CONFIRM_BTN_1,
            self.CONFIRM_BTN_2,
            self.CONFIRM_BTN_3,
            self.CONFIRM_BTN_4,
        ]

        for locator in locators:
            try:
                print(f"   [调试] 尝试定位器: {locator}")
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    element.click()
                    print(f"   ✅ 点击Confirm按钮成功")
                    time.sleep(2)
                    from .order_success_page import OrderSuccessPage
                    return OrderSuccessPage(self.driver)
            except:
                continue

        raise Exception("找不到Confirm按钮")

    def get_product_names(self):
        """获取所有商品名称"""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_prices(self):
        """获取所有商品价格"""
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [el.text for el in elements]