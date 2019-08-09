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
# ## Data Sampling and Initial Impressions
# This notebook is going to merge and sample our .csv files. They are pretty large and we don't want to be perpetually messing around with large files in memory. So I'm going to start with making a couple sample files that will be used when we are testing our code. Once our model is ready to go, we'll run it on the big guys.
# 
# I decide to profile the data at load time, to get a sense of what I'm dealing with.

#%%
import os
import random
import pandas as pd
import pandas_profiling


#%%
os.chdir('/Users/patrick/Documents/portfolio/Wine Classification/data')
os.listdir() #let's see what we're working with


#%%
#Sample 5% of our dataset, or a little under 7,000 rows in this case
#sample function easily adjustable for a direct sample size instead of percentage.
file_nm = 'winemag-data-130k-v2.csv'
num_lines = sum(1 for l in open(file_nm))
sample_frac = .05
sample_size = int(num_lines * .05) #truncate down, to be safe
n = int(num_lines / sample_size) #how many nth rows to sample
n #sanity check this number


#%%
#I don't know if data is ordered, so we need to randomly sample rows
skip_index = random.sample(range(1, num_lines), num_lines - sample_size)
data = pd.read_csv(file_nm, skiprows=skip_index)


#%%
data.to_csv('wine_sample.csv')


#%%
#Just had one column name to fix.
data = data.rename(columns = {'Unnamed: 0': "original_index"
                       })


#%%
#let's take a peak
data.head(5)


#%%
pandas_profiling.ProfileReport(data)

#%% [markdown]
# ## Discussion
# 
# Let's talk briefly about what we're seeing here, a priori to a deeper dive of the data. My initial impression is of the data quality, which is quite good. There are a few apparent duplicates, but they should be quite easy to clean up. I'm not so concerned with most of the missing values. I wasn't expecting the designation (e.g. "reserva") to be especially meaningful.
# 
# On a personal note, I find the summary statistics and histogram of the points *very* interesting, and a little surprising. I did not read beforehand any discussion on the wine magazine point system. But it's very apparent that it ranges from 80 to 100. I'm glad I now know that 93 points represents that 95% percentile of wine points. What's maybe more surprising is that 88 points is the 50th percentile, and the 0th percentile is 80. 

