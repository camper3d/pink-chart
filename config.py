"""
Все визуальные константы графика.
Единственное место, где меняются цвета/размеры/шрифты.
"""

# ---------- Цвета фона ----------
BG_APP = "#fbe0e0"          # розово-персиковый фон приложения (как на референсе)
BG_CHART = "#fdf3f3"        # фон внутренней области графика (чуть светлее)
BG_CARD = "#ffffff"         # белые карточки: метрики, тултип, кнопка

BORDER_SOFT = "#e9c9c9"     # тонкая рамка вокруг чарта/карточек
GRID_COLOR = "#ecd7d7"      # горизонтальная сетка внутри графика

# ---------- Цвета серий ----------
COLOR_COST = "#f2e28a"      # жёлтый — area (Cost)
COLOR_CPA = "#3b6fe0"       # синий — line (CPA)
COLOR_ROI = "#2e8b2e"       # зелёный — spline (ROI confirmed)
COLOR_CONV = "#8a2be2"      # фиолетовый — bar (Conversions)

# ---------- Цвета текста ----------
TEXT_PRIMARY = "#1c1c1c"    # основной текст (тултип, названия)
TEXT_SECONDARY = "#8a8a8a"  # подписи осей, метрики сайдбара
TEXT_MUTED = "#b8b8b8"      # совсем бледное

# ---------- Тултип ----------
TOOLTIP_BG = "#ffffff"
TOOLTIP_RADIUS = "10px"
TOOLTIP_SHADOW = "0 6px 18px rgba(0, 0, 0, 0.12)"
TOOLTIP_PAD = "10px 14px"

# ---------- Размеры ----------
CHART_HEIGHT = 420          # высота области графика в px
APP_PADDING = "28px"        # отступ контейнера от краёв окна
CARD_RADIUS = "10px"        # скругление белых карточек
SIDEBAR_WIDTH = "90px"      # ширина левой колонки метрик

# ---------- Шрифты ----------
FONT_FAMILY = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', "
    "Roboto, Helvetica, Arial, sans-serif"
)
FONT_SIZE_BASE = "13px"
FONT_SIZE_TOOLTIP_TITLE = "13px"
FONT_SIZE_TOOLTIP_ROW = "13px"
FONT_SIZE_METRIC = "12px"

# ---------- Оси / сетка ----------
AXIS_LINE_COLOR = "#e9c9c9"     # цвет самой оси
AXIS_LINE_WIDTH = 1
GRID_WIDTH = 1
SHOW_Y_GRID = True
SHOW_X_GRID = False             # на референсе вертикальной сетки не видно

# ---------- Индикатор ховера ----------
HOVER_LINE_COLOR = "#c9a9a9"    # тонкая вертикальная линия под курсором
HOVER_LINE_WIDTH = 1

# ---------- Маркеры ----------
MARKER_SIZE = 7                 # базовый размер квадратных маркеров
MARKER_LINE_WIDTH = 0           # без обводки

# ---------- Порядок и подписи серий ----------
SERIES_COST = "Cost"
SERIES_CPA = "CPA"
SERIES_ROI = "ROI confirmed"
SERIES_CONV = "Conversions"

SERIES_ORDER = [SERIES_COST, SERIES_CPA, SERIES_ROI, SERIES_CONV]

SERIES_COLORS = {
    SERIES_COST: COLOR_COST,
    SERIES_CPA: COLOR_CPA,
    SERIES_ROI: COLOR_ROI,
    SERIES_CONV: COLOR_CONV,
}

# ---------- Метрики сайдбара (как на референсе, слева) ----------
SIDEBAR_METRICS = ["Today", "0%", "$0", "$0", "0", "0"]