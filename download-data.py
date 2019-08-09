# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'notebooks'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# This notebook uses the Kaggle API to fetch our wine data. It downloads the large .csv as a zip, and unzips them in one go.
# 
# The kaggle.json file stores our API keys downloaded from our Kaggle account.

#%%
import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi


#%%
with open('/Users/patrick/.kaggle/kaggle.json') as json_file:  
    api_key = json.load(json_file)
api = KaggleApi(api_key)
api.authenticate()
#Change the working directory to where we want to download our files from Kaggle
os.chdir('/Users/patrick/Documents/portfolio/Wine Classification/data')


#%%
#load our files and unzip them
files = api.dataset_download_files("zynicide/wine-reviews",unzip=True)


