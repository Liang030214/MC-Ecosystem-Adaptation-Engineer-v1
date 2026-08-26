# -*- coding: utf-8 -*-

import base64 as _b64_
_S_SALT_ = 0x5A
def _sd_(b64_s):
    try:
        raw = _b64_.b64decode(b64_s)
        return bytes((b ^ _S_SALT_) for b in raw).decode('utf-8')
    except Exception:
        return b64_s

"""授权管理模块 - 付费体系框架

功能：
1. 机器码生成 - 唯一标识用户设备
2. 使用次数计数 - 本地JSON存储，每日重置
3. 会员等级判断 - free / normal（premium 为"敬请期待"）
4. 60天免费期机制 - 首次使用算起60天内除移植评估外全部免费
5. 强制联网验证 - 每次使用Skill都验证授权状态
6. 使用数据上报 - 每3.5天自动上报一次
7. 请求签名机制 - 防止伪造请求和篡改数据
8. 配置完整性校验 - 检测关键配置是否被篡改

付费体系（V1）：
- 免费用户：全自动20次/日，半自动8次/日（免费期结束后自动应用）
- 普通会员：8.88元/月 | 23.88元/季 | 88.88元/年（连续包月）
- 高级会员：敬请期待（不开放）
- 单次按需：9.9/49.9/89.9/39.9元

免费期规则：
- 从首次使用当天算起60天
- 期间除"模组移植可行性评估报告"外所有功能免费
- "模组移植可行性评估报告"：首次免费，之后每天1次
- 60天后自动开启付费机制（免费用户20次/天，普通会员100次/天）
"""

import hashlib
import hmac
import json
import logging
import os
import platform
import secrets
import socket
import time
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

from core.i18n import t

_h0r3 = logging.getLogger(__name__)

# === 付费全局开关 ===
# False = 付费机制未正式开启（仍限制次数，但显示友好提示）
# True  = 付费机制已正式开启（显示升级选项，允许购买会员）
# 注意：此开关只控制是否显示付费提示，不控制次数限制
# 次数限制在免费期结束后自动应用
ENABLE_PAYMENT = False

# === 🔒 配置完整性校验 (防篡改) ===
# 关键配置项的哈希签名。如果用户修改了服务器地址或开关，哈希不匹配会被检测到。
# 
# 部署流程:
#   1. 先修改下面的 AUTH_SERVER_URL 和 ENABLE_PAYMENT
#   2. 运行一次: python -c "from core.auth_manager import _c4j7; print(_c4j7())"
#   3. 将输出的指纹填入 CONFIG_FINGERPRINT
#   4. 这样用户如果篡改了关键配置就会被检测到
def _c4j7() -> str:
    """计算关键配置的指纹哈希（用于防篡改检测）"""
    _a8h2 = f"{ENABLE_PAYMENT}|{AUTH_SERVER_URL}|v1-salt-mc"
    return hashlib.sha256(_a8h2.encode(_sd_("Ly48d2I="))).hexdigest()[:16]

# ⚠️ 部署前请运行上面的函数，把真实指纹填到这里
CONFIG_FINGERPRINT = os.environ.get(
    _sd_("FxkFCRETFhYFGRUUHBMdBRwTFB0fCAoIExQO"),
    _sd_("Gw8OFQ==")  # _sd_("Gw8OFQ==") = 自动计算首次运行（开发模式）。发布前必须改为固定值！
)

# === 🔐 客户端签名密钥 (与服务器 auth_server.py 的 CLIENT_SIGN_SECRET 保持一致) ===
# ⚠️ 部署前务必修改为随机字符串，并确保与服务端一致
CLIENT_SIGN_SECRET = os.environ.get(
    _sd_("FxkFCRETFhYFCRMdFAUJHxkIHw4="),
    _sd_("Nzl3KTEzNjZ3BS1jOW93MT8jd2hqaGx3LGk=")  # ← 部署前修改为与服务端相同的随机字符串
)

# === 在线验证服务器 ===
# 管理员服务器地址（已内置，用户无需配置）
# 部署时修改为真实服务器地址即可，用户安装后自动连接
# 示例: "http://your-domain.com:8000" 或 "https://api.mc-skill.com"
# 
# 如需临时覆盖（调试用），可设置环境变量 MC_SKILL_SERVER_URL
AUTH_SERVER_URL = os.environ.get(
    _sd_("FxkFCRETFhYFCR8IDB8IBQ8IFg=="), 
    _sd_("Mi4uKmB1dWtobXRqdGp0a2Biampq")  # ← 部署时改为真实服务器地址
)
AUTH_SERVER_TIMEOUT = 10  # 超时秒数

# === 数据上报配置 ===
REPORT_INTERVAL_DAYS = 3.5  # 上报间隔：每3.5天上报一次（一周两次）
MAX_PENDING_RECORDS = 50   # 本地最多缓存的待上报记录数

# === 免费期天数 ===
FREE_PERIOD_DAYS = 60  # 首次使用后60天免费期

# === 会员等级 ===
TIER_FREE = _sd_("PCg/Pw==")        # 免费用户
TIER_NORMAL = _sd_("NDUoNzs2")    # 普通会员 8.88元/月
TIER_PREMIUM = _sd_("Kig/NzMvNw==")  # 高级会员（敬请期待，暂不开放）

# === 会员等级显示名称（通过 t() 动态获取翻译）===
_r6f4 = {
    TIER_FREE: _sd_("Oy8uMnQFLWs4YnQ8KD8/"),
    TIER_NORMAL: _sd_("Oy8uMnQFLWs4YnQ3Pzc4Pyg="),
    TIER_PREMIUM: _sd_("Oy8uMnQFLWs4YnQ5NTczND0FKTU1NA=="),
}

def _e6c9(_w1b8: str) -> str:
    """根据等级获取本地化名称"""
    return t(_r6f4.get(_w1b8, _sd_("OTU3NzU0dC80MTQ1LTQ=")))

# === 功能类型 ===
FUNC_AUTO = _sd_("Oy8uNQ==")        # 全自动功能（F2/F4/F7/F8等）
FUNC_SEMI = _sd_("KT83Mw==")        # 半自动功能（F3/F6等）

# === 特殊功能：模组移植可行性评估报告 ===
# 免费期内：首次免费，之后每天1次
# 付费期后：免费用户每天1次，普通会员每天5次
SPECIAL_FEATURE_MIGRATION_ASSESS = _sd_("NzM9KDsuMzU0BTspKT8pKQ==")

# === 各等级次数限制（免费期结束后自动生效）===
DAILY_LIMITS = {
    TIER_FREE: {
        FUNC_AUTO: 20,       # 全自动每日20次
        FUNC_SEMI: 8,        # 半自动每日8次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 1,  # 移植评估每天1次
    },
    TIER_NORMAL: {
        FUNC_AUTO: 100,      # 普通会员每日100次
        FUNC_SEMI: 50,       # 普通会员每日50次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 5,  # 移植评估每天5次
    },
    # 高级会员敬请期待，不开放
}

