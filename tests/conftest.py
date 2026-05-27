import pandas as pd
import pytest
from src.data.loader import _enrich


@pytest.fixture
def sample_df():
    data = {
        "SID": (
            ["2017228N14314"] * 5
            + ["2007235N14314"] * 5
            + ["2005236N20280"] * 5
        ),
        "NAME": ["IRMA"] * 5 + ["DEAN"] * 5 + ["KATRINA"] * 5,
        "year": [2017] * 5 + [2007] * 5 + [2005] * 5,
        "month": [9] * 5 + [8] * 5 + [8] * 5,
        "day": [6, 7, 8, 9, 10] + [17, 18, 19, 20, 21] + [25, 26, 27, 28, 29],
        "LAT": [
            17.0, 17.5, 18.0, 19.0, 20.0,
            15.0, 16.0, 17.0, 18.0, 19.0,
            23.0, 24.0, 25.0, 26.0, 27.0,
        ],
        "LON": [
            -63.0, -64.0, -65.0, -66.0, -67.0,
            -61.0, -62.0, -63.0, -64.0, -65.0,
            -75.0, -76.0, -77.0, -78.0, -79.0,
        ],
        "USA_WIND": [
            155, 165, 150, 100, 75,
            140, 135, 130, 90, 65,
            120, 115, 110, 80, 55,
        ],
        "USA_PRES": [
            914, 910, 915, 950, 975,
            905, 910, 915, 945, 970,
            918, 920, 920, 948, 972,
        ],
        "BASIN": ["AL"] * 15,
    }
    return pd.DataFrame(data)


@pytest.fixture
def enriched_df(sample_df):
    return _enrich(sample_df)


@pytest.fixture
def sample_earthquakes_df():
    return pd.DataFrame({
        "magnitude": [7.2, 6.1, 5.8, 5.3, 4.7, 4.2],
        "latitude":  [18.4, 15.0, 17.8, 19.0, 13.5, 21.0],
        "longitude": [-72.5, -61.0, -66.8, -70.0, -60.5, -77.0],
        "depth_km":  [10.0, 15.0, 8.5, 20.0, 12.0, 25.0],
        "place": [
            "Haiti", "Martinique", "Puerto Rico",
            "Dominican Republic", "Barbados", "Cuba",
        ],
        "time": pd.to_datetime([
            "2021-08-14", "2015-06-10", "2020-01-07",
            "2003-09-22", "1999-04-05", "1992-07-30",
        ]),
        "year":  [2021, 2015, 2020, 2003, 1999, 1992],
        "month": [8, 6, 1, 9, 4, 7],
    })


@pytest.fixture
def sample_sst_df():
    import math as _math
    years  = [y for y in range(1980, 2026) for _ in range(12)]
    months = list(range(1, 13)) * 46
    # Caribbean average ~28°C, seasonal variation (+1.8°C trend over 45 years)
    # sin((m-5)*π/6) peaks at month 8 (August), correct for Caribbean SST
    sst = [
        27.5
        + 1.5 * _math.sin((m - 5) * _math.pi / 6)
        + 1.8 * (y - 1980) / 45
        for y, m in zip(years, months)
    ]
    return pd.DataFrame({"year": years, "month": months, "sst_c": sst})
