"""异常契约

- 定义所有自定义异常的基类与致命等级
- 定义代理与 Token 探测的细分异常
- 定义领域异常基类与消息消失错
"""

from typing import Any, ClassVar

from ..dto import MsgReferenceDTO


class BotError(Exception):
    """自定义异常基类

    - 关键字参数存为属性供文案模板渲染
    - fatal 定致命等级，兜底那侧按它决定弹窗还是回落向导
    """

    fatal: ClassVar[bool] = False

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()


class ConnectivityError(BotError):
    """连接性异常基类"""


class TelegramServerError(ConnectivityError):
    """Telegram 服务器异常"""


class DirectTimeoutError(ConnectivityError):
    """无代理直连超时"""


class TokenError(ConnectivityError):
    """Token 异常"""


class TokenFormatError(TokenError):
    """Token 形状不对

    - 平台各自的形状判定留在适配器，句子归本体
    """


class ProbeTimeoutError(ConnectivityError):
    """这一轮探测没在预算内回来"""


class ProbeCrashedError(ConnectivityError):
    """探测自己抛了表外的错"""


class ProxyError(ConnectivityError):
    """代理异常基类"""

    def __init__(self, proxy: str) -> None:
        self.proxy = proxy
        super().__init__()


class ProxySchemeError(ProxyError):
    """代理协议头错误"""

    def __init__(self, scheme: str = "未知协议", proxy: str = "") -> None:
        self.scheme = scheme
        super().__init__(proxy)


class ProxySchemeMissingError(ProxySchemeError):
    """代理地址没写协议头

    - 协议位为空时抛这一只，不用占位文案填协议位
    """

    def __init__(self, proxy: str) -> None:
        super().__init__(scheme="", proxy=proxy)


class ProxyAddressError(ProxyError):
    """代理地址解析错误"""


class ProxyConnectionRefusedError(ProxyError):
    """代理连接被拒绝"""


class ProxyTimeoutError(ProxyError):
    """代理连接超时"""


class DomainError(BotError):
    """领域异常基类"""


class MessageVanishedError(DomainError):
    """消息不存在

    - 被撤回或删除
    """

    def __init__(self, ref: MsgReferenceDTO) -> None:
        self.platform = ref.platform
        self.message_id = ref.message_id
        super().__init__()
