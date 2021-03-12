from pretreatment import *
from cluster import *

# import database
database_name = 'descriptors_last.db'

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
print(f'Columns deleted for meteo sub dataset: {columns_deleted(columns_meteo, columns_remained_meteo)}')
print(f'Columns deleted for meteo sub dataset: {columns_deleted(columns_operation, columns_remained_operation)}')

# aggregate data on airline level
df_airlines = to_airlines(df, columns_remained)
df_airlines_meteo = to_airlines(df_meteo, columns_remained_meteo)
df_airlines_operation = to_airlines(df_operation, columns_remained_operation)

# conduct clustering
groups_cah = cah(df_airlines)
groups_cah_meteo = cah(df_airlines_meteo)
groups_cah_operation = cah(df_airlines_operation)


