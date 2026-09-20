"""
Источник данных для графика.

Публичная функция:
    get_series(cost=None, cpa=None, roi=None, conversions=None,
               dates=None, csv_path=None) -> pd.DataFrame

Правила приоритета:
    1. Если переданы все 4 последовательности списками — берём их.
    2. Иначе, если передан csv_path — читаем CSV.
    3. Иначе читаем data/series.csv (если есть).
    4. Иначе генерируем демо-данные в форме референса.

Формат CSV:
    date,cost,cpa,roi,conversions
    2026-06-01,10,1.2,50,3
    ...
"""

from __future__ import annotations

import os
from typing import Optional, Sequence

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Пути
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_CSV = os.path.join(DATA_DIR, "series.csv")

# Имена колонок — единый контракт для всего проекта
COL_DATE = "date"
COL_COST = "cost"
COL_CPA = "cpa"
COL_ROI = "roi"
COL_CONV = "conversions"

REQUIRED_COLUMNS = [COL_DATE, COL_COST, COL_CPA, COL_ROI, COL_CONV]


# ---------------------------------------------------------------------------
# Публичная функция
# ---------------------------------------------------------------------------
def get_series(
    cost: Optional[Sequence[float]] = None,
    cpa: Optional[Sequence[float]] = None,
    roi: Optional[Sequence[float]] = None,
    conversions: Optional[Sequence[float]] = None,
    dates: Optional[Sequence] = None,
    csv_path: Optional[str] = None,
) -> pd.DataFrame:
    """
    Возвращает DataFrame с колонками:
        date, cost, cpa, roi, conversions

    Приоритет источников описан в docstring модуля.
    """
    if _all_sequences_provided(cost, cpa, roi, conversions):
        return _from_sequences(cost, cpa, roi, conversions, dates)

    if csv_path is not None:
        return _from_csv(csv_path)

    if os.path.exists(DEFAULT_CSV):
        return _from_csv(DEFAULT_CSV)

    return _demo_frame()


# ---------------------------------------------------------------------------
# Внутренние билдеры
# ---------------------------------------------------------------------------
def _all_sequences_provided(*seqs) -> bool:
    return all(s is not None and len(s) > 0 for s in seqs)


def _from_sequences(cost, cpa, roi, conversions, dates) -> pd.DataFrame:
    lengths = {len(cost), len(cpa), len(roi), len(conversions)}
    if len(lengths) != 1:
        raise ValueError(
            "Все 4 последовательности должны быть одинаковой длины. "
            f"Получено: cost={len(cost)}, cpa={len(cpa)}, "
            f"roi={len(roi)}, conversions={len(conversions)}"
        )

    n = lengths.pop()
    if dates is None:
        dates = _default_dates(n)
    if len(dates) != n:
        raise ValueError(
            f"len(dates)={len(dates)} != len(series)={n}"
        )

    return pd.DataFrame(
        {
            COL_DATE: pd.to_datetime(list(dates)),
            COL_COST: list(cost),
            COL_CPA: list(cpa),
            COL_ROI: list(roi),
            COL_CONV: list(conversions),
        }
    )


def _from_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV не найден: {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"В CSV не хватает колонок: {missing}. "
            f"Ожидаются: {REQUIRED_COLUMNS}"
        )

    df = df[REQUIRED_COLUMNS].copy()
    df[COL_DATE] = pd.to_datetime(df[COL_DATE])
    df = df.sort_values(COL_DATE).reset_index(drop=True)
    return df


def _default_dates(n: int) -> list[pd.Timestamp]:
    """n подряд идущих дней, заканчивая сегодняшним."""
    end = pd.Timestamp.today().normalize()
    return list(pd.date_range(end=end, periods=n, freq="D"))


def _demo_frame() -> pd.DataFrame:
    """
    Демо-данные в форме референса (12 точек, одна активная — посередине).
    Значения подобраны так, чтобы визуально совпадало с картинкой.
    """
    n = 12
    x = np.linspace(0, 1, n)

    # Cost: area растёт слева-направо, лёгкая волнистость
    cost = 8 + 42 * x + 4 * np.sin(x * np.pi * 2)

    # CPA: почти горизонтальная линия внизу с небольшим дрейфом
    cpa = np.full(n, 1.2)
    cpa[-3:] = 1.2  # оставляем ровной, как на референсе

    # ROI: spline с провалом в середине и подъёмом справа
    roi = 170 - 90 * np.sin(x * np.pi) + 25 * x

    # Conversions: монотонный рост с плато в начале
    conversions = np.concatenate(
        [np.linspace(0, 2, n // 3), np.linspace(2, 36, n - n // 3)]
    )

    return _from_sequences(cost, cpa, roi, conversions, _default_dates(n))


# ---------------------------------------------------------------------------
# Ручная проверка
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    df = get_series()
    print(df)
    print("\nshape:", df.shape)
    print("dtypes:\n", df.dtypes)