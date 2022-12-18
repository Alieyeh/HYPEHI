import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import scipy.stats
import itertools
from sklearn.cluster import OPTICS, cluster_optics_dbscan
import matplotlib.gridspec as gridspec
from sklearn.cluster import DBSCAN


def cluster_3D(df, cols, type, number, min_sample = 3, eps = 0.5, 
            lab1 = None, lab2 = None, lab3 = None):
    if type == 'OPTICS':
        clusters = OPTICS(min_samples = min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_     
    elif type == 'DBSCAN':
        clusters = DBSCAN(eps = eps, min_samples = min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    else:
        pass  # add to make code run, delete it when you see this
    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    if not (lab1 is None) and type(lab1) == str:
        ax.set_xlabel(lab1)
    else:
        ax.set_xlabel(col[0])
    if not (lab2 is None) and type(lab2) == str:
        ax.set_ylabel(lab2)
    else:
        ax.set_ylabel(col[1])
    if not (lab3 is None) and type(lab3) == str:
        ax.set_zlabel(lab3)
    else:
        ax.set_zlabel(col[2])
    
    for s in df.Clusters.unique():
        ax.scatter(df[col[0]], df[col[1]], df[col[2]],label=s)
    ax.legend(loc='upper left')
    fig = plt.figure(figsize=(10,10))

    return fig, ax


def cluster_2D():
    pass


def graph_3D(df, ax1: str, ax2: str, ax3: str, lab1 = None,
            lab2 = None, lab3 = None):
    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    if not (lab1 is None) and type(lab1) == str:
        ax.set_xlabel(lab1)
    else:
        ax.set_xlabel(ax1)
    if not (lab2 is None) and type(lab2) == str:
        ax.set_ylabel(lab2)
    else:
        ax.set_ylabel(ax2)
    if not (lab3 is None) and type(lab3) == str:
        ax.set_zlabel(lab3)
    else:
        ax.set_zlabel(ax3)
    ax.scatter(df[ax1], df[ax2], df[ax3], color='purple')
    return fig, ax


def f_test(group1, group2):
    """
    Return the p-value given two groups' data.

            Parameters
            ----------
            group1 : series or list
                Containing continuous numbers for F-test from group 1.
            group2 : series or list
                Containing continuous numbers for F-test from group 2.

            Returns
            -------
            p_value : float
                A number round to 3 decimal places.

            Examples
            --------
            >>> a = [0.28, 0.2, 0.26, 0.28, 0.5]
            >>> b = [0.2, 0.23, 0.26, 0.21, 0.23]
            >>> f_test(a, b)
            0.004
    """
    x = np.array(group1)
    y = np.array(group2)
    if np.var(group2, ddof=1) != 0:
        f_value = np.var(group1, ddof=1) / np.var(group2, ddof=1)
        nun = x.size - 1
        dun = y.size - 1
        p_value = round(1 - scipy.stats.f.cdf(f_value, nun, dun), 3)
    else:
        p_value = np.nan
    return p_value


def demo_graph(var: list, input_data: pd.DataFrame, group_by=None):
    """Return a new matrix of given shape and type, without initializing entries.

        Parameters
        ----------
        var : int or tuple of int
            Shape of the empty matrix.
        input_data : data-type, optional
            Desired output data-type.
        group_by : {'C', 'F'}, optional
            Whether to store multi-dimensional data in row-major
            (C-style) or column-major (Fortran-style) order in
            memory.

        Returns
        -------
        ret : ndarray
        An array, or list of arrays, each with ``a.ndim >= 1``.
        Copies are made only if necessary.

        See Also
        --------
        atleast_2d, atleast_3d

        Examples
        --------
        >>>
        >>>    # filled with random data

    """
    for col in var:
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        if group_by is not None:
            dat = input_data.sort_values(by=[group_by, col], ascending=True)
        else:
            dat = input_data.sort_values(by=[col], ascending=True)
        if np.issubdtype(input_data[col].dtype, np.number):
            sns.boxplot(ax=ax, data=dat, y=col, x=group_by, orient="v")
            if group_by is not None:
                summary = dat.groupby([group_by])[col].describe(percentiles=[0.5]).round(2).transpose()
            else:
                summary = dat[col].describe(percentiles=[0.5]).round(2).reset_index().set_index('index')
        else:
            summary = pd.DataFrame()
            if group_by is not None:
                sns.countplot(ax=ax, data=dat, x=group_by, hue=col)
                summary['result'] = dat.groupby([group_by])[col].value_counts().astype(str) + " (" + \
                                    round(dat.groupby([group_by])[col].value_counts(normalize=True) * 100, 2)\
                                    .astype(str) + "%)"
                summary = summary.reset_index()
                summary = summary.pivot(index=col, columns=group_by)
                plt.legend(loc='upper left')
            else:
                sns.countplot(ax=ax, data=dat, x=col, hue=col, dodge=False)
                plt.xticks([], [])
                summary['result'] = dat[col].value_counts().astype(str) + " (" + \
                                    round(dat[col].value_counts(normalize=True) * 100, 2).astype(str) + "%)"
        ax.set(xlabel=None)
        plt.table(cellText=summary.values, rowLabels=[" ".join(i.split()[:3]) for i in summary.index],
                  loc='bottom', bbox=[0, -0.3, 1, 0.2], cellLoc="center")
        plt.subplots_adjust(left=0.2, bottom=0.3)
        plt.ylabel(col, fontsize=16)
        plt.title(f"Plot and summary table for {col.title()}", fontsize=30)
        plt.show()
        return fig, ax
        # what should I return?/ but I have multiple output plots
        #  axis and figure


def longitudinal_graph(outcome: list, time, group_by, input_data=pd.DataFrame):

    for col in outcome:
        summary = round(input_data.groupby([group_by, time])[col].mean().reset_index(), 2)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        sns.lineplot(x=time, y=col, hue=group_by, data=summary)

        time_group = input_data[time].unique()
        group = input_data[group_by].unique()
        temp = pd.DataFrame()
        for i in time_group:
            for g1, g2 in itertools.combinations(range(len(group)), 2):
                a = input_data.query(f"{time}=={i} and {group_by}=='{group[g1]}'")[col].transpose()
                b = input_data.query(f"{time}=={i} and {group_by}=='{group[g2]}'")[col].transpose()
                p_value = f_test(a, b)
                row = pd.DataFrame([[i, f"p-value: \n {group[g1]} vs {group[g2]}", p_value]],
                                   columns=["Time", "Compare", col])
                temp = pd.concat([temp, row])
        temp = temp.pivot_table(index='Compare', columns="Time")
        print(summary)
        summary = summary.pivot_table(index=group_by, columns=time)
        summary = pd.concat([summary, temp])
        ax.set(xlabel=None)
        plt.table(cellText=summary.values, rowLabels=summary.index, loc='bottom', bbox=[0, -0.5, 1, 0.4], cellLoc="center")
        plt.subplots_adjust(left=0.2, bottom=0.3)
        plt.title(f"Line plot and summary table for {col.title()}", fontsize=30)
        plt.show()
    return fig, ax


def relation():
    pass


def time_to_death():
    pass


def survival_analysis():
    pass


def boxplot_grid():
    pass
