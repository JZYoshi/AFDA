import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MaxAbsScaler
from sklearn.metrics import silhouette_score

def to_airlines(df, columns_remained, group_by="median"):
    """
    Group by the dataframe with flights into a dataframe with airlines, considering only important features

    :param df: the original dataframe
    :param columns_remained: a list of remained columns after feature selection
    :param group_by: the parameter for group_by function ("median" or "mean")
    :returns: a dataframe with aggregated information on the airline level
    """

    if group_by == "median":
        df_agg = df.groupby(by='airline_cat').median()
    if group_by == "mean":
        df_agg = df.groupby(by='airline_cat').mean()
    df_agg.dropna(inplace=True)

    return df_agg[columns_remained]


def scale(df):
    """
    Scale each feature of dataframe by its maximum absolute value

    :param df: the original dataframe
    :returns: the scaled dataframe
    """

    df_scaled = MaxAbsScaler().fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    df_scaled.set_index(df.index, inplace=True)

    return df_scaled


def cah(df_airlines, fig_title, output_filename, threshold=2, plot=True):
    """
    Provide a classification by CAH (hierarchical clustering)

    :param df_airlines: Pandas dataframe on which to compute CAH
    :param fig_title: title of the plotted figure
    :param output_filename: path-like string that indicates the place to output the figure as well as its name
    :param threshold: float threshold to split groups in CAH
    :param plot: Boolean whether to plot dendrogram (True by default)
    :returns: list of group labels from CAH
    """

    # scaling
    df_airlines_scaled = scale(df_airlines)

    # compute CAH
    Z = linkage(df_airlines_scaled, method='ward', metric='euclidean')

    # plot CAH
    if plot:
        fig = plt.figure()
        plt.title(fig_title)
        dendrogram(Z, labels=df_airlines_scaled.index, orientation='right', color_threshold=threshold)
        maxsize = 11
        m = 0.2 # inch margin
        s = maxsize/plt.gcf().dpi*len(df_airlines_scaled.index)+2*m
        plt.gcf().set_size_inches(plt.gcf().get_size_inches()[0], s)
        plt.savefig(output_filename, format=output_filename.split(".")[-1])

    groups_cah = fcluster(Z, t=threshold, criterion='distance')

    return groups_cah


def pca_plot_clustering(df_airlines, groups, fig_title, output_filename):
    """
    Provide a PCA plot for clustering

    :param df_airlines: dataframe on airline level
    :param groups: list of group labels
    :param fig_title: title of the plotted figure
    :param output_filename: path-like string that indicates the place to output the figure as well as its name
    """
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(scale(df_airlines))
    fig = plt.figure()
    plt.title(fig_title)
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=groups)
    plt.colorbar()
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.savefig(output_filename, format=output_filename.split(".")[-1])


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
    df_airlines_group = df_airlines_group.rename(columns={0: 'airline'})
    # .drop('airline_cat', axis=1)

    return df_airlines_group


def optimal_group_numbers(df_airlines, min=2, max=15, plot=False):
    """
    Provide recommended numbers of group by K-means algorithm

    :param df_airlines: dataframe on airline level
    :param min: minimum groups to be divided
    :param max: maximum groups to be divided
    :param plot: whether to provide silhouette diagram based on K-means algorithm
    :returns: an optimal numbers of group
    """
    silhouettes = []
    df_airlines_scaled = scale(df_airlines)
    for k in range(min, max):
        kmeans = KMeans(n_clusters=k).fit(df_airlines_scaled)
        silhouettes.append(silhouette_score(df_airlines_scaled, kmeans.labels_))
    if plot:
        plt.title('Silhouette')
        plt.plot(range(min, max), silhouettes)
        plt.show()

    optimal_nbs = np.argmax(silhouettes) + min

    return optimal_nbs
