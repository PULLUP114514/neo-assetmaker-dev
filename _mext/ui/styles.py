"""_mext 扩展模块专用样式常量。

引用 gui/styles.py 的公共颜色/辅助函数，并定义
素材卡片、列表、间距等 _mext 专有尺寸常量。
"""

from __future__ import annotations

# 将主应用样式辅助函数重新导出，方便 _mext 内部直接 import
from gui.styles import (  # noqa: F401
    COLOR_ACCENT,
    COLOR_BG_ELEVATED,
    COLOR_BG_INSET,
    COLOR_BG_SURFACE,
    COLOR_BORDER,
    COLOR_ERROR,
    COLOR_SUCCESS,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_WARNING,
    apply_themed_style,
    pick,
)

# ── 素材卡片尺寸 ────────────────────────────────────────────
# 与 _mext/core/constants.py 中的 MATERIAL_CARD_WIDTH/HEIGHT 保持一致

CARD_WIDTH: int = 220
CARD_HEIGHT: int = 280
CARD_IMAGE_HEIGHT: int = 140   # 卡片顶部预览图高度（≈ 63% 卡片高）
CARD_BORDER_RADIUS: int = 8

# ── 通用间距 ────────────────────────────────────────────────

SPACING_XS: int = 4
SPACING_SM: int = 8
SPACING_MD: int = 12
SPACING_LG: int = 16
SPACING_XL: int = 24

# ── FlowLayout 卡片网格间距 ──────────────────────────────────

GRID_H_SPACING: int = 12
GRID_V_SPACING: int = 12

# ── 侧边过滤面板宽度 ─────────────────────────────────────────

FILTER_PANEL_WIDTH: int = 200

# ── 排序/通用 ComboBox 宽度 ──────────────────────────────────

COMBO_WIDTH_SM: int = 120      # 小型（如并发数，只有几个数字选项）
COMBO_WIDTH_MD: int = 150      # 中型（如排序方式）
COMBO_WIDTH_LG: int = 200      # 标准（与主应用统一）

# ── 卡片选中态颜色（用于 USB 设备卡片） ─────────────────────
# themeColor() 动态获取，这里只作 fallback

COLOR_SELECTION_BORDER = ("#ff6b8b", "#ff8fa3")   # (light, dark)

# ── 占位图颜色（替代硬编码 lightGray） ──────────────────────

COLOR_PLACEHOLDER_BG = ("#e0e0e0", "#3a3a3a")    # (light, dark)
COLOR_PLACEHOLDER_FG = ("#aaaaaa", "#666666")    # (light, dark)
