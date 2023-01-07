from Library import data_manipulation as da
import pandas as pd
import numpy as np
import random


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
    df['C1'] = [0.7154, np.nan, 0.2615, 0.5846, np.nan, 0.8308, 0.4962, np.nan, 0.5340, 0.6731]
    df['group'] = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    expected['group'] = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    expected['C1'] = [0.7154, 0.5846, 0.2615, 0.5846, 0.6635, 0.8308, 0.4962, 0.60355, 0.5340, 0.6731]
    actual = da.handle_null(df, 'C1', 'median', 'group')
    assert actual.equals(expected), "Imputation incorrectly with group!"


def test_data_selection():
    # test data
    df = pd.DataFrame()
    random.seed(1234)
    df['class'] = random.choices(['A', 'B', 'C', 'D'], k=12)
    df['gender'] = random.choices(['female', 'male'], k=12)
    df['age'] = random.choices(range(10, 20), k=12)
    df['math_score'] = random.choices(range(0, 100), k=12)

    # merge data
    mer = pd.DataFrame()
    mer['class'] = ['A', 'B', 'C', 'D']
    mer['floor'] = [1, 2, 3, 4]

    # expected data
    expected = pd.DataFrame()
    expected['class'] = ['A', 'A', 'A', 'A']
    expected['age'] = [13, 14, 15, 19]
    expected['math'] = [58, 14, 0, 55]
    expected['floor'] = [1, 1, 1, 1]

    # compare
    actual = da.data_selection(df, cond='`class`=="A"', drop_col='gender', sort_by='age', rename={'math_score': 'math'},
                               merge_data=mer, merge_by='class')
    assert np.array_equal(actual.values, expected.values), "Imputation incorrectly with group!"


def test_derive_baseline():
    # test data
    df = pd.DataFrame()
    random.seed(1234)
    df['patient'] = [1001, 1001, 1001, 1001, 1001, 1002, 1002, 1002, 1002]
    df['visit'] = [0, 1, 2, 3, 4, 0, 1, 2, 3]
    df['value'] = random.choices(range(0, 100), k=9)

    # expected data
    expected = df.copy()
    expected['base'] = [96, 96, 96, 96, 96, 58, 58, 58, 58]
    expected['chg'] = [0, -52, -96, -5, -3, 0, 9, -50, 18]

    # compare
    actual = da.derive_baseline(df, base_visit='`visit`==0', by_vars=['patient'], value='value', chg=True, pchg=False)
    assert np.array_equal(actual.values, expected.values), "Baseline value incorrectly with group!"


def test_derive_extreme_flag():
    # test data
    df = pd.DataFrame()
    random.seed(1234)
    df['patient'] = [1001, 1001, 1001, 1001, 1001, 1002, 1002, 1002, 1002]
    df['visit'] = [0, 1, 2, 3, 4, 0, 1, 2, 3]
    df['value'] = random.choices(range(0, 100), k=9)

    # expected data
    expected = df.copy()
    expected['max'] = ["Y", np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, "Y"]

    # compare
    actual = da.derive_extreme_flag(df, by_vars=['patient'], sort_var=['visit'], new_var="max", mode="max",
                                    value_var='value')
    assert actual.equals(expected), "Baseline value incorrectly with group!"


def test_time_to_event():
    pass