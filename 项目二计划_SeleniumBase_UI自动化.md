# 项目二：SauceDemo UI 自动化测试框架 — 详细计划

> **目标系统**：SauceDemo（https://www.saucedemo.com）— 专为 QA 练习设计的电商网站
> **技术栈**：Python 3.12 + SeleniumBase 4.49 + pytest + Allure + Git + GitHub Actions
> **权限映射**：直接覆盖该岗位"UI 自动化脚本维护"+"Python 测试脚本"+"测试报告"+"缺陷分析"四条核心要求

---

## 🎯 本项目与岗位要求的直接映射

| 岗位要求 | 本项目的对应实践 | 产出证据 |
|----------|-----------------|----------|
| 具备 Selenium 实战经验，编写维护自动化脚本 | 用 SeleniumBase + POM 搭建 20+ 条用例的回归套件 | GitHub 仓库：完整框架源码 |
| 能用 Python 编写测试脚本或扩展工具 | 纯 Python OOP 设计，自定义 BasePage / fixtures / utilities | 可复用的 Page Object 基类 |
| 维护 Web/移动端 UI 自动化脚本，提升回归效率 | 覆盖电商核心业务全流程，支持一键回归 | CI 流水线跑通 |
| 搭建维护测试环境，管理测试数据 | 多环境配置切换 + JSON 数据文件驱动 | conftest.py + test_data/ |
| 输出测试报告，提供产品质量评估 | Allure 报告含通过率/失败截图/步骤追踪 | 报告样例截图 |
| 精准定位缺陷并推动修复，跟踪闭环问题 | 失败自动截图 + 日志定位根因 + Markdown Bug Report | Bug 报告模板 |
| 逻辑严谨，快速理解复杂业务 | 覆盖登录/排序/筛选/购物车/结算全业务流 | 测试用例设计文档 |

---

## 📁 最终项目结构（这是你要搭建出来的）

```
saucedemo-seleniumbase-tests/
├── README.md                          # 项目说明 + 运行指南
├── requirements.txt                   # Python 依赖
├── conftest.py                        # pytest 全局配置（fixture、浏览器、环境切换）
├── pytest.ini                         # pytest 运行参数
├── config/
│   ├── settings.py                    # 环境配置（URL、超时、浏览器类型）
│   └── test_data.json                 # 数据驱动测试数据
├── pages/
│   ├── base_page.py                   # 页面基类（通用操作封装）
│   ├── login_page.py                  # 登录页对象
│   ├── inventory_page.py              # 商品列表页对象
│   ├── cart_page.py                   # 购物车页对象
│   ├── checkout_page.py               # 结算页对象
│   └── checkout_overview_page.py      # 结算确认页对象
├── tests/
│   ├── test_login.py                  # 登录模块用例
│   ├── test_inventory.py              # 商品浏览/排序/筛选用例
│   ├── test_cart.py                   # 购物车操作用例
│   └── test_checkout.py               # 结算全流程用例
├── utilities/
│   ├── logger.py                      # 日志工具
│   └── report_helper.py               # 报告辅助（截图、步骤描述）
├── reports/                           # Allure 报告输出目录
├── screenshots/                       # 失败截图存档
├── bug_reports/                       # 缺陷报告模板
└── .github/
    └── workflows/
        └── run_tests.yml              # GitHub Actions 自动跑回归
```

---

## 📅 九步详细计划

---

### 第一步：框架地基 —— BasePage 基类设计（0.5 天）

**要做什么**：
创建 `pages/base_page.py`，把所有页面共用的操作封装进去。

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| SeleniumBase 基础 API | `self.open()` / `self.type()` / `self.click()` / `self.assert_element()` / `self.get_text()` |
| OOP 继承设计 | 所有 Page Object 继承 BasePage，避免重复代码 |
| 智能等待 | SeleniumBase 内置自动等待，不需要手写 `time.sleep()` |
| 错误处理 | 操作失败时自动截图，记录日志 |

**代码骨架**：

```python
# pages/base_page.py
from seleniumbase import BaseCase

class BasePage:
    def __init__(self, sb: BaseCase):
        self.sb = sb

    def navigate_to(self, url: str):
        """打开页面"""
        self.sb.open(url)

    def wait_for_page_load(self, selector: str):
        """等待页面加载完成"""
        self.sb.wait_for_element_visible(selector)

    def get_error_message(self):
        """获取错误提示文本"""
        return self.sb.get_text('[data-test="error"]')

    def take_screenshot(self, name: str):
        """截图（失败时自动调用）"""
        self.sb.save_screenshot(name)
```

---

### 第二步：登录页 —— 第一个 Page Object（0.5 天）

