import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    """每个测试函数提供driver实例"""
    print("🚀 启动浏览器...")
    driver = webdriver.Edge()
    driver.maximize_window()
    yield driver
    print("🔚 关闭浏览器...")
    driver.quit()