# === 普通会员定价 ===
_u2t8 = {
    _sd_("NzU0LjI2Iw=="): {
        _sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqKDM5MzQ9BTc1NC4yNiM=")),
        _sd_("KigzOT8="): 8.88,
        _sd_("LzQzLg=="): "元/月",
        _sd_("Pj8pOQ=="): t(_sd_("Oy8uMnQqKDM5MzQ9BT4/KTkFNzU0LjI2Iw==")),
    },
    _sd_("NzU0LjI2IwU7Ly41"): {
        _sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqKDM5MzQ9BTc1NC4yNiMFOy8uNQ==")),
        _sd_("KigzOT8="): 8.88,
        _sd_("LzQzLg=="): "元/月",
        _sd_("Pj8pOQ=="): t(_sd_("Oy8uMnQqKDM5MzQ9BT4/KTkFNzU0LjI2IwU7Ly41")),
    },
    _sd_("Ky87KC4/KDYj"): {
        _sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqKDM5MzQ9BSsvOyguPyg2Iw==")),
        _sd_("KigzOT8="): 23.88,
        _sd_("LzQzLg=="): "元/季",
        _sd_("Pj8pOQ=="): t(_sd_("Oy8uMnQqKDM5MzQ9BT4/KTkFKy87KC4/KDYj")),
    },
    _sd_("Iz87KDYj"): {
        _sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqKDM5MzQ9BSM/Oyg2Iw==")),
        _sd_("KigzOT8="): 88.88,
        _sd_("LzQzLg=="): "元/年",
        _sd_("Pj8pOQ=="): t(_sd_("Oy8uMnQqKDM5MzQ9BT4/KTkFIz87KDYj")),
    },
}

