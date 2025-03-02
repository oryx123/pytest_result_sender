from datetime import datetime

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_addoption(parser):
    parser.addini("send_when", help="send result when")
    parser.addini("send_api", help="send where")


def pytest_runtest_logreport(report):
    # print(report)
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成后执行，包含了所有用例
    data["total"] = len(session.items)
    # print(data["total"])


def pytest_configure(config: pytest.Config):
    # 配置加载完毕，测试用例之前
    data["start_time"] = datetime.now()
    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")
    # print(config.getini('send_when'))
    # print(config.getini('send_api'))


def pytest_unconfigure():
    # 结束测试
    data["end_time"] = datetime.now()

    data["duration"] = data["end_time"] - data["start_time"]
    data["pass_ratio"] = data["passed"] / data["total"] * 100
    data["pass_ratio"] = f"{data['pass_ratio']:.2f}%"
    # assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
    send_result()


def send_result():
    print(data["send_when"])
    print(data["send_api"])

    if data["send_when"] == "on_fail" and data["failed"] == 0:
        return
    if data["send_api"] == "":
        return
    url = data["send_api"]

    content = f"""
    自动化测试报告
    用例总数：{data['total']}
    用例通过数：{data['passed']}
    用例失败数：{data['failed']}
    用例通过率：{data['pass_ratio']}
    用例执行时间：{data['duration']}
    """
    print("!!!!!!!!!!!!")
    print(content)
    print("!!!!!!!!!!!!")
    try:
        requests.post(
            url, json={"msgtype": "markdown", "markdown": {"content": content}}
        )
    except Exception as e:
        print(e)

    data["send_done"] = True
