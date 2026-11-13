"""断链上报公开件

- 断连周期的账由宿主自持，没绑上就调用当场抛错
"""

from collections.abc import Callable
from typing import TypeAlias

# 宿主交来的两只实现
_FailureSink: TypeAlias = Callable[[str, BaseException, str | None], None]
_RecoverySink: TypeAlias = Callable[[], None]

_on_failure: _FailureSink | None = None
_on_recovery: _RecoverySink | None = None


def bind_link_report(on_failure: _FailureSink, on_recovery: _RecoverySink) -> None:
    """把宿主的断连状态机绑到调用面上，只由本体在启动期做一次"""
    global _on_failure, _on_recovery
    _on_failure = on_failure
    _on_recovery = on_recovery


def link_down(api: str, error: BaseException, proxy: str | None) -> None:
    """报一次网络层失败"""
    if _on_failure is None:
        raise RuntimeError("断链上报件还没绑上实现")
    _on_failure(api, error, proxy)


def link_up() -> None:
    """报一次成功"""
    if _on_recovery is None:
        raise RuntimeError("断链上报件还没绑上实现")
    _on_recovery()