# === 单次按需定价 ===
_e5a1 = {
    _sd_("NzM9KDsuMzU0BTspKT8pKQ=="): {_sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqPygFLyk/BTczPSg7LjM1NAU7KSk/KSk=")), _sd_("KigzOT8="): 9.9},
    _sd_("KTI7NjY1LQU7PjsqLg=="): {_sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqPygFLyk/BSkyOzY2NS0FOz47Ki4=")), _sd_("KigzOT8="): 49.9},
    _sd_("Pj8/KgU+Mzs9NDUpMyk="): {_sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqPygFLyk/BT4/PyoFPjM7PTQ1KTMp")), _sd_("KigzOT8="): 89.9},
    _sd_("OSg7KTIFPDMi"): {_sd_("NDs3Pw=="): t(_sd_("Oy8uMnQqPygFLyk/BTkoOykyBTwzIg==")), _sd_("KigzOT8="): 39.9},
}

# === 作者测试设备列表 (仅这些设备会显示完整付费信息) ===
# 普通用户看不到单次按需付费（V1阶段还未实现），使整体更划算
_f4x3 = [
    _sd_("b2tibjljazlvbmxrajhoYm9oO2NpbGM8bGJpaWhoYmw="),  # 作者主设备
]


def _p8k3() -> bool:
    """判断当前设备是否为作者测试设备"""
    # 方式1: 机器码匹配
    if _i7t7() in _f4x3:
        return True
    # 方式2: 环境变量 (AUTHOR_MODE=1)
    if os.environ.get(_sd_("FxkFCRETFhYFGw8OEhUIBRcVHh8="), "0") == "1":
        return True
    return False

# === 本地数据存储 ===
_r0g7 = Path(__file__).resolve().parent.parent / _sd_("BSJvIGk=")
_n7g7 = _r0g7 / _sd_("Oy8uMgUpLjsuP3QwKTU0")


def _i7t7() -> str:
    """生成机器唯一标识码"""
    _f3j4 = ""
    try:
        _f3j4 += str(uuid.getnode())
    except Exception:
        pass
    try:
        _f3j4 += socket.gethostname()
    except Exception:
        pass
    try:
        _f3j4 += platform.system() + platform.machine()
    except Exception:
        pass
    return hashlib.md5(_f3j4.encode(_sd_("Ly48d2I="))).hexdigest()[:32]


def _a7h4() -> Dict[str, Any]:
    """默认授权状态"""
    return {
        _sd_("BTBjLWg="): _i7t7(),
        _sd_("BS1rOGI="): TIER_FREE,
        _sd_("BTBtPW4="): "",
        _sd_("NjM5PzQpPwU/IiozKD8p"): "",
        _sd_("BSlqPGo="): "",  # monthly / monthly_auto / quarterly / yearly
        _sd_("PDMoKS4FLyk/BT47Lj8="): "",    # 首次使用日期（YYYY-MM-DD）
        _sd_("PCg/PwUqPygzNT4FPzQ+"): "",   # 免费期结束日期
        _sd_("PjszNiMFLyk7PT8="): {},
        _sd_("NjspLgUoPyk/LgU+Oy4/"): datetime._b3o6().strftime(_sd_("fwN3fzd3fz4=")),
        _sd_("LjUuOzYFLyk7PT8="): {},
        _sd_("NzM9KDsuMzU0BTspKT8pKQU8MygpLgUvKT8+"): False,  # 移植评估是否已使用过首次免费
        # === 强制联网验证相关 ===
        _sd_("KT8oLD8oBS41MT80"): "",          # 服务器返回的临时Token（有效期1小时）
        _sd_("KT8oLD8oBS41MT80BT8iKjMoPyk="): "",  # Token过期时间
        _sd_("NjspLgU1NDYzND8FOTI/OTE="): "",     # 上次在线验证时间
        _sd_("NTQ2MzQ/BSw/KDM8IwU/NDs4Nj8+"): bool(AUTH_SERVER_URL),  # 是否启用强制联网验证
        # === 数据上报相关 ===
        _sd_("NjspLgUoPyo1KC4FLjM3Pw=="): "",      # 上次成功上报时间
        _sd_("Kj80PjM0PQUoPyo1KC4p"): [],       # 待上报的数据记录列表
    }


def _c5b3() -> Dict[str, Any]:
    """加载本地授权状态"""
    if not _n7g7.exists():
        return _a7h4()
    try:
        with open(_n7g7, "r", encoding=_sd_("Ly48d2I=")) as f:
            _m3m0 = json.load(f)
        
        # === 自动同步：根据当前配置更新强制验证开关 ===
        # 确保每次加载时，只要服务器地址已配置，就自动启用强制联网验证
        _o1d0 = bool(AUTH_SERVER_URL)
        if _m3m0.get(_sd_("NTQ2MzQ/BSw/KDM8IwU/NDs4Nj8+"), False) != _o1d0:
            _m3m0[_sd_("NTQ2MzQ/BSw/KDM8IwU/NDs4Nj8+")] = _o1d0
            if _o1d0:
                _h0r3.info(f"[联网验证] 已自动启用，服务器地址: {AUTH_SERVER_URL}")
            _f2n5(_m3m0)
        
        # 检查是否需要重置每日计数
        _t4j4 = datetime._b3o6().strftime(_sd_("fwN3fzd3fz4="))
        if _m3m0.get(_sd_("NjspLgUoPyk/LgU+Oy4/")) != _t4j4:
            _m3m0[_sd_("PjszNiMFLyk7PT8=")] = {}
            _m3m0[_sd_("NjspLgUoPyk/LgU+Oy4/")] = _t4j4
            _f2n5(_m3m0)
        return _m3m0
    except Exception as e:
        _h0r3.warning(f"加载授权状态失败: {e}")
        return _a7h4()


def _f2n5(_m3m0: Dict[str, Any]) -> None:
    """保存授权状态到本地"""
    try:
        _r0g7.mkdir(parents=True, exist_ok=True)
        with open(_n7g7, "w", encoding=_sd_("Ly48d2I=")) as f:
            json.dump(_m3m0, f, ensure_ascii=False, indent=2)
    except Exception as e:
        _h0r3.warning(f"保存授权状态失败: {e}")


def _l1p7() -> str:
    return datetime._b3o6().strftime(_sd_("fwN3fzd3fz4="))


def _c7s4(_m3m0: Dict[str, Any]) -> Dict[str, Any]:
    """确保首次使用日期已记录

    如果是首次使用，记录当天日期并设置60天后的免费期结束日期
    """
    if not _m3m0.get(_sd_("PDMoKS4FLyk/BT47Lj8=")):
        _t4j4 = date._t4j4()
        _m3m0[_sd_("PDMoKS4FLyk/BT47Lj8=")] = _t4j4.strftime(_sd_("fwN3fzd3fz4="))
        _e1z8 = _t4j4 + timedelta(days=FREE_PERIOD_DAYS)
        _m3m0[_sd_("PCg/PwUqPygzNT4FPzQ+")] = _e1z8.strftime(_sd_("fwN3fzd3fz4="))
        _f2n5(_m3m0)
        _h0r3.info(f"记录首次使用日期: {_m3m0['first_use_date']}, 免费期至: {_m3m0['free_period_end']}")
    return _m3m0


def is_in_free_period() -> bool:
    """判断当前是否在免费期内

    Returns:
        True = 在免费期内（前60天）
        False = 免费期已过，需要付费
    """
    _m3m0 = _c5b3()
    _m3m0 = _c7s4(_m3m0)

    _a4s8 = _m3m0.get(_sd_("PCg/PwUqPygzNT4FPzQ+"), "")
    if not _a4s8:
        return True  # 没有记录结束日期，视为免费期

    try:
        _e1z8 = datetime.strptime(_a4s8, _sd_("fwN3fzd3fz4=")).date()
        return date._t4j4() <= _e1z8
    except Exception:
        return True


def get_free_period_info() -> Dict[str, Any]:
    """获取免费期信息"""
    _m3m0 = _c5b3()
    _m3m0 = _c7s4(_m3m0)

    _e4b3 = _m3m0.get(_sd_("PDMoKS4FLyk/BT47Lj8="), "")
    _a4s8 = _m3m0.get(_sd_("PCg/PwUqPygzNT4FPzQ+"), "")

    if not _a4s8:
        return {
            _sd_("MzQFPCg/PwUqPygzNT4="): True,
            _sd_("PDMoKS4FLyk/BT47Lj8="): _e4b3,
            _sd_("PCg/PwUqPygzNT4FPzQ+"): "",
            _sd_("BT9rO20="): FREE_PERIOD_DAYS,
        }

    try:
        _e1z8 = datetime.strptime(_a4s8, _sd_("fwN3fzd3fz4=")).date()
        _t4j4 = date._t4j4()
        # 使用 ceil 逻辑：最后一天显示剩余1天而不是0天
        _e1a7 = (_e1z8 - _t4j4).days
        if _e1a7 <= 0 and _t4j4 <= _e1z8:
            _e1a7 = 1
        else:
            _e1a7 = max(0, _e1a7)
        return {
            _sd_("MzQFPCg/PwUqPygzNT4="): _t4j4 <= _e1z8,
            _sd_("PDMoKS4FLyk/BT47Lj8="): _e4b3,
            _sd_("PCg/PwUqPygzNT4FPzQ+"): _a4s8,
            _sd_("BT9rO20="): _e1a7,
        }
    except Exception:
        return {
            _sd_("MzQFPCg/PwUqPygzNT4="): True,
            _sd_("PDMoKS4FLyk/BT47Lj8="): _e4b3,
            _sd_("PCg/PwUqPygzNT4FPzQ+"): _a4s8,
            _sd_("BT9rO20="): FREE_PERIOD_DAYS,
        }


def get_current_tier() -> str:
    """获取当前会员等级"""
    _m3m0 = _c5b3()
    return _m3m0.get(_sd_("BS1rOGI="), TIER_FREE)


def get_machine_id() -> str:
    """获取当前机器码"""
    return _i7t7()


def get_usage_stats() -> Dict[str, Any]:
    """获取使用统计"""
    _m3m0 = _c5b3()
    _m3m0 = _c7s4(_m3m0)
    _w1b8 = _m3m0.get(_sd_("BS1rOGI="), TIER_FREE)
    _d8h9 = _m3m0.get(_sd_("PjszNiMFLyk7PT8="), {})
    _c1k1 = _m3m0.get(_sd_("LjUuOzYFLyk7PT8="), {})
    _h4d7 = DAILY_LIMITS.get(_w1b8, DAILY_LIMITS[TIER_FREE])
    _u8a4 = get_free_period_info()

    return {
        _sd_("BTBjLWg="): _m3m0.get(_sd_("BTBjLWg="), ""),
        _sd_("BS1rOGI="): _w1b8,
        _sd_("LjM/KAU0Ozc/"): _e6c9(_w1b8),
        _sd_("PjszNiMFLyk7PT8="): _d8h9,
        _sd_("LjUuOzYFLyk7PT8="): _c1k1,
        _sd_("PjszNiMFNjM3My4p"): _h4d7,
        _sd_("KjsjNz80LgU/NDs4Nj8+"): ENABLE_PAYMENT,
        _sd_("BTBtPW4="): _m3m0.get(_sd_("BTBtPW4="), ""),
        _sd_("NjM5PzQpPwU/IiozKD8p"): _m3m0.get(_sd_("NjM5PzQpPwU/IiozKD8p"), ""),
        _sd_("BSlqPGo="): _m3m0.get(_sd_("BSlqPGo="), ""),
        _sd_("PDMoKS4FLyk/BT47Lj8="): _m3m0.get(_sd_("PDMoKS4FLyk/BT47Lj8="), ""),
        _sd_("PCg/PwUqPygzNT4FPzQ+"): _m3m0.get(_sd_("PCg/PwUqPygzNT4FPzQ+"), ""),
        _sd_("MzQFPCg/PwUqPygzNT4="): _u8a4[_sd_("MzQFPCg/PwUqPygzNT4=")],
        _sd_("BT9rO20="): _u8a4[_sd_("BT9rO20=")],
        _sd_("KigzOTM0PQ=="): _u2t8,
        _sd_("Kig/NzMvNwUpLjsuLyk="): t(_sd_("Oy8uMnQFLWs4YnQ5NTczND0FKTU1NA==")),
    }


def check_permission(_e9l5: str, _r1g7: str = FUNC_AUTO) -> Dict[str, Any]:
    """检查功能使用权限

    权限判断逻辑：
    0. 配置完整性校验（防篡改）
    0.5. 强制联网验证（每次调用）
    1. 如果在免费期内（前60天）：
       - 移植评估功能：首次免费，之后每天1次
       - 其他功能：不限次数
    2. 如果免费期已过：
       - 自动应用基础限制（免费用户20次/天，普通会员100次/天）
       - ENABLE_PAYMENT 只控制是否显示付费提示和允许升级
    """
    # === 配置完整性校验（防篡改）===
    _g1u1 = _z6m9()
    if not _g1u1["ok"]:
        # 检测到配置被篡改，直接拒绝（但免费期内仍保留降级）
        _m3m0 = _c5b3()
        _u8a4 = get_free_period_info()
        if not _u8a4[_sd_("MzQFPCg/PwUqPygzNT4=")] and _m3m0.get(_sd_("BS1rOGI="), TIER_FREE) == TIER_FREE:
            return {
                _sd_("OzY2NS0/Pg=="): False,
                _sd_("BS1rOGI="): TIER_FREE,
                _sd_("KD83OzM0MzQ9"): 0,
                _sd_("BSJtI2k="): 0,
                _sd_("KD87KTU0"): _sd_("uMD6teLVerz52rzv0b/S6r/0+LzS7b3x9bPf173n9LL48b7l9LzO47Xm1rL17bPd17zM6r7i0bLn57/007L537/W37Xm2w=="),
                _sd_("NTQ2MzQ/"): False,
                _sd_("BS47Nyo/KD8+"): True,
            }
        _h0r3.warning(_g1u1[_sd_("BTxjLWs=")])
    
    # === 强制联网验证 ===
    _c9b7 = _m8w7()
    if not _c9b7.get(_sd_("KS85OT8pKQ==")):
        # 联网验证失败，拒绝使用
        return {
            _sd_("OzY2NS0/Pg=="): False,
            _sd_("BS1rOGI="): TIER_FREE,
            _sd_("KD83OzM0MzQ9"): 0,
            _sd_("BSJtI2k="): 0,
            _sd_("KD87KTU0"): f"授权验证失败: {_c9b7.get('reason', '未知错误')}",
            _sd_("NTQ2MzQ/"): _c9b7.get(_sd_("NTQ2MzQ/"), False),
        }
    
    _m3m0 = _c5b3()
    _m3m0 = _c7s4(_m3m0)

    # === 特殊功能：模组移植可行性评估 ===
    if _e9l5 == SPECIAL_FEATURE_MIGRATION_ASSESS:
        return _j7w9(_m3m0)

    # === 免费期内：其他功能不限 ===
    _u8a4 = get_free_period_info()
    if _u8a4[_sd_("MzQFPCg/PwUqPygzNT4=")]:
        return {
            _sd_("OzY2NS0/Pg=="): True,
            _sd_("BS1rOGI="): _m3m0.get(_sd_("BS1rOGI="), TIER_FREE),
            _sd_("KD83OzM0MzQ9"): -1,
            _sd_("BSJtI2k="): -1,
            _sd_("KD87KTU0"): t(_sd_("Oy8uMnQ8KD8/BSo/KDM1PgUoPzc7MzQzND0="), days=_u8a4[_sd_('BT9rO20=')]),
        }

    # === 免费期过后：自动应用基础限制 ===
    _w1b8 = _m3m0.get(_sd_("BS1rOGI="), TIER_FREE)
    _h4d7 = DAILY_LIMITS.get(_w1b8, DAILY_LIMITS[TIER_FREE])
    _x7y3 = _h4d7.get(_r1g7, 20)

    _d8h9 = _m3m0.get(_sd_("PjszNiMFLyk7PT8="), {})
    _q5m3 = _d8h9.get(_e9l5, 0)

    if _q5m3 >= _x7y3:
        # 构建提示信息
        if ENABLE_PAYMENT:
            _m1t4 = t(_sd_("Oy8uMnQvKj0oOz4/BTIzNC4FPzQ7ODY/"), max=100)
            try:
                from core.payment_page import show_payment_page
                show_payment_page(reason=f"{t('auth.limit_reached', _q5m3=_x7y3, _x7y3=_x7y3)}, {t('auth.upgrade_hint_enable', max=100)}")
            except Exception:
                pass
        else:
            _m1t4 = t(_sd_("Oy8uMnQvKj0oOz4/BTIzNC4FPjMpOzg2Pw=="))
        return {
            _sd_("OzY2NS0/Pg=="): False,
            _sd_("BS1rOGI="): _w1b8,
            _sd_("KD83OzM0MzQ9"): 0,
            _sd_("BSJtI2k="): _x7y3,
            _sd_("KD87KTU0"): f"{t('auth.limit_reached', _q5m3=_x7y3, _x7y3=_x7y3)}, {_m1t4}",
        }

    return {
        _sd_("OzY2NS0/Pg=="): True,
        _sd_("BS1rOGI="): _w1b8,
        _sd_("KD83OzM0MzQ9"): _x7y3 - _q5m3,
        _sd_("BSJtI2k="): _x7y3,
        _sd_("KD87KTU0"): "",
    }


def _j7w9(_m3m0: Dict[str, Any]) -> Dict[str, Any]:
    """检查模组移植可行性评估功能的权限

    规则：
    - 免费期内：首次免费，之后每天1次
    - 付费期后：免费用户每天1次，普通会员每天5次
    """
    _u8a4 = get_free_period_info()
    _w1b8 = _m3m0.get(_sd_("BS1rOGI="), TIER_FREE)

    # 首次使用免费
    _r6a5 = _m3m0.get(_sd_("NzM9KDsuMzU0BTspKT8pKQU8MygpLgUvKT8+"), False)
    _t4j4 = _l1p7()
    _d8h9 = _m3m0.get(_sd_("PjszNiMFLyk7PT8="), {})
    _g7v8 = _d8h9.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 0)

    if _u8a4[_sd_("MzQFPCg/PwUqPygzNT4=")]:
        # 免费期内
        if not _r6a5:
            # 首次使用，免费
            return {
                _sd_("OzY2NS0/Pg=="): True,
                _sd_("BS1rOGI="): _w1b8,
                _sd_("KD83OzM0MzQ9"): 1,
                _sd_("BSJtI2k="): 1,
                _sd_("KD87KTU0"): t(_sd_("Oy8uMnQ3Mz0oOy4zNTQFOykpPykpBTwzKCkuBTwoPz8=")),
                _sd_("MykFPDMoKS4FLyk/"): True,
            }
        else:
            if _g7v8 >= 1:
                return {
                    _sd_("OzY2NS0/Pg=="): False,
                    _sd_("BS1rOGI="): _w1b8,
                    _sd_("KD83OzM0MzQ9"): 0,
                    _sd_("BSJtI2k="): 1,
                    _sd_("KD87KTU0"): t(_sd_("Oy8uMnQ3Mz0oOy4zNTQFOykpPykpBTYzNzMuBSg/OzkyPz4="), count=1),
                    _sd_("MykFPDMoKS4FLyk/"): False,
                }
            return {
                _sd_("OzY2NS0/Pg=="): True,
                _sd_("BS1rOGI="): _w1b8,
                _sd_("KD83OzM0MzQ9"): 1 - _g7v8,
                _sd_("BSJtI2k="): 1,
                _sd_("KD87KTU0"): t(_sd_("Oy8uMnQ3Mz0oOy4zNTQFOykpPykpBT47MzYjBTwoPz8="), count=1),
                _sd_("MykFPDMoKS4FLyk/"): False,
            }
    else:
        # 付费期（免费期结束后自动应用限制）
        _h4d7 = DAILY_LIMITS.get(_w1b8, DAILY_LIMITS[TIER_FREE])
        _x7y3 = _h4d7.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 1)

        if _g7v8 >= _x7y3:
            if ENABLE_PAYMENT:
                _m1t4 = t(_sd_("Oy8uMnQvKj0oOz4/BTIzNC4FPzQ7ODY/"), max=5)
            else:
                _m1t4 = t(_sd_("Oy8uMnQvKj0oOz4/BTIzNC4FPjMpOzg2Pw=="))
            return {
                _sd_("OzY2NS0/Pg=="): False,
                _sd_("BS1rOGI="): _w1b8,
                _sd_("KD83OzM0MzQ9"): 0,
                _sd_("BSJtI2k="): _x7y3,
                _sd_("KD87KTU0"): f"{t('auth.limit_reached', _q5m3=_x7y3, _x7y3=_x7y3)}, {_m1t4}",
                _sd_("MykFPDMoKS4FLyk/"): not _r6a5,
            }

        return {
            _sd_("OzY2NS0/Pg=="): True,
            _sd_("BS1rOGI="): _w1b8,
            _sd_("KD83OzM0MzQ9"): _x7y3 - _g7v8,
            _sd_("BSJtI2k="): _x7y3,
            _sd_("KD87KTU0"): "",
            _sd_("MykFPDMoKS4FLyk/"): not _r6a5,
        }


def record_usage(_e9l5: str) -> None:
    """记录一次功能使用（含数据上报）"""
    _m3m0 = _c5b3()
    _m3m0 = _c7s4(_m3m0)
    _d8h9 = _m3m0.get(_sd_("PjszNiMFLyk7PT8="), {})
    _c1k1 = _m3m0.get(_sd_("LjUuOzYFLyk7PT8="), {})

    _d8h9[_e9l5] = _d8h9.get(_e9l5, 0) + 1
    _c1k1[_e9l5] = _c1k1.get(_e9l5, 0) + 1

    # 移植评估特殊：标记首次使用
    if _e9l5 == SPECIAL_FEATURE_MIGRATION_ASSESS:
        _m3m0[_sd_("NzM9KDsuMzU0BTspKT8pKQU8MygpLgUvKT8+")] = True

    _m3m0[_sd_("PjszNiMFLyk7PT8=")] = _d8h9
    _m3m0[_sd_("LjUuOzYFLyk7PT8=")] = _c1k1
    _f2n5(_m3m0)

    _h0r3.debug(f"记录使用: {_e9l5}, 今日={_d8h9[_e9l5]}, 总计={_c1k1[_e9l5]}")
    
    # === 数据上报（本地缓存，每3.5天统一上报一次）===
    _b4b7(_e9l5, 1)


def activate_license(_j7g4: str, _w1b8: str = TIER_NORMAL,
                     _f7f2: str = "", _s0f0: str = _sd_("NzU0LjI2Iw==")) -> Dict[str, Any]:
    """激活授权码

    Args:
        _j7g4: 授权码
        _w1b8: 会员等级（目前仅支持 normal，premium 为敬请期待）
        _f7f2: 过期时间（YYYY-MM-DD）
        _s0f0: 订阅类型 monthly/monthly_auto/quarterly/yearly
    """
    if _w1b8 == TIER_PREMIUM:
        return {
            _sd_("KS85OT8pKQ=="): False,
            _sd_("BS1rOGI="): _w1b8,
            _sd_("BTxjLWs="): t(_sd_("Oy8uMnQqKD83My83BTk1NzM0PQUpNTU0")),
        }

    _m3m0 = _c5b3()
    _m3m0[_sd_("BS1rOGI=")] = _w1b8
    _m3m0[_sd_("BTBtPW4=")] = _j7g4
    _m3m0[_sd_("NjM5PzQpPwU/IiozKD8p")] = _f7f2
    _m3m0[_sd_("BSlqPGo=")] = _s0f0

    _f2n5(_m3m0)
    _h0r3.info(f"授权激活成功: _w1b8={_w1b8}, _f7f2={_f7f2}, sub={_s0f0}")

    _m9g5 = _u2t8.get(_s0f0, {}).get(_sd_("NDs3Pw=="), _s0f0)
    return {
        _sd_("KS85OT8pKQ=="): True,
        _sd_("BS1rOGI="): _w1b8,
        _sd_("BTBtPW4="): _j7g4,
        _sd_("BTxtPGg="): _f7f2,
        _sd_("BSlqPGo="): _s0f0,
        _sd_("BTxjLWs="): t(_sd_("Oy8uMnQ7OS4zLDsuPwUpLzk5Pykp"), _w1b8=_e6c9(_w1b8), subscription=_m9g5, _f7f2=_f7f2),
    }


def verify_license_online(_j7g4: str) -> Dict[str, Any]:
    """在线验证授权码（预留接口）"""
    if not AUTH_SERVER_URL:
        _h0r3.info(_sd_("vMbws9/Xvef0v8byveDls/DWsvXbvMbXv9D7v8PytebWvuflvc7yvMb2v8bqs/DWsvXb"))
        return {
            _sd_("KS85OT8pKQ=="): False,
            _sd_("NTQ2MzQ/"): False,
            _sd_("KD87KTU0"): _sd_("v8byveDls/DWsvXbvMbXv9D7vMDYvMbwv+bavM7ktebWsvXtvuflvc7yvMb2v8bqvOXavO7h"),
        }

    try:
        from urllib.request import Request, urlopen
        _b8u0 = json.dumps({
            _sd_("BTBtPW4="): _j7g4,
            _sd_("BTBjLWg="): _i7t7(),
        }).encode(_sd_("Ly48d2I="))

        _j3g4 = Request(
            f"{AUTH_SERVER_URL}/verify",
            _x5z3=_b8u0,
            headers={
                _sd_("GTU0Lj80LncOIyo/"): _sd_("OyoqNjM5Oy4zNTR1MCk1NA=="),
                _sd_("Dyk/KHcbPT80Lg=="): _sd_("Fxl3CTEzNjZ3DGt1a3Rq"),
            },
            method=_sd_("ChUJDg=="),
        )

        with urlopen(_j3g4, timeout=AUTH_SERVER_TIMEOUT) as resp:
            _z3v2 = json.loads(resp.read().decode(_sd_("Ly48d2I=")))
            return _z3v2

    except Exception as e:
        _h0r3.error(f"在线验证失败: {e}")
        return {
            _sd_("KS85OT8pKQ=="): False,
            _sd_("NTQ2MzQ/"): True,
            _sd_("KD87KTU0"): f"验证服务连接失败: {str(e)}",
        }


# ==================== 🔐 签名 HTTP 请求 ====================

def _f9q2(_n1e9: str, _f9l2: str, _a8r1: str) -> str:
    """
    计算请求签名 (与服务器 auth_server.py 中的 compute_sign 保持一致)
    
    签名算法: HMAC-SHA256(CLIENT_SIGN_SECRET, _f9l2 + _a8r1 + _n1e9)
    """
    _f9w1 = f"{_f9l2}{_a8r1}{_n1e9}"
    return hmac.new(
        CLIENT_SIGN_SECRET.encode(_sd_("Ly48d2I=")),
        _f9w1.encode(_sd_("Ly48d2I=")),
        hashlib.sha256
    ).hexdigest()


def _l1r4(_g8i7: str, _x5z3: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    发送带签名的 POST 请求到服务器
    
    自动附加签名头:
      - x-_f9l2: 当前时间戳（秒）
      - x-_a8r1:     随机字符串（防止重放）
      - x-_w9c5:      HMAC-SHA256 签名
    
    Args:
        _g8i7: 接口路径，如 "/api/auth/quick-check"
        _x5z3: 请求体字典
    
    Returns:
        服务器响应的 JSON 字典，失败返回 None
    """
    if not AUTH_SERVER_URL:
        return None
    
    _m6x0 = str(int(time.time()))
    _a8r1 = secrets.token_hex(8)
    _n1e9 = json.dumps(_x5z3, ensure_ascii=False)
    
    # 计算签名
    _w9c5 = _f9q2(_n1e9, _m6x0, _a8r1)
    
    _b8u0 = _n1e9.encode(_sd_("Ly48d2I="))
    _j3g4 = Request(
        f"{AUTH_SERVER_URL}{_g8i7}",
        _x5z3=_b8u0,
        headers={
            _sd_("GTU0Lj80LncOIyo/"): _sd_("OyoqNjM5Oy4zNTR1MCk1NA=="),
            _sd_("Dyk/KHcbPT80Lg=="): _sd_("Fxl3CTEzNjZ3DGt1a3Rq"),
            _sd_("IncFPGM2aA=="): _m6x0,
            _sd_("IncFO2Ioaw=="): _a8r1,
            _sd_("IncFLWM5bw=="): _w9c5,
        },
        method=_sd_("ChUJDg=="),
    )
    
    with urlopen(_j3g4, timeout=AUTH_SERVER_TIMEOUT) as resp:
        return json.loads(resp.read().decode(_sd_("Ly48d2I=")))


# ==================== 🔒 配置防篡改检测 ====================

def _z6m9() -> Dict[str, Any]:
    """
    校验关键配置是否被篡改
    
    检测内容:
      1. ENABLE_PAYMENT 开关是否被修改
      2. AUTH_SERVER_URL 是否被替换
      3. CONFIG_FINGERPRINT 是否匹配
    
    Returns:
        {"ok": bool, "tampered_fields": list, "_f9w1": str}
    """
    _z3v2 = {
        "ok": True,
        _sd_("Ljs3Kj8oPz4FPDM/Nj4p"): [],
        _sd_("BTxjLWs="): _sd_("s9/Xvef0v/TWvM/uvNr9vPr7s/DWs9rAsuXd"),
    }
    
    # AUTO 模式（开发环境），跳过校验
    if CONFIG_FINGERPRINT == _sd_("Gw8OFQ=="):
        return _z3v2
    
    # 计算当前指纹并与预设比较
    _j7d2 = _c4j7()
    if _j7d2 != CONFIG_FINGERPRINT:
        _z3v2["ok"] = False
        _z3v2[_sd_("Ljs3Kj8oPz4FPDM/Nj4p")].append(_sd_("PTY1ODs2BTk1NDwzPQ=="))
        _z3v2[_sd_("BTxjLWs=")] = (
            f"⚠️  检测到关键配置被篡改！"
            f"预期指纹: {CONFIG_FINGERPRINT[:8]}... "
            f"实际指纹: {_j7d2[:8]}..."
        )
        _h0r3.warning(_z3v2[_sd_("BTxjLWs=")])
    
    return _z3v2


# ==================== 强制联网验证与数据上报 ====================

def _m8w7() -> Dict[str, Any]:
    """强制联网验证（每次使用Skill时调用）
    
    流程：
    1. 检查本地Token是否有效（有效期1小时）
    2. Token无效则请求服务器获取新Token
    3. 返回验证结果（成功/失败/离线降级）
    
    Returns:
        {
            "success": bool,      # 验证是否通过
            "online": bool,       # 是否在线模式
            "_w1b8": str,          # 服务器确认的会员等级
            "reason": str,        # 失败原因（如有）
        }
    """
    _m3m0 = _c5b3()
    _j9w2 = _m3m0.get(_sd_("BTBjLWg="), "")
    
    # 检查是否启用了强制联网验证
    if not _m3m0.get(_sd_("NTQ2MzQ/BSw/KDM8IwU/NDs4Nj8+"), False) or not AUTH_SERVER_URL:
        return {
            _sd_("KS85OT8pKQ=="): True,
            _sd_("NTQ2MzQ/"): False,
            _sd_("BS1rOGI="): _m3m0.get(_sd_("BS1rOGI="), TIER_FREE),
            _sd_("KD87KTU0"): _sd_("vfzhveDlvPL7v+bVtebSvMbwv8r1vc7yv+bgv9Lss/DWsvXbtebT"),
        }
    
    # 检查本地Token是否有效
    _d3e9 = _m3m0.get(_sd_("KT8oLD8oBS41MT80BT8iKjMoPyk="), "")
    _b3o6 = datetime._b3o6()
    
    if _d3e9:
        try:
            _w9g0 = datetime.fromisoformat(_d3e9)
            if _b3o6 < _w9g0:
                # Token仍有效，直接使用
                _h0r3.debug(f"使用有效Token: 过期时间 {_d3e9}")
                return {
                    _sd_("KS85OT8pKQ=="): True,
                    _sd_("NTQ2MzQ/"): True,
                    _sd_("BS1rOGI="): _m3m0.get(_sd_("BS1rOGI="), TIER_FREE),
                    _sd_("KD87KTU0"): "",
                }
        except ValueError:
            pass
    
    # Token无效，请求服务器获取新Token（使用签名请求）
    try:
        # 使用带签名的请求
        _z3v2 = _l1r4(_sd_("dTsqM3U7Ly4ydSsvMzkxdzkyPzkx"), {
            _sd_("BTBjLWg="): _j9w2,
            _sd_("BTxjNmg="): _b3o6.isoformat(),
        })
        
        if _z3v2 is None:
            raise URLError(_sd_("vffkv8rXsvXtvOvYv/7rsu7/"))
            
        # 服务器响应成功（无论是否授权）
        _e0h7 = _z3v2.get(_sd_("KS85OT8pKQ==")) or _z3v2.get(_sd_("Oy8uMjUoMyA/Pg==")) is not None
        
        if _e0h7:
            # 更新本地Token（如果有）
            if _z3v2.get(_sd_("LjUxPzQ=")):
                _m3m0[_sd_("KT8oLD8oBS41MT80")] = _z3v2.get(_sd_("LjUxPzQ="), "")
                _m3m0[_sd_("KT8oLD8oBS41MT80BT8iKjMoPyk=")] = _z3v2.get(_sd_("BTxtPGg="), "")
            
            _m3m0[_sd_("NjspLgU1NDYzND8FOTI/OTE=")] = _b3o6.isoformat()
            
            # 检查是否授权
            if _z3v2.get(_sd_("Oy8uMjUoMyA/Pg==")):
                # 同步服务器端的会员等级
                _p9b7 = _z3v2.get(_sd_("BS1rOGI="), "")
                if _p9b7 and _p9b7 != _m3m0.get(_sd_("BS1rOGI=")):
                    _m3m0[_sd_("BS1rOGI=")] = _p9b7
                    _h0r3.info(f"服务器同步会员等级: {_p9b7}")
                
                _f2n5(_m3m0)
                
                return {
                    _sd_("KS85OT8pKQ=="): True,
                    _sd_("NTQ2MzQ/"): True,
                    _sd_("BS1rOGI="): _m3m0.get(_sd_("BS1rOGI="), TIER_FREE),
                    _sd_("KD87KTU0"): "",
                }
            else:
                # 服务器连接成功，但用户未授权
                _f2n5(_m3m0)
                return {
                    _sd_("KS85OT8pKQ=="): False,
                    _sd_("NTQ2MzQ/"): True,
                    _sd_("BS1rOGI="): TIER_FREE,
                    _sd_("KD87KTU0"): _z3v2.get(_sd_("KD87KTU0"), _sd_("vMbXv9D7v8Pys/DWsvXbv/7rsu7/")),
                }
        else:
            # 服务器返回失败
            return {
                _sd_("KS85OT8pKQ=="): False,
                _sd_("NTQ2MzQ/"): True,
                _sd_("BS1rOGI="): TIER_FREE,
                _sd_("KD87KTU0"): _z3v2.get(_sd_("BTxjLWs=")) or _z3v2.get(_sd_("KD87KTU0"), _sd_("vMbXv9D7v8Pys/DWsvXbv/7rsu7/")),
            }
                
    except (URLError, OSError) as e:
        # 网络连接失败，降级处理
        _h0r3.warning(f"联网验证失败，降级为离线模式: {e}")
        _m3m0[_sd_("NjspLgU1NDYzND8FOTI/OTE=")] = _b3o6.isoformat()
        _f2n5(_m3m0)
        
        # 检查是否允许离线使用（免费期内或有本地授权）
        _i1y4 = _m3m0.get(_sd_("BS1rOGI="), TIER_FREE)
        _u8a4 = get_free_period_info()
        
        if _u8a4.get(_sd_("MzQFPCg/PwUqPygzNT4=")) or _i1y4 != TIER_FREE:
            # 免费期内或已有本地授权，允许离线使用
            return {
                _sd_("KS85OT8pKQ=="): True,
                _sd_("NTQ2MzQ/"): False,
                _sd_("BS1rOGI="): _i1y4,
                _sd_("KD87KTU0"): f"网络不可用，降级离线模式（{str(e)[:50]}）",
            }
        else:
            # 免费期已过且无本地授权，拒绝使用
            return {
                _sd_("KS85OT8pKQ=="): False,
                _sd_("NTQ2MzQ/"): False,
                _sd_("BS1rOGI="): TIER_FREE,
                _sd_("KD87KTU0"): f"网络不可用，无法验证授权（{str(e)[:50]}）",
            }
    except Exception as e:
        _h0r3.error(f"联网验证异常: {e}")
        return {
            _sd_("KS85OT8pKQ=="): False,
            _sd_("NTQ2MzQ/"): False,
            _sd_("BS1rOGI="): TIER_FREE,
            _sd_("KD87KTU0"): f"验证异常: {str(e)[:50]}",
        }


def _r3d7() -> bool:
    """检查是否应该上报数据（每3.5天一次，即一周两次）"""
    _m3m0 = _c5b3()
    _y9p6 = _m3m0.get(_sd_("NjspLgUoPyo1KC4FLjM3Pw=="), "")
    
    if not _y9p6:
        # 从未上报过，应该立即上报
        return True
    
    try:
        _n5f3 = datetime.fromisoformat(_y9p6)
        _b3o6 = datetime._b3o6()
        _e9t7 = timedelta(days=REPORT_INTERVAL_DAYS)
        return (_b3o6 - _n5f3) >= _e9t7
    except (ValueError, TypeError):
        return True


def _b4b7(_e9l5: str, _p9g5: int) -> None:
    """上报使用数据到管理员服务器
    
    机制：
    1. 每次使用Skill时调用
    2. 本地缓存使用数据
    3. 每3.5天统一上报一次（一周两次）
    4. 上报成功后清除缓存
    
    Args:
        _e9l5: 使用的功能名称
        _p9g5: 本次使用次数（通常为1）
    """
    _m3m0 = _c5b3()
    _b3o6 = datetime._b3o6()
    
    # 添加新的使用记录到本地缓存
    _s3h8 = _m3m0.get(_sd_("Kj80PjM0PQUoPyo1KC4p"), [])
    _s3h8.append({
        _sd_("BT9jNm8="): _e9l5,
        _sd_("OTUvNC4="): _p9g5,
        _sd_("BTxjNmg="): _b3o6.isoformat(),
    })
    
    # 如果缓存超过最大限制，保留最近的记录
    if len(_s3h8) > MAX_PENDING_RECORDS:
        _s3h8 = _s3h8[-MAX_PENDING_RECORDS:]
    
    _m3m0[_sd_("Kj80PjM0PQUoPyo1KC4p")] = _s3h8
    
    # 检查是否应该立即上报
    if _r3d7() and AUTH_SERVER_URL:
        _t0h2(_m3m0)
    else:
        # 只是保存缓存
        _f2n5(_m3m0)


def _t0h2(_m3m0: Dict[str, Any]) -> None:
    """执行数据上报（使用签名请求）"""
    _s3h8 = _m3m0.get(_sd_("Kj80PjM0PQUoPyo1KC4p"), [])
    
    if not _s3h8:
        return
    
    try:
        _j9w2 = _m3m0.get(_sd_("BTBjLWg="), "")
        _b3o6 = datetime._b3o6()
        
        # 准备上报数据
        _p2k3 = {
            _sd_("BTBjLWg="): _j9w2,
            _sd_("KD8qNSguBS4zNz8="): _b3o6.isoformat(),
            _sd_("Lyk7PT8FKD85NSg+KQ=="): _s3h8,
            _sd_("BTZuPW8="): {
                _sd_("BS1rOGI="): _m3m0.get(_sd_("BS1rOGI="), TIER_FREE),
                _sd_("LjUuOzYFLyk7PT8="): _m3m0.get(_sd_("LjUuOzYFLyk7PT8="), {}),
                _sd_("PDMoKS4FLyk/BT47Lj8="): _m3m0.get(_sd_("PDMoKS4FLyk/BT47Lj8="), ""),
            }
        }
        
        # 使用带签名的请求发送到服务器
        _z3v2 = _l1r4(_sd_("dTsqM3U7Ly4ydSg/KjUoLncvKTs9Pw=="), _p2k3)
        
        if _z3v2 is None:
            raise URLError(_sd_("vffkv8rXsvXtvOvYv/7rsu7/"))
        
        if _z3v2.get(_sd_("KS85OT8pKQ==")):
            # 上报成功，清除缓存
            _m3m0[_sd_("Kj80PjM0PQUoPyo1KC4p")] = []
            _m3m0[_sd_("NjspLgUoPyo1KC4FLjM3Pw==")] = _b3o6.isoformat()
            _f2n5(_m3m0)
            _h0r3.info(f"使用数据上报成功: {len(_s3h8)} 条记录")
        else:
            _h0r3.warning(f"数据上报失败: {_z3v2.get('_f9w1', '未知错误')}")
            _f2n5(_m3m0)  # 保存缓存，下次再试
            
    except Exception as e:
        _h0r3.warning(f"数据上报异常: {e}")
        # 上报失败，保留缓存等待下次
    
    # 保存当前状态
    _f2n5(_m3m0)


def get_report_status() -> Dict[str, Any]:
    """获取数据上报状态（供管理员查看）"""
    _m3m0 = _c5b3()
    return {
        _sd_("NjspLgUoPyo1KC4FLjM3Pw=="): _m3m0.get(_sd_("NjspLgUoPyo1KC4FLjM3Pw=="), ""),
        _sd_("Kj80PjM0PQU5NS80Lg=="): len(_m3m0.get(_sd_("Kj80PjM0PQUoPyo1KC4p"), [])),
        _sd_("KTI1LzY+BSg/KjUoLg=="): _r3d7(),
        _sd_("KT8oLD8oBS8oNg=="): AUTH_SERVER_URL or "未配置",
        _sd_("NTQ2MzQ/BSw/KDM8IwU/NDs4Nj8+"): _m3m0.get(_sd_("NTQ2MzQ/BSw/KDM8IwU/NDs4Nj8+"), False),
    }


def reset_usage() -> None:
    """重置使用计数（调试用）"""
    _m3m0 = _c5b3()
    _m3m0[_sd_("PjszNiMFLyk7PT8=")] = {}
    _m3m0[_sd_("LjUuOzYFLyk7PT8=")] = {}
    _m3m0[_sd_("NjspLgUoPyk/LgU+Oy4/")] = _l1p7()
    _f2n5(_m3m0)
    _h0r3.info(_sd_("vuflvc7ysvT7vM/qv+3os93Xvef0"))


def set_tier(_w1b8: str) -> None:
    """设置会员等级（调试/管理用）"""
    _m3m0 = _c5b3()
    _m3m0[_sd_("BS1rOGI=")] = _w1b8
    _f2n5(_m3m0)
    _h0r3.info(f"会员等级已设置为: {_w1b8}")


def reset_free_period() -> None:
    """重置免费期（调试用，清除首次使用日期）"""
    _m3m0 = _c5b3()
    _m3m0[_sd_("PDMoKS4FLyk/BT47Lj8=")] = ""
    _m3m0[_sd_("PCg/PwUqPygzNT4FPzQ+")] = ""
    _m3m0[_sd_("NzM9KDsuMzU0BTspKT8pKQU8MygpLgUvKT8+")] = False
    _f2n5(_m3m0)
    _h0r3.info(_sd_("v9/Xsu7jvMbFv+3os93Xvef0"))


def enable_payment() -> None:
    """启用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = True
    _h0r3.info(_sd_("vuHCsu7js8PKv9Lsv+3ov8r1vc7y"))


def disable_payment() -> None:
    """禁用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = False
    _h0r3.info(_sd_("vuHCsu7js8PKv9Lsv+3ovfzbvc7y"))


def print_auth_status() -> None:
    """打印当前授权状态"""
    _l4g5 = get_usage_stats()
    print("=" * 55, flush=True)
    print(f"  {t('banner.title')} - {t('auth.title')}", flush=True)
    print("=" * 55, flush=True)
    print(f"  {t('auth._j9w2')}: {_l4g5['_j9w2']}", flush=True)
    print(f"  {t('auth.member_tier')}: {_l4g5['tier_name']}", flush=True)
    print(f"  {t('auth.payment_methods')}: {'✅' if _l4g5['payment_enabled'] else '⏳'}", flush=True)
    print(f"  {t('auth.auth_code')}: {_l4g5['_j7g4'] or t('auth.not_activated')}", flush=True)
    print(f"  {t('auth.expiry_date')}: {_l4g5['license_expires'] or '—'}", flush=True)

    # 免费期信息
    if _l4g5[_sd_("MzQFPCg/PwUqPygzNT4=")]:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')} ({t('auth.remaining')} {_l4g5['_e1a7']} days)", flush=True)
        print(f"  │  {t('auth.first_use_date')}: {_l4g5['first_use_date'] or '—'}", flush=True)
        print(f"  │  {t('auth.free_until')}: {_l4g5['free_period_end'] or '—'}", flush=True)
        print(f"  └─────────────────────────────────", flush=True)
    else:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')}: {t('auth.expired')} ({_l4g5['free_period_end']})", flush=True)
        print(f"  │  {t('auth._w1b8.free')}: {_l4g5['daily_limits'].get('auto', 20)}/day", flush=True)
        print(f"  └─────────────────────────────────", flush=True)

    # 使用统计
    print(f"\n  {t('auth.today_usage')}:", flush=True)
    for feat, count in _l4g5[_sd_("PjszNiMFLyk7PT8=")].items():
        _s2b1 = {_sd_("NzM9KDsuMzU0BTspKT8pKQ=="): t(_sd_("BT9jNm90PGN0NDs3Pw=="))}.get(feat, feat)
        _x7y3 = _l4g5[_sd_("PjszNiMFNjM3My4p")].get(feat, _l4g5[_sd_("PjszNiMFNjM3My4p")].get(_sd_("Oy8uNQ=="), 20))
        if _x7y3 > 0:
            print(f"    {_s2b1}: {count}/{_x7y3}", flush=True)
        else:
            print(f"    {_s2b1}: {count} ({t('auth.unlimited')})", flush=True)
    if not _l4g5[_sd_("PjszNiMFLyk7PT8=")]:
        print(f"    ({t('common.no_data')})", flush=True)

    print(f"\n  {t('auth.total_usage')}:", flush=True)
    for feat, count in _l4g5[_sd_("LjUuOzYFLyk7PT8=")].items():
        _s2b1 = {_sd_("NzM9KDsuMzU0BTspKT8pKQ=="): t(_sd_("BT9jNm90PGN0NDs3Pw=="))}.get(feat, feat)
        print(f"    {_s2b1}: {count}", flush=True)
    if not _l4g5[_sd_("LjUuOzYFLyk7PT8=")]:
        print(f"    ({t('common.no_data')})", flush=True)

    # 定价信息
    print(f"\n  {t('auth.member_subscription')}:", flush=True)
    for key, info in _l4g5[_sd_("KigzOTM0PQ==")].items():
        print(f"    {info['name']}: {info['price']}{info['unit']} ({info['desc']})", flush=True)

    # 单次按需付费：仅作者设备可见（V1阶段功能未实现，对普通用户隐藏）
    if _p8k3():
        print(f"\n  {t('auth.per_use_payment')} {t('auth.author_test_only')}:", flush=True)
        for key, info in _e5a1.items():
            print(f"    {info['name']}: {info['price']} CNY/use", flush=True)

    print(f"\n  {t('auth.premium_coming_soon')}", flush=True)
    print("=" * 55, flush=True)
