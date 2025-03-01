from datetime import datetime, timedelta

import pytest

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_runtest_logreport(report):
    print(report)
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成后执行，包含了所有用例
    data["total"] = len(session.items)
    print(session.items)


def pytest_configure():
    # 配置加载完毕，测试用例之前
    data["start_time"] = datetime.now()


def pytest_unconfigure():
    # 结束测试
    data["end_time"] = datetime.now()

    data["duration"] = data["end_time"] - data["start_time"]
    data["pass_ratio"] = data["passed"] / data["total"] * 100
    data["pass_ratio"] = f"{data['pass_ratio']:.2f}%"
    assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
    assert data["total"] == 3
    assert data["passed"] == 2
    assert data["failed"] == 1
    print(data["pass_ratio"])
    assert data["pass_ratio"] == "66.67%"
