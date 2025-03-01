from datetime import datetime

def pytest_configure():
    # 配置加载完毕，测试用例之前

    print(f"{datetime.now()}: 开始执行测试用例")

def pytest_unconfigure():
    # 结束测试

    print(f"{datetime.now()}: 测试用例执行完毕")
