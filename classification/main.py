from pretreatment import *
from cluster import *

# import database
database_name = '../data/descriptors.db'

# manually delete the columns not necessary for the analysis
columns_dropped = ['icao', 'icao_airline', 'duration_cruise', 'airport_climb', 'airport_descent']

# create dataframes and airlines_decoder
df, df_meteo, df_operation, airlines_decoder = pretreatment(database_name, columns_dropped)

# feature selection process
columns = df.columns
mad, clf, accuracy, X_train, X_test, y_train, y_test = feature_selection_baseline(df)
columns_remained = feature_selection(mad, clf, accuracy, X_train, X_test, y_train, y_test, columns)

columns_meteo = df_meteo.columns
mad, clf, accuracy, X_train, X_test, y_train, y_test = feature_selection_baseline(df_meteo)
columns_remained_meteo = feature_selection(mad, clf, accuracy, X_train, X_test, y_train, y_test, columns_meteo)

columns_operation = df_operation.columns
mad, clf, accuracy, X_train, X_test, y_train, y_test = feature_selection_baseline(df_operation)
columns_remained_operation = feature_selection(mad, clf, accuracy, X_train, X_test, y_train, y_test, columns_operation)

# display of feature selection results
print(f'Columns deleted for whole dataset: {columns_deleted(columns, columns_remained)}')
print(f'Columns deleted for weather sub dataset: {columns_deleted(columns_meteo, columns_remained_meteo)}')
print(f'Columns deleted for operation sub dataset: {columns_deleted(columns_operation, columns_remained_operation)}')

# aggregate data on airline level
df_airlines = to_airlines(df, columns_remained)
df_airlines_meteo = to_airlines(df_meteo, columns_remained_meteo)
df_airlines_operation = to_airlines(df_operation, columns_remained_operation)

# optimal group numbers deduced from K-means, for reference
print(f'Optimal group numbers for whole dataset: {optimal_group_numbers(df_airlines, plot=True)}')
print(f'Optimal group numbers for meteo dataset: {optimal_group_numbers(df_airlines_meteo, plot=True)}')
print(f'Optimal group numbers for operation dataset: {optimal_group_numbers(df_airlines_operation, plot=True)}')

# conduct clustering
groups_cah = cah(df_airlines, "Hierarchical Clustering", "../webapp/vue/client/src/assets/clustering_res/cah.svg", threshold = 2)
groups_cah_meteo = cah(df_airlines_meteo, "Hierarchical Clustering Weather", "../webapp/vue/client/src/assets/clustering_res/cah_meteo.svg", threshold = 3)
groups_cah_operation = cah(df_airlines_operation, "Hierarchical Clustering ADSB", "../webapp/vue/client/src/assets/clustering_res/cah_operation.svg", threshold = 0.8)

# visualize clusters on PCA
pca_plot_clustering(df_airlines, groups_cah, "PCA", "../webapp/vue/client/src/assets/clustering_res/pca.svg")
pca_plot_clustering(df_airlines_meteo, groups_cah_meteo, "PCA Weather", "../webapp/vue/client/src/assets/clustering_res/pca_meteo.svg")
pca_plot_clustering(df_airlines_operation, groups_cah_operation, "PCA ADSB", "../webapp/vue/client/src/assets/clustering_res/pca_operation.svg")

pca_plot_clustering(df_airlines, groups_cah, "PCA", "../classification_result/pca.svg")
pca_plot_clustering(df_airlines_meteo, groups_cah_meteo, "PCA Weather", "../classification_result/pca_meteo.svg")
pca_plot_clustering(df_airlines_operation, groups_cah_operation, "PCA ADSB", "../classification_result/pca_operation.svg")

# save statistics for clusters (csv)
with open('../classification_result/clustering_stats.csv', 'w') as f:
    f.write(group_descriptors(df_airlines, groups_cah).to_csv())
with open('../classification_result/clustering_stats_meteo.csv', 'w') as f:
    f.write(group_descriptors(df_airlines_meteo, groups_cah_meteo).to_csv())
with open('../classification_result/clustering_stats_operation.csv', 'w') as f:
    f.write(group_descriptors(df_airlines_operation, groups_cah_operation).to_csv())
    
# save statistics for clusters (json)
with open('../webapp/vue/client/src/assets/clustering_res/clustering_stats.json', 'w') as f:
    f.write(group_descriptors(df_airlines, groups_cah).to_json(orient='records'))
with open('../webapp/vue/client/src/assets/clustering_res/clustering_stats_meteo.json', 'w') as f:
    f.write(group_descriptors(df_airlines_meteo, groups_cah_meteo).to_json(orient='records'))
with open('../webapp/vue/client/src/assets/clustering_res/clustering_stats_operation.json', 'w') as f:
    f.write(group_descriptors(df_airlines_operation, groups_cah_operation).to_json(orient='records'))
    
# show final clustering results
classification = airlines_group(df_airlines, groups_cah, airlines_decoder)
classification.reset_index(inplace=True)
classification.columns = ['group', 'airline']

classification_meteo = airlines_group(df_airlines_meteo, groups_cah_meteo, airlines_decoder)
classification_meteo.reset_index(inplace=True)
classification_meteo.columns = ['group_meteo', 'airline']

classification_operation = airlines_group(df_airlines_operation, groups_cah_operation, airlines_decoder)
classification_operation.reset_index(inplace = True)
classification_operation.columns = ['group_operation', 'airline']

# merge three clustering results
classification_3 = classification.merge(classification_meteo, how='left', on='airline').merge(classification_operation, how='left', on='airline')
cols = ["airline", "group", "group_meteo", "group_operation"]

with open('../classification_result/classification.csv','w', encoding='utf-8') as f:
    f.write(classification_3[cols].to_csv())

with open('../webapp/vue/client/src/assets/clustering_res/classification.json','w') as f:
    f.write(classification_3[cols].to_json(orient = "records"))

