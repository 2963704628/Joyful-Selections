# pytest 快速入门指南
## 一、简介
- pytest 是一个成熟且功能全面的Python测试框架，其核心优势包括：

    - 简洁性与灵活性：易于上手，快速搭建测试环境。
    - 参数化支持：简化数据驱动测试。
    - 广泛适用性：覆盖单元至功能测试，兼容UI自动化（如selenium）、API测试。
    - 强大生态：丰富的第三方插件，如pytest-selenium、pytest-html、pytest-rerunfailures等。
    - 高级特性：测试跳过与预期失败处理，Jenkins集成，Allure报告支持。
    - 官方文档 https://docs.pytest.org/en/latest/contents.html

## 二、文件与命名规范
- 测试文件命名应遵循 test_*.py 或 *_test.py。
- 测试类以 Test 开头，无需 __init__ 方法。
## 三、安装
```shell
pip install pytest
```

## 四、编写测试用例
- 函数式：直接定义以 test_ 开头的函数。
- 类式：推荐使用，便于管理 fixtures，类名以 Test 开头，方法以 test_ 开头。
## 五、核心功能
- 测试生命周期管理：通过 setup_* 和 teardown_* 方法控制测试前后的操作。
- 参数化测试：利用 @pytest.mark.parametrize 实现数据驱动。
- 跳过与预期失败：@pytest.mark.skip 和 @pytest.mark.xfail 控制测试执行逻辑。
- Mark标记：多功能标记，如条件跳过、执行顺序控制、超时设置等。
- 自定义标签：通过 @pytest.mark.tag_name 定义，执行时筛选特定标签用例。
## 六、命令行操作
- 精准控制测试执行，包括指定用例、参数调整、输出定制等。
- 支持并行执行、超时设置、失败重试等功能，需相应插件。
## 七、高级特性
- conftest.py：项目级配置与fixture共享。
- Fixture夹具：灵活的测试环境准备与清理工具，支持多种作用域和自动应用。
- 内置函数与hook机制：如 tmpdir 临时文件管理，pytestconfig 访问配置，以及详尽的hook点以自定义测试流程。