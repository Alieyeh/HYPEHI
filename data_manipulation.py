import pandas as pd
import numpy as np
from operator import itemgetter

def handle_null():
    pass


def change_type():
    pass


def data_selection(cond=None, keep_col=None, drop_col=None, sort_by=None, merge_data=None,
                   merge_by=None, merge_keep_col=None, sort_asc=True, rename=None, input_data=None):
    if cond is not None:
        output_data = input_data.query(cond)
    else:
        output_data = input_data

    if keep_col is not None:
        output_data = output_data.loc[:, keep_col]

    if drop_col is not None:
        output_data.drop(drop_col, axis=1, inplace=True)

    if merge_keep_col is not None:
        merge_data = merge_data.loc[:, merge_keep_col]

    if merge_data is not None:
        output_data = output_data.merge(merge_data, on=merge_by, how="left")

    if sort_by is not None:
        output_data.sort_values(by=sort_by, ascending=sort_asc, inplace=True)

    if rename is not None:
        output_data.rename(columns=rename, inplace=True)

    return output_data


def derive_baseline(input_data=None, chg=None, pchg=None, base_visit=None):
    baseline = data_selection(keep_col=["USUBJID", "PARAMCD", "AVISITN", "AVAL"], input_data=input_data,
                              cond=base_visit, rename={"AVAL":"BASE"})

    input_data = data_selection(input_data=input_data, merge_data=baseline, merge_by=["USUBJID", "PARAMCD"])
    if chg:
        input_data["CHG"] = input_data["AVAL"]-input_data["BASE"]
    if pchg:
        input_data["PCHG"] = (input_data["AVAL"]-input_data["BASE"])/input_data["BASE"]

    return input_data


def download():
    pass


def data_bias():
    pass


def numeric_to_categorical(df, col: str, bounds, add = False):
    def group (row, bounds, col):
        bounds = sorted(bounds, key=itemgetter(0))
        for i in bounds:
            if float(row[col]) <= i[0]:
                return i[1]
    if add == True:
        name = col+'_group'
        df[name] = df.apply(lambda row: group(row, bounds, col), axis=1)
        return df
    else:
        df[col] = df.apply(lambda row: group(row, bounds, col), axis=1)
        return df
