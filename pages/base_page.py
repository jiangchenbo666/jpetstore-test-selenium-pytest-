from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """所有页面类的基类，封装公共方法"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 显式等待10秒

    def find_element(self, locator):
        """查找单个元素，等待元素出现"""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        """查找多个元素"""
        return self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator):
        """点击元素，等待元素可点击"""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """获取元素文本"""
        return self.find_element(locator).text

    def is_element_present(self, locator):
        """判断元素是否存在"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def select_by_visible_text(self, locator, text):
        """通过可见文本选择下拉框选项"""
        from selenium.webdriver.support.ui import Select
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)