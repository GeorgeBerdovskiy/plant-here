#!/usr/bin/env python
# coding: utf-8

# In[1]:


import netCDF4 as nc
import pandas as pd
import boto3
from io import BytesIO
import gzip
import numpy as np


# In[2]:


from botocore.handlers import disable_signing
s3_resource = boto3.resource('s3')
s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)


# In[19]:


def collect_data():
    year = "2020"
    month = "01"
    
    for i in range(1,32):
        day = str(i)
        
        if (i < 10):
            day = "0" + day
        
        date_file=f"2020{month}{day}"
        date_path=f"2020/{month}/{day}"
        
        key=f"rain_rate/{date_path}/NPR.GEO.GHE.v1.S{date_file}0000.nc.gz"
        
        zip_obj = s3_resource.Object(bucket_name="noaa-ghe-pds", key=key)
        buffer = BytesIO(zip_obj.get()["Body"].read())
        
        dataset_new = nc.Dataset('none.nc', 'w')
        
        with gzip.open(buffer, 'rb') as f:
            file_content = f.read()
            dataset_new = nc.Dataset('TEMP', memory=file_content)
            
        rainfall_array = dataset_new['rain']
        
        dataframe = pd.DataFrame(rainfall_array[1333:3466, 4453:6541])
        dataframe.to_csv(f'africa-rainfall/{date_file}.csv')
        
        print(key)


# In[20]:


collect_data()


# In[48]:


# Requested coordinates
lat_requested = -20.775
long_requested = 37.25745


# In[49]:


def read_data():
    month = "01"
    year = "2020"
    
    for i in range(1,2):
        day = str(i)
        
        if (i < 10):
            day = "0" + day
            
        date_file=f"2020{month}{day}"
        path = f"africa-rainfall/{date_file}.csv"
        
        temp_dataframe = pd.read_csv(path)
        retrieve_data(temp_dataframe, lat_requested, long_requested)


# In[86]:


def retrieve_data(df, latitude, longitude):
    # Both are now validated! Next, correct lat. and long. to begin at zero
    lat_corrected = 90 - latitude
    long_corrected = longitude + 180
    
    # Convert coordinates into indexes (reminder - latitude is y, longitude is x)
    # TODO - Look into proper rounding (up/down)
    # .round for indexes
    
    lat_index = int(((4800.0 / 180) * lat_corrected - 1333) // 1) 
    long_index = int(((10020.0 / 360) * long_corrected - 4453) // 1)
    
    print("LAT INDEX = " + str(lat_index))
    print("LONG INDEX = " + str(long_index))
    
    print(df.iloc[lat_index].iloc[long_index])


# In[87]:


read_data()


# In[ ]:




