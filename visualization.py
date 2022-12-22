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
from sklearn.cluster import DBSCAN, KMeans
from matplotlib import cm
from lifelines import KaplanMeierFitter


def cluster_3D(df, cols, type, number = None, min_sample = 3, eps = 0.5, 
            lab1 = None, lab2 = None, lab3 = None):
    if len(cols) != 3:
        return 'Wrong number of columns'
    if type == 'OPTICS':
        clusters = OPTICS(min_samples = min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_     
    elif type == 'DBSCAN':
        clusters = DBSCAN(eps = eps, min_samples = min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    else:
        if number is None:
            number = 15
            for k in range(1,15):
                clusters = KMeans(n_clusters=k).fit(df[cols])
                if clusters.inertia_ < 50:
                    number = k
                    break
        clusters = KMeans(n_clusters=number)fit(df[cols])
        df['Clusters'] = clusters.labels_

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


def cluster_2D(df, cols, type, number, min_sample = 3, eps = 0.5, 
            lab1 = None, lab2 = None):
    if len(cols) != 2:
        return 'Wrong number of columns'
    if type == 'OPTICS':
        clusters = OPTICS(min_samples = min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_     
    elif type == 'DBSCAN':
        clusters = DBSCAN(eps = eps, min_samples = min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    else:
        if number is None:
            number = 15
            for k in range(1,15):
                clusters = KMeans(n_clusters=k).fit(df[cols])
                if clusters.inertia_ < 50:
                    number = k
                    break
        clusters = KMeans(n_clusters=number)fit(df[cols])
        df['Clusters'] = clusters.labels_

    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(12, 12))
    ax = sns.scatterplot(data=X,x="Prftchange",y="Revchange",hue=X['OPTICS'])

    if not (lab1 is None) and type(lab1) == str:
        ax.set_xlabel(lab1)
    else:
        ax.set_xlabel(col[0])
    if not (lab2 is None) and type(lab2) == str:
        ax.set_ylabel(lab2)
    else:
        ax.set_ylabel(col[1])

    return fig, ax


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


def demo_graph(var: list, input_data: pd.DataFrame, group=None):
    """
    Show the counts of categorical characteristic variables in each group and combine with a summary table.
    Show the boxplots of countinous characteristic variables in each group and combine with a smmary table.

        Parameters
        ----------
        var : list
            List of the characteristic variables. The list can include both categorical and countinous variables,
            the function can automatically detect its type and then use proper plot.
        input_data : pd.DataFrame
            Input dataet name.
        group : names of variables in input_data, optional
            Grouping variables that will produce plottings and summary tables with different colors
            (e.g. treatment group).

        Returns
        -------
        fig, ax : matplotlib.axes.Axes
        The matplotlib axes containing the plot and summary table.

        See Also
        --------
        longitudinal_graph

        Examples
        --------
        >>>
        >>>    # filled with random data

    """
    for col in var:
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        if group is not None:
            dat = input_data.sort_values(by=[group, col], ascending=True)
        else:
            dat = input_data.sort_values(by=[col], ascending=True)
        if np.issubdtype(input_data[col].dtype, np.number):
            sns.boxplot(ax=ax, data=dat, y=col, x=group, orient="v")
            if group is not None:
                summary = dat.groupby([group])[col].describe(percentiles=[0.5]).round(2).transpose()
            else:
                summary = dat[col].describe(percentiles=[0.5]).round(2).reset_index().set_index('index')
        else:
            summary = pd.DataFrame()
            if group is not None:
                sns.countplot(ax=ax, data=dat, x=group, hue=col)
                summary['result'] = dat.groupby([group])[col].value_counts().astype(str) + " (" + \
                                    round(dat.groupby([group])[col].value_counts(normalize=True) * 100, 2)\
                                    .astype(str) + "%)"
                summary = summary.reset_index()
                summary = summary.pivot(index=col, columns=group)
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


def longitudinal_graph(outcome: list, time, group, input_data: pd.DataFrame):

    for col in outcome:
        summary = round(input_data.groupby([group, time])[col].mean().reset_index(), 2)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        sns.lineplot(x=time, y=col, hue=group, data=summary)

        time_group = input_data[time].unique()
        group = input_data[group].unique()
        temp = pd.DataFrame()
        for i in time_group:
            for g1, g2 in itertools.combinations(range(len(group)), 2):
                a = input_data.query(f"{time}=={i} and {group}=='{group[g1]}'")[col].transpose()
                b = input_data.query(f"{time}=={i} and {group}=='{group[g2]}'")[col].transpose()
                p_value = f_test(a, b)
                row = pd.DataFrame([[i, f"p-value: \n {group[g1]} vs {group[g2]}", p_value]],
                                   columns=["Time", "Compare", col])
                temp = pd.concat([temp, row])
        temp = temp.pivot_table(index='Compare', columns="Time")
        print(summary)
        summary = summary.pivot_table(index=group, columns=time)
        summary = pd.concat([summary, temp])
        ax.set(xlabel=None)
        plt.table(cellText=summary.values, rowLabels=summary.index, loc='bottom', bbox=[0, -0.5, 1, 0.4], cellLoc="center")
        plt.subplots_adjust(left=0.2, bottom=0.3)
        plt.title(f"Line plot and summary table for {col.title()}", fontsize=30)
        plt.show()
    return fig, ax


# type 1 is catagorical, 2 is correlation, anything else is both
def relation(df, col1 = None, col2 = None, gtype = 3, path = None, 
            name_chi = 'chiheatmap', name_cor = 'corheatmap'):
    if col1 is None and col2 is None:
        if gtype != 2:
            chi = []
            cols = df.columns
            num_cols = df._get_numeric_data().columns
            cat_cols = list(set(cols) - set(num_cols))
            for i in cat_cols:
                for j in cat_cols:
                    con = pd.crosstab(df[i], df[j]) 
                    c, p, dof, expected = stats.chi2_contingency(con)
                    chi.append(round(p,3)) 
            data = np.array(chi)
            n = int(np.sqrt(len(data)))
            data = data.reshape(n, n)
        
            fig, ax = plt.subplots(figsize=(14, 14))
            p = sns.heatmap(data=data, annot=True, fmt='2g', ax=ax,
                        cmap=cm.YlOrBr, xticklabels=cat_cols, yticklabels=cat_cols)

            if path is not None:
                fig.savefig(f'{path}/{name_chi}.pdf', format='png', bbox_inches='tight')       
            plt.show()
            # pandas.DataFrame(chi, chi_cols, chi_cols)
            return fig, ax
        if gtype != 1:
            plt.figure(figsize = (14, 14))
            p = sns.heatmap(df.corr(), annot = True)
            if path is not None:
                fig.savefig(f'{path}/{name_cor}.pdf', format='png', bbox_inches='tight')       
            plt.show()


def survival_analysis(input_data, time, censor_status, group):
    group_list = input_data[group].unique()
    for i in group_list:
        mask = input_data[group] == i
        fig, ax = plt.subplots(figsize=(15, 10))
        KaplanMeierFitter.fit(input_data[censor_status][mask], input_data[time][mask], label=i)
        KaplanMeierFitter.plot_survival_function(ax=ax, at_risk_counts=True)

    plt.title(f"KM plot of {group}")


def boxplot_grid():
    pass
