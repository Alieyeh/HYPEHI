import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import textwrap as twp
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


def demo_graph(var=None, group_by=None, input_data=None):
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
        # what should I return?
        #  axis and figure       


def longitudinal_graph(y=None, x=None, by=None, input_data=None):
    for col in x:
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        if np.issubdtype(input_data[col].dtype, np.number):
            sns.boxplot(ax=ax, data=dat, y=col, x=group_by, orient="v")



def relation():
    pass


def time_to_death():
    pass


def survival_analysis():
    pass


def boxplot_grid():
    pass
