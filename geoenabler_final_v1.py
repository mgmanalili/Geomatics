#This is was used to assign use case specific id to tableA based on existing tableB.
#Table A should take the last item in tableB-ID and continue the counting based on a specific column name.

# coding: utf-8
from pandas import DataFrame, read_csv
import pandas as pd

s = r'/Users/michael/Desktop/Geoenabler_SCOPE/test.txt'
d = r'/Users/michael/Desktop/Geoenabler_SCOPE/raw_data.txt'
df_s = pd.read_csv(s, sep = "\t")
df_d = pd.read_csv(d, sep = "\t")
print df_d

df_d.reset_index(drop=True, inplace=True)
df_s.reset_index(drop=True, inplace=True)
df_d['cum_count'] = df_d.groupby('iso3d').cumcount() + 1

#Drop duplicates keeps the last record
dupli = df_s.drop_duplicates(['iso3_s'],keep='last')
print dupli

df_d['locid_s'] = df_d['iso3d'].map(dupli.set_index('iso3_s')['loc_id_s'])
print df_d

df_d.to_csv(r'/Users/michael/Desktop/result.txt')
