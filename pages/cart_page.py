from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class CartPage(BasePage):
    """购物车页面 - 基于最新截图精准定位"""

    # ===== 精准定位器 =====
    # 商品行：所有表格行，排除表头
    CART_ITEMS = (By.CSS_SELECTOR, "table tr:not(:first-child)")

    # 数量输入框：在第4列
    ITEM_QUANTITY = (By.CSS_SELECTOR, "td:nth-child(4) input")

    # Remove链接：在最后一列（第7列）
    REMOVE_BTN = (By.CSS_SELECTOR, "td:last-child a")

    # Update Cart按钮
    UPDATE_CART_BTN = (By.CSS_SELECTOR, "input[value='Update Cart']")

    # 去结算
    PROCEED_CHECKOUT = (By.LINK_TEXT, "Proceed to Checkout")

    # 继续购物
    CONTINUE_SHOPPING = (By.LINK_TEXT, "Return to Main Menu")

    # ===== 业务方法 =====
    def get_item_count(self):
        """获取购物车商品数量"""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)

    def get_item_quantity(self, index=0):
        """获取指定商品数量"""
        print(f"   [调试] 开始查找数量输入框，使用定位器: {self.ITEM_QUANTITY}")

        # 等待一下
        time.sleep(2)

        # 打印所有td，看看第4列到底是什么
        all_tds = self.driver.find_elements(By.CSS_SELECTOR, "td")
        print(f"   [调试] 页面共有 {len(all_tds)} 个td")
        for i, td in enumerate(all_tds[:10]):  # 只打印前10个
            print(f"   [调试] td {i}: {td.text[:30]}")

        quantities = self.find_elements(self.ITEM_QUANTITY)
        print(f"   [调试] 找到 {len(quantities)} 个数量输入框")

        if quantities and len(quantities) > index:
            value = quantities[index].get_attribute("value")
            print(f"   [调试] 第 {index} 个数量值: {value}")
            return value
        return None

    def update_quantity(self, quantity, index=0):
        """修改商品数量"""
        quantities = self.find_elements(self.ITEM_QUANTITY)
        if quantities and len(quantities) > index:
            quantities[index].clear()
            quantities[index].send_keys(str(quantity))
            self.click(self.UPDATE_CART_BTN)
            time.sleep(1)
            return True
        raise Exception("无法找到数量输入框")

    def remove_item(self, index=0):
        """
        点击Remove链接删除商品，并返回当前页面的新CartPage对象
        注意：PetStore需要点击Update Cart才能生效
        """
        print(f"   [调试] 开始查找Remove按钮")

        # 等待一下，让页面稳定
        time.sleep(1)

        # 找所有的Remove链接（基于文本）
        all_links = self.driver.find_elements(By.CSS_SELECTOR, "td a")
        remove_links = [link for link in all_links if link.text == "Remove"]
        print(f"   [调试] 找到 {len(remove_links)} 个文本为'Remove'的链接")

        if remove_links and len(remove_links) > index:
            remove_links[index].click()
            print(f"   [调试] 点击了第 {index} 个Remove按钮")
            time.sleep(2)  # 等待页面刷新

            # 关键：点击Update Cart使删除生效
            try:
                update_btn = self.driver.find_element(*self.UPDATE_CART_BTN)
                update_btn.click()
                print(f"   [调试] 点击了Update Cart按钮")
                time.sleep(2)
            except:
                print(f"   [调试] 未找到Update Cart按钮，可能不需要")

            # 返回一个新的CartPage实例，代表刷新后的页面
            from .cart_page import CartPage
            return CartPage(self.driver)
        raise Exception("无法找到Remove按钮")

    def proceed_to_checkout(self):
        """去结算 - 进入支付信息页"""
        self.click(self.PROCEED_CHECKOUT)
        from .payment_page import PaymentPage  # 注意这里改成了 PaymentPage
        return PaymentPage(self.driver)

    def continue_shopping(self):
        """继续购物"""
        self.click(self.CONTINUE_SHOPPING)
        from .home_page import HomePage
        return HomePage(self.driver)

    def is_empty(self):
        """购物车是否为空"""
        return self.get_item_count() == 0