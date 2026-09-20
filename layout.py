"""
Layout дашборда. Чистая разметка, без логики.

Структура (как на референсе):
    ┌─────────────────────────────────────────────────────────────┐
    │  ┌──────┐  ┌──────────────────────────────┐  ┌──────────┐  │
    │  │ Today│  │                              │  │ ✎  ▾     │  │
    │  │ 0%   │  │        CHART (Plotly)        │  └──────────┘  │
    │  │ $0   │  │                              │                │
    │  │ $0   │  │                              │                │
    │  │ 0    │  └──────────────────────────────┘                │
    │  │ 0    │                                                  │
    │  └──────┘                                                  │
    └─────────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

from dash import dcc, html

import config as cfg


# ---------------------------------------------------------------------------
# Публичная функция
# ---------------------------------------------------------------------------
def build_layout(figure) -> html.Div:
    """
    Собирает корневой layout.
    `figure` — уже готовая plotly Figure (см. chart.build_figure).
    """
    return html.Div(
        id="app-root",
        style=_root_style(),
        children=[
            html.Div(
                id="app-card",
                style=_card_style(),
                children=[
                    _sidebar(),
                    _chart_area(figure),
                    _toolbar(),
                ],
            )
        ],
    )


# ---------------------------------------------------------------------------
# Блоки
# ---------------------------------------------------------------------------
def _sidebar() -> html.Div:
    items = []
    for i, value in enumerate(cfg.SIDEBAR_METRICS):
        items.append(
            html.Div(
                value,
                style=_metric_style(is_first=(i == 0)),
            )
        )
    return html.Div(id="sidebar", style=_sidebar_style(), children=items)


def _chart_area(figure) -> html.Div:
    return html.Div(
        id="chart-area",
        style=_chart_area_style(),
        children=[
            dcc.Graph(
                id="main-chart",
                figure=figure,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                    "scrollZoom": False,
                    "doubleClick": False,
                    "showTips": False,
                },
                style={"height": "100%", "width": "100%"},
            )
        ],
    )


def _toolbar() -> html.Div:
    return html.Div(
        id="toolbar",
        style=_toolbar_style(),
        children=[
            html.Button(
                "✎",
                id="btn-edit",
                n_clicks=0,
                style=_toolbar_btn_style(),
                title="Edit",
            ),
            html.Button(
                "▾",
                id="btn-dropdown",
                n_clicks=0,
                style=_toolbar_btn_style(),
                title="More",
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Стили (инлайн — чтобы не плодить классы; CSS-файл всё равно добавим
# для hover/анимаций и точной подгонки)
# ---------------------------------------------------------------------------
def _root_style() -> dict:
    return {
        "backgroundColor": cfg.BG_APP,
        "minHeight": "100vh",
        "padding": cfg.APP_PADDING,
        "fontFamily": cfg.FONT_FAMILY,
        "fontSize": cfg.FONT_SIZE_BASE,
        "color": cfg.TEXT_PRIMARY,
        "boxSizing": "border-box",
    }


def _card_style() -> dict:
    return {
        "position": "relative",
        "display": "grid",
        "gridTemplateColumns": f"{cfg.SIDEBAR_WIDTH} 1fr",
        "gap": "18px",
        "backgroundColor": cfg.BG_APP,   # на референсе фон карточки = фону app
        "borderRadius": cfg.CARD_RADIUS,
        "padding": "6px",
    }


def _sidebar_style() -> dict:
    return {
        "display": "flex",
        "flexDirection": "column",
        "gap": "10px",
        "paddingTop": "4px",
    }


def _metric_style(is_first: bool = False) -> dict:
    base = {
        "backgroundColor": cfg.BG_CARD,
        "borderRadius": cfg.CARD_RADIUS,
        "padding": "10px 12px",
        "fontSize": cfg.FONT_SIZE_METRIC,
        "color": cfg.TEXT_PRIMARY if is_first else cfg.TEXT_SECONDARY,
        "textAlign": "left",
        "lineHeight": "1.1",
        "minHeight": "34px",
        "boxSizing": "border-box",
        "border": f"1px solid {cfg.BORDER_SOFT}",
    }
    if is_first:
        base["fontWeight"] = "600"
    return base


def _chart_area_style() -> dict:
    return {
        "position": "relative",
        "backgroundColor": cfg.BG_CHART,
        "border": f"1px solid {cfg.BORDER_SOFT}",
        "borderRadius": cfg.CARD_RADIUS,
        "padding": "8px 6px 4px 6px",
        "minHeight": f"{cfg.CHART_HEIGHT}px",
        "boxSizing": "border-box",
    }


def _toolbar_style() -> dict:
    return {
        "position": "absolute",
        "top": "-2px",
        "right": "6px",
        "display": "flex",
        "gap": "6px",
        "alignItems": "center",
    }


def _toolbar_btn_style() -> dict:
    return {
        "backgroundColor": cfg.BG_CARD,
        "border": f"1px solid {cfg.BORDER_SOFT}",
        "borderRadius": "8px",
        "width": "34px",
        "height": "28px",
        "cursor": "pointer",
        "fontSize": "14px",
        "color": cfg.TEXT_SECONDARY,
        "display": "inline-flex",
        "alignItems": "center",
        "justifyContent": "center",
        "padding": "0",
        "outline": "none",
    }