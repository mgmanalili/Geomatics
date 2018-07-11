
# coding: utf-8

# In[12]:


from pandas import DataFrame, read_csv
import pandas as pd


# In[13]:


s = r'/Users/michael/Desktop/Geoenabler_SCOPE/test.txt'
d = r'/Users/michael/Desktop/Geoenabler_SCOPE/raw_data.txt'
df_s = pd.read_csv(s, sep = "\t")
df_d = pd.read_csv(d, sep = "\t")
print df_d


# In[17]:


df_d.reset_index(drop=True, inplace=True)
df_s.reset_index(drop=True, inplace=True)
df_d['cum_count'] = df_d.groupby('iso3d').cumcount() + 1
#Drop duplicates keeps the last record
dupli = df_s.drop_duplicates(['iso3_s'],keep='last')
print dupli


# In[15]:


df_d['locid_s'] = df_d['iso3d'].map(dupli.set_index('iso3_s')['loc_id_s'])
print df_d


# In[16]:


df_d.to_csv(r'/Users/michael/Desktop/result.txt')

