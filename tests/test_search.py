import pytest
from pages.home_page import HomePage
from selenium.webdriver.common.by import By


class TestSearch:
    """搜索模块测试用例"""

    @pytest.mark.parametrize("keyword", [
        "fish", "dog", "cat", "bird", "reptile"
    ])
    def test_search_returns_results_page(self, driver, keyword):
        """测试搜索任何关键词都能正常返回页面"""
        print(f"\n测试搜索: '{keyword}'")

        driver.get("https://petstore.octoperf.com/actions/Catalog.action")
        home_page = HomePage(driver)
        home_page.search(keyword)

        assert "JPetStore" in driver.title
        print("✅ 搜索页面加载正常")

    def test_search_results_are_clickable(self, driver):
        """测试搜索结果可点击进入详情页"""
        driver.get("https://petstore.octoperf.com/actions/Catalog.action")
        home_page = HomePage(driver)

        # 搜索fish
        result_page = home_page.search("fish")

        # 如果没结果，跳过
        if result_page.get_product_count() == 0:
            pytest.skip("当前 fish 搜索结果为空")

        # 点击第一个商品
        product_page = result_page.click_first_product()

        # 验证进入详情页
        assert product_page is not None
        product_name = product_page.get_product_name()
        assert product_name != ""
        print(f"✅ 成功进入商品详情页: {product_name}")

    def test_search_nonexistent_keyword(self, driver):
        """
        测试搜索不存在的商品
        验证重点：系统不崩溃，可继续操作
        """
        driver.get("https://petstore.octoperf.com/actions/Catalog.action")
        home_page = HomePage(driver)

        keyword = "thisproductdoesnotexist12345"
        result_page = home_page.search(keyword)

        # 验证1：页面标题正常（系统没崩溃）
        assert "JPetStore" in driver.title or "PetStore" in driver.title

        # 验证2：搜索框还在，而且保留了输入的内容
        search_input = driver.find_element(By.NAME, "keyword")
        assert search_input.get_attribute("value") == keyword

        # 验证3：页面核心元素都在（Sign In链接还在）
        sign_in_link = driver.find_element(By.LINK_TEXT, "Sign In")
        assert sign_in_link.is_displayed()

        print("✅ 搜索不存在商品，系统处理正常")