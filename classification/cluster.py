import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from scipy.cluster.hierarchy import ward, fcluster
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA


def to_airlines(df, group_by="median"):
    """
    Group by the dataframe with flights into a dataframe with airlines

    :param df: the original dataframe
    :param group_by: the parameter for group_by function ("median" or "mean")
    :returns: a dataframe with aggregated information on the airline level
    """

    if group_by == "median":
        df_agg = df.groupby(by='airline_cat').median()
    if group_by == "mean":
        df_agg = df.groupby(by='airline_cat').mean()
    df_agg.dropna(inplace=True)

    return df_agg


def scale(df):
    """
    Scale each feature of dataframe by its maximum absolute value

    :param df: the original dataframe
    :returns: the scaled dataframe
    """

    df_scaled = MaxAbsScaler().fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)

    return df_scaled


def cah(df_airlines, threshold=2, plot=True):
    """
    Provide a classification by CAH (hierarchical clustering)

    :param df_airlines: Pandas dataframe on which to compute CAH
    :param threshold: float threshold to split groups in CAH
    :param plot: Boolean whether to plot dendrogram (True by default)
    :returns: list of group labels from CAH
    """

    # scaling
    df_airlines_scaled = scale(df_airlines)

    # compute CAH
    Z = linkage(df_airlines_scaled, method='ward', metric='euclidean')

    # plot CAH
    plt.title('CAH')
    dendrogram(Z, labels=df_airlines_scaled.index, orientation='right', color_threshold=threshold)
    plt.show()

    groups_cah = fcluster(Z, t=threshold, criterion='distance')

    return groups_cah


def pca_plot_clustering(df_airlines, groups):
    """
    Provide a PCA plot for clustering

    :param df_airlines: dataframe on airline level
    :param groups: list of group labels
    """
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(scale(df_airlines))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=groups)
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')


def group_descriptors(df_airlines, groups):
    """
    Provide descriptor information on group level

    :param df_airlines: dataframe on airline level
    :param groups: list of group labels
    :returns: dataframe sorted by feature importance on group level
    """

    df_airlines['group'] = groups
    df_airlines_scaled = scale(df_airlines)
    df_airlines_scaled['group'] = groups
    feature_importance = df_airlines_scaled.groupby('group').median().std()

    # sort the result by the importance of features
    columns_sorted = feature_importance.sort_values(ascending=False).index

    return df_airlines.groupby('group').median().loc[:, columns_sorted]


def airlines_group(df_airlines, groups, airlines_decoder):
    """
    Provide a dataframe with airlines and their group

    :param df_airlines: dataframe on airline level
    :param groups: list of group labels
    :param airlines_decoder: a dictionary providing a correspondence between airline name and airline code
    :returns: dataframe containing airline and their affiliation to groups
    """
    idg = np.argsort(groups)
    df1 = pd.DataFrame(df_airlines.index[idg], groups[idg])
    df2 = pd.DataFrame.from_dict(airlines_decoder, orient='index')

    df_airlines_group = pd.merge(df1, df2, how='left', left_on='airline_cat', right_index=True)
    df_airlines_group = df_airlines_group.rename(columns={0: 'airline'}).drop('airline_cat', axis=1)

    return df_airlines_group
