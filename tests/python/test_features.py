import pandas as pd
from python.features.engineer import create_basic_features


def test_create_basic_features():
    data = {
        "Close": [100, 101, 102, 101, 103, 104, 105, 106, 107, 108],
        "High": [101, 102, 103, 102, 104, 105, 106, 107, 108, 109],
        "Low": [99, 100, 101, 100, 102, 103, 104, 105, 106, 107],
    }
    df = pd.DataFrame(data)
    out = create_basic_features(df)
    assert "sma_5" in out.columns
    assert "sma_20" in out.columns
    assert "atr_14" in out.columns
    assert "ret" in out.columns
    assert "vol_10" in out.columns
    # Basic sanity checks
    assert out["sma_5"].iloc[-1] > 0
    assert out["vol_10"].iloc[-1] >= 0
