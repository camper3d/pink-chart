"""
Сборка Plotly Figure для дашборда.

Публичная функция:
    build_figure(df: pd.DataFrame) -> go.Figure

Трейсы (в порядке отрисовки снизу вверх):
    1. Cost        — area (заливка tozeroy, без линии)
    2. CPA         — line + square-маркеры, тонкая, у нижней границы
    3. ROI confirmed — spline (плавная кривая), зелёная
    4. Conversions — bar-стиль: тонкая линия с square-маркерами

Ховер: 'x unified' + кастомный hovertemplate.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

import config as cfg
from data import COL_CONV, COL_COST, COL_CPA, COL_DATE, COL_ROI


# ---------------------------------------------------------------------------
# Публичная функция
# ---------------------------------------------------------------------------
def build_figure(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    # --- 1. Cost: area -----------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=df[COL_DATE],
            y=df[COL_COST],
            name=cfg.SERIES_COST,
            mode="lines",
            line=dict(color=cfg.COLOR_COST, width=0),
            fill="tozeroy",
            fillcolor=_alpha(cfg.COLOR_COST, 0.75),
            hovertemplate="%{y:.2f}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 2. CPA: line с квадратными маркерами ------------------------------
    fig.add_trace(
        go.Scatter(
            x=df[COL_DATE],
            y=df[COL_CPA],
            name=cfg.SERIES_CPA,
            mode="lines+markers",
            line=dict(color=cfg.COLOR_CPA, width=2),
            marker=dict(
                symbol="square",
                size=cfg.MARKER_SIZE,
                color=cfg.COLOR_CPA,
                line=dict(width=cfg.MARKER_LINE_WIDTH),
            ),
            hovertemplate="%{y:.2f}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 3. ROI confirmed: spline ------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=df[COL_DATE],
            y=df[COL_ROI],
            name=cfg.SERIES_ROI,
            mode="lines",
            line=dict(color=cfg.COLOR_ROI, width=2, shape="spline"),
            hovertemplate="%{y:.2f}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 4. Conversions: bar-стиль (линия + квадратные маркеры) ------------
    fig.add_trace(
        go.Scatter(
            x=df[COL_DATE],
            y=df[COL_CONV],
            name=cfg.SERIES_CONV,
            mode="lines+markers",
            line=dict(color=cfg.COLOR_CONV, width=2),
            marker=dict(
                symbol="square",
                size=cfg.MARKER_SIZE,
                color=cfg.COLOR_CONV,
                line=dict(width=cfg.MARKER_LINE_WIDTH),
            ),
            hovertemplate="%{y:.2f}<extra></extra>",
            showlegend=False,
        )
    )

    _apply_layout(fig)
    return fig


# ---------------------------------------------------------------------------
# Layout / оси / ховер
# ---------------------------------------------------------------------------
def _apply_layout(fig: go.Figure) -> None:
    fig.update_layout(
        # --- фон ---
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=cfg.BG_CHART,
        margin=dict(l=50, r=20, t=20, b=30),
        height=cfg.CHART_HEIGHT,
        font=dict(
            family=cfg.FONT_FAMILY,
            size=int(cfg.FONT_SIZE_BASE.replace("px", "")),
            color=cfg.TEXT_PRIMARY,
        ),
        # --- легенда выключена (в референсе её нет, роли в тултипе) ---
        showlegend=False,
        # --- ховер ---
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=cfg.TOOLTIP_BG,
            bordercolor=cfg.TOOLTIP_BG,
            font=dict(
                family=cfg.FONT_FAMILY,
                size=int(cfg.FONT_SIZE_TOOLTIP_ROW.replace("px", "")),
                color=cfg.TEXT_PRIMARY,
            ),
            align="left",
        ),
        # --- индикатор под курсором ---
        xaxis=dict(
            showgrid=cfg.SHOW_X_GRID,
            showline=True,
            linecolor=cfg.AXIS_LINE_COLOR,
            linewidth=cfg.AXIS_LINE_WIDTH,
            ticks="",
            tickfont=dict(color=cfg.TEXT_MUTED, size=11),
            showticklabels=False,  # на референсе подписи дат не видны на оси
            fixedrange=True,
        ),
        yaxis=dict(
            showgrid=cfg.SHOW_Y_GRID,
            gridcolor=cfg.GRID_COLOR,
            gridwidth=cfg.GRID_WIDTH,
            zeroline=False,
            showline=False,
            ticks="",
            tickfont=dict(color=cfg.TEXT_MUTED, size=11),
            fixedrange=True,
        ),
        # тонкая вертикальная линия под курсором
        shapes=[
            dict(
                type="line",
                xref="paper",
                x0=0,
                x1=0,
                yref="paper",
                y0=0,
                y1=1,
                line=dict(color=cfg.HOVER_LINE_COLOR, width=cfg.HOVER_LINE_WIDTH),
                opacity=0,
            )
        ],
    )

    # --- horizontal hover line (spikelines) ---
    fig.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikecolor=cfg.HOVER_LINE_COLOR,
        spikethickness=cfg.HOVER_LINE_WIDTH,
        spikedash="solid",
    )


# ---------------------------------------------------------------------------
# Утилиты
# ---------------------------------------------------------------------------
def _alpha(hex_color: str, alpha: float) -> str:
    """#rrggbb -> rgba(r, g, b, alpha)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


# ---------------------------------------------------------------------------
# Ручная проверка
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from data import get_series

    df = get_series()
    fig = build_figure(df)
    fig.write_html("preview.html", include_plotlyjs="cdn")
    print("Открыт preview.html — проверь визуал.")