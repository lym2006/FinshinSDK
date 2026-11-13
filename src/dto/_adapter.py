"""适配器数据传输对象

- 定义外部适配器自描述清单
- 字段与声明文件的段键对应
"""

from dataclasses import dataclass

from ..domain import Platform


@dataclass(frozen=True, slots=True)
class AdapterManifestDTO:
    """外部适配器自描述清单

    - 入口模块名取自声明里的入口点
    - 接口包版本下限取自声明，没写即不设限
    - 装进环境的适配器带不出这一项，那一路读到的是不设限
    """

    platform: Platform
    deps: tuple[str, ...]
    requires_sdk: str
    entry: str
