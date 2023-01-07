from Library import data_manipulation as da
import pandas as pd
import numpy as np
import random


def test_handle_null():
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


def test_change_type():
    # data
    df = pd.DataFrame()
    df['C0'] = ['1,000', '1', '1 000']
    df['C1'] = [1, 3.01, 50]

    # str to int
    expected = pd.DataFrame()
    expected['C0'] = [1000, 1, 1000]
    expected['C1'] = [1, 3.01, 50]
    actual = da.change_typel(df, 'C0', int)
    assert actual.equals(expected), "Incorrect change from str to int!"

    # float to str
    df['C0'] = ['1,000', '1', '1 000']
    df['C1'] = [1, 3.01, 50]
    expected['C0'] = ['1,000', '1', '1 000']
    expected['C1'] = ["1", "3.01", "50"]
    actual = da.handle_null(df, 'C1', str)
    assert actual.equals(expected), "Incorrect change from float to str!"
    
    # float to int
    df['C0'] = ['1,000', '1', '1 000']
    df['C1'] = [1.9, 3.01, 50.2]
    expected['C0'] = ['1,000', '1', '1 000']
    expected['C1'] = [1, 3, 50]
    actual = da.handle_null(df, 'C1', int)
    assert actual.equals(expected), "Incorrect change from float to int!"


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

    
def test_check_bias():
    # test data
    df = pd.DataFrame()
    df['Visit'] = [True, np.nan, np.nan, np.nan,]
    df['Rest'] = [np.nan, np.nan, '3h', '1h']
    df['Sex'] = ['M', 'M', 'M', 'F']

    # expected data
    expected1 = [['Visit', 3],['Rest', 2]]
    expected2 = [['M', 75], ['F', 25]]
    
    # actual data
    actual1, actual2 =da.check_bias(df, 'Sex', [['M',50],['F',50]])
    
    # compare    
    assert actual1 == expected1, "Null value incorrect!"
    assert actual2 == expected2, "Distribution incorrect!"


def test_numeric_to_categorical():
    # test data
    df = pd.DataFrame()
    df['Height'] = [160, 145, 180, 178]

    # expected data
    expected = pd.DataFrame()
    expected['Height'] = ['medium', 'short', 'tall', 'tall']

    # replace
    actual = dm.numeric_to_categorical(df, 'Height', [[150, 'short'], [170, 'medium'], [190, 'tall']])
    assert actual.equals(expected), "Incorrect replacement!"
    
    # new group
    df['Height'] = [160, 145, 180, 178]
    expected['Height'] = [160, 145, 180, 178]
    expected['Height_group'] = ['medium', 'short', 'tall', 'tall']
    actual = dm.numeric_to_categorical(df, 'Height', [[150, 'short'], [170, 'medium'], [190, 'tall']], True)
    assert actual.equals(expected), "Incorrect new group!"
    
    
def test_time_to_event():
    pass


def test_read():
    pass
