"""
pink-chart — точка входа.

Запуск:
    python app.py
Затем открыть http://127.0.0.1:8050
"""

from __future__ import annotations

import dash
from dash import Input, Output, State, html

import config as cfg
from chart import build_figure
from data import get_series
from layout import build_layout


# ---------------------------------------------------------------------------
# Данные + фигура (мок по умолчанию; см. data.get_series для своих данных)
# ---------------------------------------------------------------------------
def _make_app() -> dash.Dash:
    df = get_series()
    figure = build_figure(df)

    app = dash.Dash(
        __name__,
        title="pink-chart",
        update_title=None,      # убираем "Updating..." в табе
        suppress_callback_exceptions=True,
    )
    app.layout = build_layout(figure)
    _register_callbacks(app)
    return app


# ---------------------------------------------------------------------------
# Колбэки (пока заглушки — чтобы клики по кнопкам не падали)
# ---------------------------------------------------------------------------
def _register_callbacks(app: dash.Dash) -> None:
    @app.callback(
        Output("btn-edit", "n_clicks"),
        Input("btn-edit", "n_clicks"),
        State("btn-edit", "n_clicks"),
        prevent_initial_call=True,
    )
    def _noop_edit(n, _prev):
        # TODO: здесь будет открытие панели редактирования серий.
        print(f"[edit] clicked, n_clicks={n}")
        return dash.no_update

    @app.callback(
        Output("btn-dropdown", "n_clicks"),
        Input("btn-dropdown", "n_clicks"),
        State("btn-dropdown", "n_clicks"),
        prevent_initial_call=True,
    )
    def _noop_dropdown(n, _prev):
        # TODO: здесь будет выпадающее меню экспорта/настроек.
        print(f"[dropdown] clicked, n_clicks={n}")
        return dash.no_update


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------
app = _make_app()
server = app.server  # для gunicorn / wsgi


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=True,
        dev_tools_hot_reload=True,
    )