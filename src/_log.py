"""日志公开件

- 实现由宿主绑定，没绑上就调用当场抛错
"""

from collections.abc import Callable
from enum import StrEnum
from typing import TypeAlias


class LogLevel(StrEnum):
    """日志档位"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


# 宿主交来的实现，异常位可空
_LogSink: TypeAlias = Callable[[str, LogLevel, str, BaseException | None], None]

_sink: _LogSink | None = None


def bind_logger(sink: _LogSink) -> None:
    """把宿主实现绑到调用面上，只由本体在启动期做一次"""
    global _sink
    _sink = sink


def log(
    source: str, level: LogLevel, msg: str, exc: BaseException | None = None
) -> None:
    """写一行日志

    - 来源名决定落进哪一只日志器
    - 带异常即由实现补一行调试档
    """
    if _sink is None:
        raise RuntimeError("日志件还没绑上实现")
    _sink(source, level, msg, exc)
