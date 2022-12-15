import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import textwrap as twp



def cluster_3D():
    pass


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
    return ax, fig


def demo_graph(var=None, by=None, input_data=None):
    for col in var:
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        if np.issubdtype(input_data[col].dtype, np.number):
            dat = input_data.sort_values(by=by, ascending=True)
            sns.boxplot(ax=ax, data=dat, y=col, x=by, orient="v")
            summary = dat.groupby([by])[col].describe(percentiles=[0.5]).round(2).transpose()
        else:
            dat = input_data.sort_values(by=[by, col], ascending=True)
            sns.countplot(ax=ax, data=dat, x=by, hue=col)
            summary = pd.DataFrame()
            summary['result'] = dat.groupby([by])[col].value_counts().astype(str) + " (" + \
                                round(dat.groupby([by])[col].value_counts(normalize=True) * 100, 2).astype(str) + "%)"
            summary = summary.reset_index()
            summary = summary.pivot(index=col, columns=by)
            plt.legend(loc='upper left')
        ax.set(xlabel=None)
        plt.table(cellText=summary.values, rowLabels=[" ".join(i.split()[:3]) for i in summary.index],
                  loc='bottom', bbox=[0, -0.3, 1, 0.2], cellLoc="center")
        plt.subplots_adjust(left=0.2, bottom=0.3)
        plt.ylabel(col, fontsize=16)
        plt.title(f"Plot and summary table for {col.title()}", fontsize=30)
        plt.show()


def relation():
    pass


def time_to_death():
    pass


def survival_analysis():
    pass



