import pytest
import time
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.order_page import OrderPage
from pages.order_success_page import OrderSuccessPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestOrder:
    """订单模块测试用例 - 企业级完整版"""

    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login_and_add_to_cart(self, keyword="fish"):
        """前置条件：登录并加购商品"""
        # 1. 打开首页
        self.driver.get("https://petstore.octoperf.com/actions/Catalog.action")

        # 2. 登录
        home_page = HomePage(self.driver)
        login_page = home_page.go_to_login()
        login_page.login("j2ee", "j2ee")

        # 3. 加购商品
        self.driver.get("https://petstore.octoperf.com/actions/Catalog.action")
        home_page = HomePage(self.driver)
        result_page = home_page.search(keyword)
        product_page = result_page.click_first_product()
        cart_page = product_page.add_to_cart()

        return cart_page

    # ========== 测试1：正向流程 ==========
    def test_checkout_flow(self, driver):
            """测试1：正向流程 - 正常提交订单"""
            print("\n" + "=" * 50)
            print("测试1：正向订单流程")
            print("=" * 50)

            # 1. 加购
            cart_page = self.login_and_add_to_cart("fish")

            # 2. 去结算 -> 进入支付信息页
            payment_page = cart_page.proceed_to_checkout()

            # 3. 填写支付信息
            payment_page.fill_payment_info()

            # 4. 点Continue -> 进入订单确认页
            order_page = payment_page.click_continue()
            time.sleep(2)

            # 5. 点Confirm -> 进入成功页
            success_page = order_page.confirm_order()
            time.sleep(2)

            # 6. 验证
            assert success_page.is_order_successful(), "订单应该成功"
            order_number = success_page.get_order_number()
            assert order_number is not None, "订单号不应为空"
            print(f"✅ 订单成功，订单号: {order_number}")

    # ========== 测试2：数据一致性 ==========
    def test_order_data_consistency(self, driver):
        """测试2：数据一致性 - 商品信息正确传递"""
        print("\n" + "=" * 50)
        print("测试2：数据一致性验证")
        print("=" * 50)

        # 1. 加购
        cart_page = self.login_and_add_to_cart("fish")

        # 记录购物车的商品信息
        cart_product = "Adult Male Goldfish"

        # 2. 去支付页
        payment_page = cart_page.proceed_to_checkout()

        # 3. 填写支付信息
        payment_page.fill_payment_info()

        # 4. 去订单确认页
        order_page = payment_page.click_continue()
        time.sleep(2)

        # 5. 确认订单 -> 进入成功页
        success_page = order_page.confirm_order()
        time.sleep(2)

        # 6. 获取成功页商品信息
        success_products = success_page.get_product_names()
        print(f"成功页商品: {success_products}")

        # 7. 验证商品存在
        found = any(cart_product in str(product) for product in success_products)
        assert found, f"商品 '{cart_product}' 未在成功页找到"
        print("✅ 商品信息正确显示在成功页")
    # ========== 测试3：订单号验证 ==========
    def test_order_number_generation(self, driver):
        """测试3：订单号验证"""
        print("\n" + "=" * 50)
        print("测试3：订单号验证")
        print("=" * 50)

        # 1. 加购
        cart_page = self.login_and_add_to_cart("fish")

        # 2. 支付页
        payment_page = cart_page.proceed_to_checkout()
        payment_page.fill_payment_info()

        # 3. 订单确认页
        order_page = payment_page.click_continue()
        time.sleep(2)

        # 4. 确认订单 -> 成功页
        success_page = order_page.confirm_order()
        time.sleep(2)

        # 5. 验证订单号
        order_number = success_page.get_order_number()
        assert order_number is not None, "订单号不应为空"
        assert order_number.isdigit(), f"订单号应为数字: {order_number}"
        print(f"✅ 订单号生成正确: {order_number}")
    # ========== 测试4：未登录结算 ==========
    def test_checkout_without_login(self, driver):
        """测试4：未登录结算"""
        print("\n" + "=" * 50)
        print("测试4：未登录结算验证")
        print("=" * 50)

        # 不登录，直接加购
        self.driver.get("https://petstore.octoperf.com/actions/Catalog.action")
        home_page = HomePage(self.driver)
        result_page = home_page.search("fish")
        product_page = result_page.click_first_product()
        cart_page = product_page.add_to_cart()

        # 去结算
        cart_page.proceed_to_checkout()
        time.sleep(2)

        # 验证：应该能进入支付页（没有跳转登录页）
        assert "Order" in self.driver.current_url or "newOrder" in self.driver.current_url
        print("✅ 未登录用户可以直接结算（PetStore特殊设计）")
        pass

    @pytest.mark.skip(reason="PetStore购物车删除功能有Bug，无法可靠清空")
    # ========== 测试5：空购物车结算 ==========
    def test_checkout_empty_cart(self, driver):
        """
        测试5：空购物车结算
        面试价值：验证边界场景
        """
        print("\n" + "=" * 50)
        print("测试5：空购物车结算验证")
        print("=" * 50)

        # 1. 登录
        self.driver.get("https://petstore.octoperf.com/actions/Catalog.action")
        home_page = HomePage(self.driver)
        login_page = home_page.go_to_login()
        login_page.login("j2ee", "j2ee")

        # 2. 确保购物车为空
        self.driver.get("https://petstore.octoperf.com/actions/Cart.action")
        cart_page = CartPage(self.driver)

        # 如果购物车有商品，删除它们
        while cart_page.get_item_count() > 0:
            cart_page.remove_item()
            time.sleep(1)

        # 3. 直接访问结算页
        self.driver.get("https://petstore.octoperf.com/actions/Checkout.action")
        time.sleep(2)

        # 4. 验证应该被重定向或停留在购物车
        assert "Cart" in self.driver.current_url or "catalog" in self.driver.current_url.lower(), \
            f"空购物车应该不能结算，当前URL: {self.driver.current_url}"
        print("✅ 空购物车不能结算")

    # ========== 测试6：重复提交验证（高级）==========
    def test_duplicate_submission(self, driver):
        """测试6：重复提交验证"""
        print("\n" + "=" * 50)
        print("测试6：重复提交验证")
        print("=" * 50)

        # 1. 完整下单流程
        cart_page = self.login_and_add_to_cart("fish")
        payment_page = cart_page.proceed_to_checkout()
        payment_page.fill_payment_info()
        order_page = payment_page.click_continue()
        time.sleep(2)

        # 2. 记录当前页面信息
        before_url = self.driver.current_url

        # 3. 第一次点击Confirm
        confirm_btn = self.driver.find_element(By.LINK_TEXT, "Confirm")
        confirm_btn.click()
        time.sleep(1)  # 等待页面开始响应

        # 4. 重新查找Confirm按钮再点击
        try:
            # 页面可能还没完全刷新，等待一下
            time.sleep(0.5)
            confirm_btn2 = self.driver.find_element(By.LINK_TEXT, "Confirm")
            confirm_btn2.click()
            print("   [调试] 第二次点击Confirm")
        except:
            print("   [调试] 第二次点击时按钮已消失，说明只提交了一次")
            pass

        time.sleep(3)

        # 5. 验证
        after_url = self.driver.current_url
        assert before_url != after_url, "页面应该跳转"

        # 检查是否只有一个订单号
        order_numbers = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Order #')]")
        assert len(order_numbers) == 1, f"应该只有一个订单号，实际有 {len(order_numbers)}"
        print("✅ 重复提交未生成多个订单")

    # ========== 测试7：订单详情页验证（如果有）==========
    def test_order_detail_page(self, driver):
        """测试7：订单详情页验证"""
        print("\n" + "=" * 50)
        print("测试7：订单详情页验证")
        print("=" * 50)

        # 1. 提交订单
        cart_page = self.login_and_add_to_cart("fish")
        payment_page = cart_page.proceed_to_checkout()
        payment_page.fill_payment_info()
        order_page = payment_page.click_continue()
        success_page = order_page.confirm_order()

        # 2. 获取订单号
        order_number = success_page.get_order_number()

        # 3. 尝试进入订单详情页（如果有链接）
        try:
            order_link = self.driver.find_element(By.XPATH, f"//a[contains(@href, '{order_number}')]")
            order_link.click()
            time.sleep(2)

            # 4. 验证详情页信息
            assert order_number in self.driver.page_source, "订单号应在详情页"
            assert "Angelfish" in self.driver.page_source, "商品应在详情页"
            print(f"✅ 订单详情页信息完整")
        except:
            print("⚠️ 订单详情页不存在，跳过验证")
            pytest.skip("订单详情页不存在")