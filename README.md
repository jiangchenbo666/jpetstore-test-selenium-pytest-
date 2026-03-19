# JPetStore 自动化测试项目

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.0-green)
![Pytest](https://img.shields.io/badge/Pytest-7.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 项目简介

基于 **Selenium + Pytest + Page Object 模式** 的 JPetStore 电商平台自动化测试项目。覆盖**登录、搜索、购物车、订单**四大核心模块，实现30+测试用例，包含正向场景、异常场景、边界条件测试。

本项目采用**企业级测试架构**，代码清晰、可维护性强，可直接用于回归测试和持续集成。

## 🛠️ 技术栈

- **编程语言**：Python 3.8+
- **测试框架**：Pytest 7.0
- **UI自动化**：Selenium 4.0
- **设计模式**：Page Object Model
- **测试报告**：Allure / Pytest-HTML
- **版本控制**：Git / GitHub
- **测试管理**：禅道

## 📁 项目结构
petstore_test/
├── pages/ # 页面对象层（PO模式）
│ ├── base_page.py # 基类（封装通用方法）
│ ├── login_page.py # 登录页
│ ├── home_page.py # 首页
│ ├── search_page.py # 搜索页
│ ├── product_page.py # 商品详情页
│ ├── cart_page.py # 购物车页
│ └── order_page.py # 订单页
├── tests/ # 测试用例层
│ ├── test_login.py # 登录模块测试
│ ├── test_search.py # 搜索模块测试
│ ├── test_cart.py # 购物车模块测试
│ └── test_order.py # 订单模块测试
├── conftest.py # Pytest全局配置
├── pytest.ini # Pytest配置文件
├── requirements.txt # 依赖包清单
└── README.md # 项目说明

text

## 🚀 如何运行

### 环境准备

1. **克隆项目**
   ```bash
   git clone https://github.com/jiangchenbo666/jpetstore-test-selenium-pytest.git
   cd jpetstore-test-selenium-pytest
安装依赖

bash
pip install -r requirements.txt
配置Edge驱动

下载 Edge 驱动（版本需与浏览器一致）

将驱动放在 drivers/ 目录下或配置环境变量

运行测试
运行所有测试

bash
pytest tests/ -v
运行指定模块

bash
pytest tests/test_login.py -v
生成测试报告

bash
pytest tests/ --html=reports/report.html



## 📸 测试结果截图

![测试报告](## 📸 测试结果截图

![测试报告](https://github.com/jiangchenbo666/jpetstore-test-selenium-pytest/blob/main/images/test_report.png?raw=true)
