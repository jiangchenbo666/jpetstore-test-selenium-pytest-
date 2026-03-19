from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """首页对象"""

    # 定位器
    SIGN_IN_LINK = (By.LINK_TEXT, "Sign In")
    SEARCH_INPUT = (By.NAME, "keyword")
    SEARCH_BUTTON = (By.NAME, "searchProducts")

    def go_to_login(self):
        """点击Sign In进入登录页"""
        self.click(self.SIGN_IN_LINK)
        from .login_page import LoginPage
        return LoginPage(self.driver)

    def search(self, keyword):
        """搜索商品"""
        self.enter_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        from .search_result_page import SearchResultPage
        return SearchResultPage(self.driver)

    def wait_for_page_ready(self, timeout=10):
        """
        等待首页加载完成
        企业级做法：确保页面所有核心元素都可操作
        """
        # 等待搜索框可用
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        # 等待 Sign In 链接可用（如果没登录）
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.SIGN_IN_LINK)
            )
        except:
            pass  # 可能已经登录了
        return self