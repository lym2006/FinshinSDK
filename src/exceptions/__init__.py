"""接口包异常出口

- 代发本体会认的异常类，文案表留本体侧
"""

from ._contracts import (
    BotError,
    ConnectivityError,
    DirectTimeoutError,
    DomainError,
    MessageVanishedError,
    ProbeCrashedError,
    ProbeTimeoutError,
    ProxyAddressError,
    ProxyConnectionRefusedError,
    ProxyError,
    ProxySchemeError,
    ProxySchemeMissingError,
    ProxyTimeoutError,
    TelegramServerError,
    TokenError,
    TokenFormatError,
)

__all__ = [
    # 基类
    "BotError",
    # 领域
    "DomainError",
    "MessageVanishedError",
    # 连接性
    "ConnectivityError",
    "DirectTimeoutError",
    "TokenError",
    "TelegramServerError",
    "ProxyError",
    "ProxyAddressError",
    "ProxySchemeError",
    "ProxySchemeMissingError",
    "ProxyTimeoutError",
    "ProxyConnectionRefusedError",
    "TokenFormatError",
    "ProbeTimeoutError",
    "ProbeCrashedError",
]
