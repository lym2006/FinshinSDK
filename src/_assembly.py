"""平台装配契约

- 定义适配器入口模块交出的三件与装配结果的数据形状
"""

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from ._adapter import BaseAdapter
from .domain import (
    BackgroundLoop,
    MomentRun,
    PlatformMoment,
    QueuedAction,
)
from .dto import PluginManifestDTO

# 单通道探测：收 token 与代理，回生效代理与每个坏掉字段的异常
ChannelProbe = Callable[[str, str], Awaitable[tuple[str | None, dict[str, Exception]]]]


@dataclass(frozen=True, slots=True)
class PlatformAssembly:
    """一个平台装配出来的件

    - 适配器交运行时托管，其余四件交装配层登记
    - 报告行每项是 (插件清单, 失败异常)，成功那项异常记 None
    """

    adapter: BaseAdapter
    report: Sequence[tuple[PluginManifestDTO, Exception | None]]
    background_loops: tuple[BackgroundLoop, ...]
    queued_actions: tuple[QueuedAction, ...]
    platform_moments: dict[PlatformMoment, tuple[MomentRun, ...]]


@dataclass(frozen=True, slots=True)
class AdapterParts:
    """适配器入口模块交出的三件

    - 收 token 与代理，回这个平台的运行时
    - 引擎预热只付导入费
    """

    assemble: Callable[[str, str | None], BaseAdapter]
    channel_probe: ChannelProbe
    engine_preload: Callable[[], None]
