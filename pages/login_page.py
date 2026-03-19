from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):
    """登录页面对象"""

    # 定位器
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "signon")
    REGISTER_LINK = (By.LINK_TEXT, "Register Now!")

    # 错误消息可能有多种
    ERROR_MSG_1 = (By.CSS_SELECTOR, "ul.messages li")  # 一种错误提示
    ERROR_MSG_2 = (By.CSS_SELECTOR, "span.error")  # 另一种错误提示

    def login(self, username, password):
        """执行登录操作"""
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def login_success(self, username, password):
        """登录成功场景"""
        self.login(username, password)
        from .home_page import HomePage
        return HomePage(self.driver)

    def login_fail(self, username, password):
        """登录失败场景"""
        self.login(username, password)
        return self

    def get_error_message(self):
        """
        获取错误提示
        改进：尝试多种可能的错误消息元素
        """
        # 等待一下，让错误消息出现
        import time
        time.sleep(1)

        # 尝试第一种错误消息
        try:
            if self.is_element_present(self.ERROR_MSG_1):
                return self.get_text(self.ERROR_MSG_1)
        except:
            pass

        # 尝试第二种错误消息
        try:
            if self.is_element_present(self.ERROR_MSG_2):
                return self.get_text(self.ERROR_MSG_2)
        except:
            pass

        # 如果都没有，返回空字符串
        return ""

    def is_element_present(self, locator):
        """判断元素是否存在（不抛异常）"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def login_and_verify(self, username, password, expected_type="error_message"):
        """
        登录并智能验证结果

        Args:
            username: 用户名
            password: 密码
            expected_type:
                - "error_message": 期望有错误消息（用于错误密码/用户名）
                - "refresh_only": 期望只刷新页面（用于空字段）
        """
        import time
        self.login(username, password)
        time.sleep(1)  # 等待响应

        if expected_type == "error_message":
            error_msg = self.get_error_message()
            assert error_msg != "", "期望有错误消息但没找到"
            return error_msg
        else:  # refresh_only
            # 验证还在登录页（检查URL包含登录相关关键词）
            current_url = self.driver.current_url
            login_keywords = ["Account", "signonForm", "signon", "login"]
            assert any(keyword in current_url for keyword in login_keywords), \
                f"页面跳转了，期望停留在登录页。当前URL: {current_url}"
            return None

    def login_and_wait_for_success(self, username, password, timeout=10):
        """
        登录并等待登录成功
        企业级做法：必须确认登录成功才能继续
        """
        self.login(username, password)

        # 等待页面出现登录成功的特征
        try:
            # 方式1：等待 Welcome 信息
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome')]"))
            )
        except:
            # 方式2：等待 URL 变化（不再是登录页）
            try:
                WebDriverWait(self.driver, timeout).until(
                    lambda d: "signonForm" not in d.current_url
                )
            except:
                raise Exception("登录失败：未检测到登录成功特征")

        return HomePage(self.driver)