**要做什么**：
创建 `pages/login_page.py`，封装登录页的所有操作。

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| 元素定位策略 | `data-test` 属性定位 > CSS Selector > XPath（优先级） |
| Page Object 原则 | 页面操作封装为方法，不暴露元素选择器给测试用例 |
| 正例 + 反例 | 登录成功 / 密码错误 / 用户名错误 / 空字段 / 锁定的用户 |

**代码骨架**：

```python
# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    # 元素定位（集中管理，改一个地方全局生效）
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"
    ERROR_MESSAGE  = '[data-test="error"]'

    def enter_username(self, username: str):
        self.sb.type(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.sb.type(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.sb.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """一步完成登录"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_text(self):
        return self.sb.get_text(self.ERROR_MESSAGE)
```

---

### 第三步：pytest 集成 —— conftest.py 全局配置（0.5 天）

**要做什么**：
创建 `conftest.py` 和 `pytest.ini`，配置测试运行参数。

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| pytest fixture 机制 | setup / teardown 生命周期 |
| SeleniumBase + pytest | 继承 `BaseCase` 获得所有 SeleniumBase 能力 |
| 命令行参数 | `--headless` / `--browser=chrome` / `--demo-mode` |

**代码骨架**：

```python
# conftest.py
import pytest
from seleniumbase import BaseCase

class MyTestBase(BaseCase):
    """所有测试类的基类，统一配置"""
    def setUp(self):
        super().setUp()
        # 测试前置：打开被测网站
        self.base_url = "https://www.saucedemo.com"
```

```ini
# pytest.ini
[pytest]
addopts = -v -s --tb=short --html=reports/report.html
testpaths = tests/
python_files = test_*.py
```

---

### 第四步：登录测试用例 —— 第一批自动化脚本（1 天）

**要做什么**：
创建 `tests/test_login.py`，写 5 条登录相关的用例。

**SauceDemo 预设账号**（这是测试数据）：

| 用户名 | 密码 | 预期 |
|--------|------|:---:|
| `standard_user` | `secret_sauce` | ✅ 登录成功 |
| `locked_out_user` | `secret_sauce` | ❌ 账号锁定 |
| `standard_user` | `wrong_password` | ❌ 密码错误 |
| （空） | `secret_sauce` | ❌ 用户名为空 |
| `standard_user` | （空） | ❌ 密码为空 |

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| pytest 用例结构 | 函数名 `test_` 开头，一个用例测一个场景 |
| Page Object 调用 | 测试用例只调 LoginPage 方法，不直接操作 driver |
| 断言设计 | 成功：验证跳转到 `inventory.html`；失败：验证错误文案 |

**用例示例**：

```python
# tests/test_login.py
from pages.login_page import LoginPage

class TestLogin(MyTestBase):

    def test_login_success(self):
        """正例：正确的用户名密码应成功登录"""
        login_page = LoginPage(self)
        login_page.login("standard_user", "secret_sauce")
        # 断言：页面跳转到商品列表
        self.assert_url_contains("/inventory.html")

    def test_login_locked_out_user(self):
        """反例：锁定用户应显示错误提示"""
        login_page = LoginPage(self)
        login_page.login("locked_out_user", "secret_sauce")
        # 断言：出现锁定错误信息
        error = login_page.get_error_text()
        self.assert_true("locked out" in error.lower())
```

---

### 第五步：商品列表页 —— 排序与筛选（1 天）

**要做什么**：
创建 `pages/inventory_page.py` 和 `tests/test_inventory.py`。

**覆盖场景**：

| 场景 | 验证点 |
|------|--------|
| 商品列表加载 | 6 个商品卡片都可见 |
| 价格排序（低→高） | 排序后价格升序排列 |
| 名称排序（A→Z） | 排序后名称字母升序 |
| 添加单个商品到购物车 | 购物车徽标数字更新 |
| 添加多个商品 | 购物车徽标 = 添加数量 |
| 移除商品 | 购物车徽标 -1，按钮变回 Add to cart |

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| 数组收集与排序验证 | 提取列表数据 → 排序 → 断言顺序正确 |
| 动态元素交互 | `self.sb.select_option_by_value()` 下拉框操作 |
| 数据状态追踪 | 购物车数字从 0→1→2→1 的状态变化 |

---

### 第六步：购物车 + 结算全流程（1.5 天）

**要做什么**：
创建 `pages/cart_page.py`、`pages/checkout_page.py`、`tests/test_cart.py`、`tests/test_checkout.py`。

**覆盖场景**：

