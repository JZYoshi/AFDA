import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
from scipy.cluster.hierarchy import ward, fcluster
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import RobustScaler
from xgboost import XGBClassifier

import sys
import os
sys.path.append("../flight phase on dataset")
import db

# Parameters
# The minimal log number to consider the airline into classification
minimal_log = 10

# The multiplicator of feature importance median to set for feature selections
threshold_setting = 0.8

# Threshold for CAH
threshold_CAH = 8 


df = db.db_to_pandas(filename = "../classification/testDB2.db")

# delete the null value for flights without airline information
df.dropna(subset=['airline'], inplace=True)

# delete the surplus information
df.drop(columns=['icao'],inplace=True)

# transform the airline to categorical code and set the flight_id as index
df["airline"] = df["airline"].astype('category')
df["airline_cat"]=df["airline"].cat.codes
df_noairline = df.drop(columns=['airline'])
df_noairline.set_index('flight_id',inplace=True)

# stock the coding in a dictionary
airlines_decoder = dict(enumerate(df["airline"].cat.categories))

columns = df_noairline.columns

filt_10log = df_noairline['airline_cat'].value_counts()>=minimal_log

# stock the airlines to be considered
airline_list_cat = filt_10log[filt_10log.values==True].index

# filter the dataframe
df_filt_10log = df_noairline[df_noairline['airline_cat'].isin(airline_list_cat)]

# seperate the dataframe to input and output
X = df_filt_10log.iloc[:,:-1]
y = df_filt_10log.loc[:,["airline_cat"]]

# seperate the data into train and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

clf = XGBClassifier()

clf.fit(X_train, y_train)
sfm = SelectFromModel(clf, threshold=threshold_setting*np.median(clf.feature_importances_))
sfm.fit(X_train, y_train)

selection = sfm.get_support()
X_columns = columns[:-1]
columns_remained = X_columns[selection]
X_new = sfm.transform(X)

X_new_df = pd.DataFrame(data = X_new, columns = columns_remained)
y.reset_index(inplace = True)

new_df = pd.merge(X_new_df, y, how = 'left', left_index = True, right_on = 'index')
new_df.drop("index", axis = 1, inplace = True)

df_median = new_df.groupby(by = 'airline_cat').median()
df_median.drop("flight_id", axis = 1, inplace=True)
df_median_values = df_median.values
scaler = RobustScaler().fit(df_median_values)
df_median_scaled = scaler.fit_transform(df_median_values)
df_median_scaled = pd.DataFrame(df_median_scaled)
df_median_scaled.dropna(inplace = True)

Z = linkage(df_median_scaled,method='ward',metric='euclidean')
plt.title("CAH")
dendrogram(Z,labels=df_median.index,orientation='right',color_threshold=threshold_CAH)
plt.show()

groupes_cah = fcluster(Z,t=threshold_CAH,criterion='distance')
idg = np.argsort(groupes_cah)
df1 = pd.DataFrame(df_median.index[idg],groupes_cah[idg])
df2 = pd.DataFrame.from_dict(airlines_decoder, orient='index')

print(pd.merge(df1, df2, how = 'left', left_on = 'airline_cat', right_index = True))






