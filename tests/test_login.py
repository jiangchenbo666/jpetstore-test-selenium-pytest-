import pytest
from pages.home_page import HomePage


class TestLogin:
    """登录模块测试用例"""

    def test_login_success(self, driver):
        """正向用例：正确账号密码登录"""
        driver.get("https://petstore.octoperf.com/actions/Catalog.action")

        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        login_page.login("j2ee", "j2ee")

        # 验证登录成功（检查页面是否包含欢迎信息）
        assert "Welcome" in driver.page_source
        print("✅ 登录成功")

    def test_login_wrong_password(self, driver):
        """异常用例：密码错误"""
        driver.get("https://petstore.octoperf.com/actions/Catalog.action")

        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        login_page.login("j2ee", "wrong_password")

        # 获取错误消息
        error_msg = login_page.get_error_message()
        print(f"错误消息: '{error_msg}'")

        # 验证错误消息包含关键词
        assert "Invalid" in error_msg or "错误" in error_msg, f"错误消息不正确: {error_msg}"
        print("✅ 密码错误验证通过")

    @pytest.mark.parametrize("username,password,expected", [
        # ("", "j2ee", "required"),  # 空用户名
        # ("j2ee", "", "required"),  # 空密码
        ("wrong_user", "j2ee", "Invalid"),  # 错误用户名
        ("j2ee", "wrong", "Invalid"),  # 错误密码
    ])
    def test_login_multiple_scenarios(self, driver, username, password, expected):
        """数据驱动：多个异常场景"""
        print(f"\n测试数据: 用户名='{username}', 密码='{password}', 期望包含='{expected}'")

        driver.get("https://petstore.octoperf.com/actions/Catalog.action")

        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        login_page.login(username, password)

        # 获取错误消息
        error_msg = login_page.get_error_message()
        print(f"实际错误: '{error_msg}'")

        # 如果错误消息为空，可能是页面没显示错误（但也算测试失败）
        assert error_msg != "", "错误消息为空，页面可能没有正确显示错误"

        # 验证错误消息包含期望的关键词
        assert expected.lower() in error_msg.lower(), \
            f"期望包含'{expected}'，实际错误'{error_msg}'"

        print("✅ 验证通过")

    def test_login_empty_username(self, driver):
            """新增测试：空用户名 - 只刷新，无错误消息"""
            driver.get("https://petstore.octoperf.com/actions/Catalog.action")

            home_page = HomePage(driver)
            login_page = home_page.go_to_login()

            # 使用新增的智能验证方法
            login_page.login_and_verify("", "j2ee", expected_type="refresh_only")
            print("✅ 空用户名测试通过（页面刷新但未跳转）")

    def test_login_empty_password(self, driver):
            """新增测试：空密码 - 只刷新，无错误消息"""
            driver.get("https://petstore.octoperf.com/actions/Catalog.action")

            home_page = HomePage(driver)
            login_page = home_page.go_to_login()

            login_page.login_and_verify("j2ee", "", expected_type="refresh_only")
            print("✅ 空密码测试通过（页面刷新但未跳转）")