| 场景 | 验证点 |
|------|--------|
| 购物车为空 | 进入购物车页面显示空状态 |
| 从商品页添加后进购物车 | 商品名称/价格一致 |
| 从购物车移除商品 | 商品消失，剩余数量正确 |
| Continue Shopping 按钮 | 返回商品列表页 |
| 结算信息填写 | 必填项（名/姓/邮编）校验 |
| 缺信息结算 | 应显示错误提示 |
| 完整结算流程 | 显示总价、税额、确认页 |
| 结算完成 | 跳转成功页，购物车清空 |

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| 跨页面数据校验 | 商品页上的价格 = 购物车里的价格 = 结算确认页的价格 |
| 多页面协作 | LoginPage → InventoryPage → CartPage → CheckoutPage → OverviewPage |
| 复杂业务流程 | 8 步完整电商交易路径 |

---

### 第七步：数据驱动 + 参数化（1 天）

**要做什么**：
把登录测试改成数据驱动，用 JSON/CSV 管理多用户数据。

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| `@pytest.mark.parametrize` | pytest 原生参数化装饰器 |
| JSON 数据文件管理 | 用例脚本与测试数据分离 |
| 一条用例覆盖多组数据 | 和项目一的 Postman 数据驱动原理一样，换 Python 实现 |

**示例**：

```python
import json

# 从 JSON 文件加载测试数据
def load_test_data():
    with open("config/test_data.json") as f:
        return json.load(f)["login_users"]

@pytest.mark.parametrize("user", load_test_data())
def test_login_data_driven(self, user):
    login_page = LoginPage(self)
    login_page.login(user["username"], user["password"])
    if user["expected_success"]:
        self.assert_url_contains("/inventory.html")
    else:
        error = login_page.get_error_text()
        self.assert_true(user["expected_error"] in error)
```

---

### 第八步：Allure 报告 + 失败截图（0.5 天）

**要做什么**：
集成 Allure 生成可视化测试报告，失败自动截图。

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| Allure 安装与集成 | `pip install allure-pytest` |
| 报告内容 | 通过率 / 失败截图 / 步骤追踪 / 执行耗时 |
| 失败定位 | 从 Allure 报告直接跳转到失败步骤 + 截图 |

**运行命令**：

```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

### 第九步：GitHub + CI/CD（0.5 天）

**要做什么**：
创建 `.github/workflows/run_tests.yml`，代码 push 自动跑回归。

**要掌握的知识点**：

| 技能点 | 具体内容 |
|--------|----------|
| GitHub Actions 配置 | YAML 流水线语法 |
| 无头浏览器执行 | `--headless` 参数 |
| CI 产物 | Allure 报告上传为流水线产物 |

**流程**：`git push` → GitHub Actions 自动拉代码 → 装依赖 → 跑全量测试 → 生成 Allure 报告 → 产物可下载。

---

## ⏱️ 总时间估算

| 步骤 | 内容 | 时间 |
|------|------|:---:|
| 1 | BasePage 基类设计 | 0.5 天 |
| 2 | LoginPage + InventoryPage | 0.5 天 |
| 3 | conftest.py + pytest.ini | 0.5 天 |
| 4 | 登录用例（5 条） | 1 天 |
| 5 | 商品列表用例（排序/筛选/添加） | 1 天 |
| 6 | 购物车 + 结算全流程 | 1.5 天 |
| 7 | 数据驱动参数化 | 1 天 |
| 8 | Allure 报告 + 失败截图 | 0.5 天 |
| 9 | GitHub Actions CI/CD | 0.5 天 |
| **合计** | | **约 1 周** |

---

## 🎯 检验标准

完成本项目后，你应该能直接回答：

1. "Page Object Model 是什么？为什么要用？每个 Page 怎么划分粒度？"
2. "你写的 UI 自动化用例有哪些？覆盖了哪些业务场景？正反例都有吗？"
3. "SeleniumBase 和原生 Selenium 有什么区别？你为什么选它？"
4. "UI 自动化里怎么处理等待？什么是显式等待/隐式等待/强制等待？"
5. "失败截图是怎么触发的？怎么从 Allure 报告定位失败原因？"
6. "怎么把 UI 自动化放进 CI 流水线？跑一次回归要多久？"

---

## 📝 和项目一的关系

| 项目一（Postman + Reqres.in） | 项目二（SeleniumBase + SauceDemo） |
|---------------------------|----------------------------------|
| API 层测试 | **UI 层测试** |
| 测接口行为 | 测**用户可见行为** |
| 数据驱动用 Postman Runner | 数据驱动用 **pytest parametrize** |
| 报告是 Newman HTML | 报告是 **Allure**（更专业） |
| CI 是手动跑 Newman | CI 是 **GitHub Actions 自动触发** |

两个项目加起来 = **API + UI 双层自动化测试能力**，这就是测试开发工程师的核心技能。

---

开始第一步——创建项目文件夹，写 `base_page.py`。准备好了告诉我。
