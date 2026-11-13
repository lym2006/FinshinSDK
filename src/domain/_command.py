"""命令值对象

- 跨平台归一的命令 flag 词表
- 分步输入的保留串词表
- 按清单声明把命令片段绑成开关与参数
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

# 开关名形状：短横起头、紧跟字母，其后可带字母数字与下划线短横
_FLAG_NAME_RE = re.compile(r"-[A-Za-z][A-Za-z0-9_-]*")

# 开关值的三种类型，清单写的默认值只能落在这三种上
ArgsValue = int | float | str


class CommandFlag(StrEnum):
    """命令 flag

    - -h 全命令默认支持，不登记进清单
    - 命令自有 flag 写在 plugin.toml 的 help.commands.flags，带短横
    """

    HELP = "-h"


class StepInput(StrEnum):
    """分步输入的保留串

    - 挂在待输入流程上时先于业务取值判定
    """

    STOP = "-1"  # 中止当前流程


@dataclass(frozen=True, slots=True)
class BoundCommand:
    """绑定后的命令输入

    - 开关项按清单顺序交出，每项是「开关 值」
    - 值按清单第三段的类型收，命令没写这只开关即落默认值
    - 纯开关的值是真假，没出现即假
    - 参数项是第一只开关之前的片段，顺序原样保留
    """

    flags: tuple[tuple[str, ArgsValue | bool], ...] = ()
    args: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BindFailure:
    """命令片段绑不进的现场

    - flag 是出事的那只开关，裸段出事时为空串
    - got 是当时收到的原文，缺值时空串
    """

    flag: str = ""
    got: str = ""


def is_flag_name(token: str) -> bool:
    """判定这段文本是开关名

    - 清单里的开关名与命令里带的片段共用这一个形状
    """
    return _FLAG_NAME_RE.fullmatch(token) is not None


def _cast(text: str, default: ArgsValue) -> ArgsValue | None:
    """按默认值的类型收开关值

    - 整数档拒收小数写法，小数档把整数写法转成小数，文本档原样交出
    - 收不进返回 None，交给绑不进的现场
    """
    if isinstance(default, str):
        return text
    try:
        return int(text) if isinstance(default, int) else float(text)
    except ValueError:
        return None


def bind_command(
    pieces: tuple[str, ...],
    flags: Sequence[tuple[str, ArgsValue | None]],
    takes_args: bool,
) -> BoundCommand | BindFailure:
    """按清单声明绑定命令片段

    - 声明项每项是清单里的「开关名 默认值」两栏，没默认值即纯开关
    - 位置参数只收第一只开关之前的片段，命令没登记参数即一段都不收
    - 带默认值的开关吃掉紧跟其后的一段，按默认值的类型转
    - -h 恒按纯开关收，不登记进清单
    - 开关没登记、同一开关重复、带值开关没吃到值一律绑不进
    """
    defaults = dict(flags)
    seen: dict[str, ArgsValue | bool] = {}
    args: list[str] = []
    index = 0

    while index < len(pieces):
        piece = pieces[index]
        if not is_flag_name(piece):
            if seen or not takes_args:
                return BindFailure(got=piece)
            args.append(piece)
            index += 1
            continue
        if piece != CommandFlag.HELP and piece not in defaults:
            return BindFailure(flag=piece)
        if piece in seen:
            return BindFailure(flag=piece)
        default = defaults.get(piece)
        if default is None:
            seen[piece] = True
            index += 1
            continue
        if index + 1 >= len(pieces) or is_flag_name(pieces[index + 1]):
            return BindFailure(flag=piece)
        value = _cast(pieces[index + 1], default)
        if value is None:
            return BindFailure(flag=piece, got=pieces[index + 1])
        seen[piece] = value
        index += 2

    settled: dict[str, ArgsValue | bool] = {
        name: (False if default is None else default)
        for name, default in defaults.items()
    }
    settled.update(seen)
    return BoundCommand(flags=tuple(settled.items()), args=tuple(args))
