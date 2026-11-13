"""外部适配器词表

- 定义适配器装载根、声明文件名、入口点组名与声明键位
"""

from dataclasses import dataclass
from enum import StrEnum

# 适配器装载根，安装目录下的适配器目录，每个平台各占一层子目录
ADAPTERS_PKG = "finshin/adapter"

# 声明文件名，位于各适配器目录根
ADAPTER_MANIFEST_FILE = "pyproject.toml"

# 入口点组名，已装包靠它自报平台，键即平台标识
ADAPTER_ENTRY_GROUP = "finshin.adapters"

# 入口点值里冒号后必须指的属性名，由本体规定
ADAPTER_ENTRY_ATTR = "parts"


class AdapterManifestKey(StrEnum):
    """适配器声明键位，值即声明文件里的段名与键名"""

    PLATFORM = "tool.finshin-adapter.platform"
    DEPS = "project.dependencies"


@dataclass(frozen=True, slots=True)
class AdapterFieldSpec:
    """适配器声明字段规格"""

    key: AdapterManifestKey
    value_type: type
    required: bool = False


ADAPTER_MANIFEST_FIELDS: tuple[AdapterFieldSpec, ...] = (
    AdapterFieldSpec(AdapterManifestKey.PLATFORM, str, required=True),
    AdapterFieldSpec(AdapterManifestKey.DEPS, list),
)
