from Library import data_manipulation as da
import pandas as pd
import numpy as np


def test_handle_null():
    """Test impute null."""
    # test data
    df = pd.DataFrame()
    df['C0'] = [0.2601, 0.2358, 0.1429, 0.1259, 0.7526, 0.7341, 0.4546, 0.1426, 0.1490, 0.2500]
    df['C1'] = [0.7154, np.nan, 0.2615, 0.5846, np.nan, 0.8308, 0.4962, np.nan, 0.5340, 0.6731]

    # without group
    expected = pd.DataFrame()
    expected['C0'] = [0.2601, 0.2358, 0.1429, 0.1259, 0.7526, 0.7341, 0.4546, 0.1426, 0.1490, 0.2500]
    expected['C1'] = [0.7154, 0.8308, 0.2615, 0.5846, 0.8308, 0.8308, 0.4962, 0.8308, 0.5340, 0.6731]
    actual = da.handle_null(df, 'C1', 'max')
    assert actual.equals(expected), "Imputation incorrectly without group!"

    # with group
    df['group'] = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    expected['group'] = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    expected['C1'] = [0.7154, 0.7154, 0.2615, 0.5846, 0.8308, 0.8308, 0.4962, 0.6731, 0.5340, 0.6731]
    actual = da.handle_null(df, 'C1', 'max', 'group')
    assert actual.equals(expected), "Imputation incorrectly with group!"


test_handle_null()