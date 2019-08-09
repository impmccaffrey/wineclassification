# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% [markdown]
# ## Exploratory Analysis
# Before I jump into any modeling, I'd like to dig a bit deeper on the data to understand what I am working with. I'll also do some cleanup at this stage.
# 
# From the sample_data_files notebook we saw there were some duplicate descriptions. I'll start by cleaning this up. I'll also want to look through the varieties and check for spelling mistakes. That will ultimately be our label so I believe it's the best use of time to check first for accuracy

#%%
library(tidyverse)
library(stringdist)


#%%
csv_dir = '/Users/patrick/Documents/portfolio/Wine Classification/data/'
csv_file = 'wine_sample.csv'
csv_path = paste0(csv_dir,csv_file)
data = readr::read_csv(csv_path)
dim(data)
data <- data %>%
    distinct(description, .keep_all = TRUE) #remove some of the duplicate descs we saw from the pandas profiler
dim(data) #dimensions after disctinct; looks like we removed about 30 from this initial sample.

#%% [markdown]
# We had 30 rows of duplicates from the sample descriptions. Since the source of the data is from web scraping it's not surprising that there is not perfect data quality. All things considered, this data is really quite nice off the shelf.
# 
# My thinking is to focus on:
# - variety
# - points
# - country
# 
# Seperately, I'll examine description. This I will look at a little differently because of its text/NLP nature.

#%%
head(data, 3)


#%%
summary(data)


#%%
points_plot <- ggplot(data = data, aes(x=points)) + geom_density(kernel="gaussian")
points_plot

#%% [markdown]
# ### 90 Points is uncharacteristically popular
# The density plot for the points given doesn't tell us much we did not already know. What I did learn from this is some of the human tendency for the reviewers to give out 90 points. Given that the center is at 88, it looks they are somewhat generous and round up to 90 points in the case of what would more likely be assigned 89. This is a common human bias I've seen pop a lot, not just in wine reviews!
# *****
#%% [markdown]
# ### Fuzzy String Matching
# I consider it best practice to clean up strings, especially if they're going to be our labels. Here I'm using some heuristics for string distance to check for varietals that should be grouped together.

#%%
###str_distance_param: osa distance between two strings. lower is more closely matched
###see https://cran.r-project.org/web/packages/stringdist/stringdist.pdf for descriptions
###Examples 
#Greco and Merlot = 4
#Arinto and Grillo = 3
#Merlot and Melon = 2
#Insolia and Inzolia = 1
str_distance_param = 1
#This is slow! It checks pairwise
var_str_matrix <- stringdist::stringdistmatrix(data$variety, data$variety, useNames = TRUE, method = 'osa')
str_distances <- melt(var_str_matrix, as.is = TRUE) %>%
    distinct() %>% 
    filter(value > 0 & value <= str_distance_param)


#%%
str_distances

#%% [markdown]
# ### String Grouping Discussion
# A string distance of 1 picks up a lot of varietals that really should be grouped together. These differences are quite explainable; a lot of varieties differ by just one letter based on the country/language of origin.
# 
# I played with the distance param and anything over 1 was grabbing false-positives. I could also run a few passes on thsi using different distance measurements. I think from what I've seen of the data though, I would not pick up too much additional accuracy.
# 
# Next I'll replace the varieties with one in the original dataset.

