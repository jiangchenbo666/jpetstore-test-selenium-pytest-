from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
import time


def test_visit_jpetstore():
    """测试能否打开JPetStore"""
    print("开始测试JPetStore...")

    # 自动下载并匹配Edge驱动
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    try:
        # 打开JPetStore（注意URL拼写：octoperf.com 不是 octopef.com）
        driver.get("https://petstore.octoperf.com/actions/Catalog.action")

        # 打印页面标题
        print(f"页面标题：{driver.title}")

        # 断言标题包含"JPetStore"
        assert "JPetStore" in driver.title or "PetStore" in driver.title

        print("✅ 测试通过！")
        time.sleep(2)

    finally:
        driver.quit()