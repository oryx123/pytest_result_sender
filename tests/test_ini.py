import pytest

from pytest_result_sender import plugin

pytest_plugins = "pytester"


@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = {
        "passed": 0,
        "failed": 0,
    }
    yield
    plugin.data = bak_data


@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path):
    config_path = tmp_path / "pytest.ini"
    config_path.write_text(
        f"""
[pytest]
send_when = {send_when}
send_api = www.baidu.com
"""
    )

    config = pytester.parseconfig(config_path)
    assert config.getini("send_when") == send_when

    pytester.makepyfile(  # 构造一个场景，全部用例都成功
        """
        def test_pass():
            pass
        """
    )

    pytester.runpytest("-c", str(config_path))

    # 检查是否发送了请求
    print(plugin.data)

    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize("send_api", ["www.baidu.com", ""])
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path):
    config_path = pytester.path / "pytest.ini"
    config_path.write_text(
        f"""
[pytest]
send_when = every
send_api = {send_api}
"""
    )

    config = pytester.parseconfig(config_path)
    assert config.getini("send_api") == send_api

    pytester.makepyfile(  # 构造一个场景，全部用例都成功
        """
        def test_pass():
            pass
        """
    )

    pytester.runpytest("-c", str(config_path))

    # 检查是否发送了请求
    print(plugin.data)

    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
