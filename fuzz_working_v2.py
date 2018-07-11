import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np

df1 = pd.read_excel(open('/Users/michael/Desktop/GE_pipeline/data.xlsx'), sheetname = 0)
df2 = pd.read_excel(open('/Users/michael/Desktop/GE_pipeline/data.xlsx'), sheetname = 1)

#print df1.head()
#print df2.head()

df3 = pd.DataFrame(index=df1.index, columns=df2.index)
#print df3

def lv1_match(master, source, threshold=0):
	for i in df3.index:
	    for j in df3.columns:
	        vi = master.get_value(i, 'Orig')
	        vj = source.get_value(j, 'Changed')
	        df3.set_value(i, j, fuzz.token_sort_ratio(vi, vj))
	return df3
#print(df3)
#threshold = df3.max(1) > 90

#a = pd.Series(np.diag(df3), index=[df3.index, df3.columns])
#print a
a = lv1_match(df1,df2)
b = pd.Series(np.diag(df3), index=[df3.index, df3.columns])
print b

#idxmax = df3.idxmax(1)
#df['PROD_ID'] = np.where(threshold, df2.loc[idxmax, 'PROD_ID'].values, np.nan)
#df['PROD_DESCRIPTION'] = np.where(threshold, df2.loc[idxmax, 'PROD_DESCRIPTION'].values, np.nan)
#df

#REFERENCES
#https://stackoverflow.com/questions/43938672/efficient-string-matching-in-apache-spark
#https://github.com/MrPowers/spark-stringmetric.git
#https://stackoverflow.com/questions/41455093/searching-one-python-dataframe-dictionary-for-fuzzy-matches-in-another-datafra
