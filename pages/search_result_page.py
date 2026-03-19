from selenium.webdriver.common.by import By
from .base_page import BasePage


class SearchResultPage(BasePage):
    """搜索结果页"""

    PRODUCT_LINKS = (By.CSS_SELECTOR, "td a")
    NO_RESULT_MSG = (By.CSS_SELECTOR, "div.messages li")

    def has_results(self):
        """是否有搜索结果（不看具体数量）"""
        try:
            # 等待一下看是否有商品链接
            self.wait.until(
                EC.presence_of_element_located(self.PRODUCT_LINKS)
            )
            return True
        except:
            return False

    def has_no_result(self):
        """是否显示无结果提示"""
        try:
            msg = self.get_text(self.NO_RESULT_MSG)
            return "No results" in msg
        except:
            return False

    def get_product_count(self):
        """获取结果数量（备用，但不用来做断言）"""
        return len(self.find_elements(self.PRODUCT_LINKS))

    def click_first_product(self):
        """点击第一个商品进入详情页"""
        products = self.find_elements(self.PRODUCT_LINKS)
        if products and len(products) > 0:
            products[0].click()
            from .product_page import ProductPage
            return ProductPage(self.driver)
        return None

    def wait_for_results(self, timeout=10):
        """
        等待搜索结果加载完成
        企业级做法：明确知道页面状态后再操作
        """
        try:
            # 等待商品链接出现（有结果）
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PRODUCT_LINKS)
            )
            self._has_results = True
        except:
            # 可能没有结果，检查无结果提示
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(self.NO_RESULT_MSG)
                )
                self._has_results = False
            except:
                # 真的超时了
                raise Exception("搜索结果页加载超时")
        return self

    def has_results(self):
        """是否有搜索结果"""
        return hasattr(self, '_has_results') and self._has_results