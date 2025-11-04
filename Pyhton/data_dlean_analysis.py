import pandas as pd

#import and view dataset
df = pd.read_csv("data/raw/airbnb_london_listing.csv")

(df.info())
(df.head())

# we can see that originaly we had 53904 observation and 73 variables, 


########################################################
#lets start filtering the observations and the variables

df['market'].value_counts()

#drop everything but london

df = df.loc[df['market'] == 'London']


#successfully droped everything (checked by: "df['market'].value_counts()"
# now our new number of obs. 52359 )

####################################################
# we have too many varaibles still, let's drop them:
####################################################
# we are using a list in order to drop the unneccesarry variables, 
# 1. we create the list of neccessary variables only
# 2. we drop the rest based on the list 

cols_to_keep = ['id', 'host_id', 'host_response_rate',
                'host_is_superhost', 'host_has_profile_pic', 
                'host_identity_verified', 'is_location_exact',
                'property_type', 'room_type',
                'accommodates', 'bathrooms',  'bedrooms',
                'beds', 'bed_type', 'price',
                'extra_people', 'minimum_nights',
                'instant_bookable',
                'cancellation_policy', 'review_scores_location',
                'review_scores_value', 'number_of_reviews']

df = df[cols_to_keep]

#check: df.head()

########################################################
# before droping the rest of the unneccesary observations 
# let's fix the data quality errors
# as there are many variables, let's use loops and lists

binary_vars = ['host_is_superhost', 'host_has_profile_pic','host_identity_verified', 'is_location_exact', 'instant_bookable']

for var in binary_vars:
    df[var] = df[var].map({'t': True, 'f': False})
    df[var] = df[var].astype(bool)

#check with: df.dtypes
############### interesting issue, and solution ###########
#we can see that e.g. superhost is still an onject let examine this 
# with df['host_is_superhost'].value_counts() 
# we can see that there are no missing values so the issue can be something else let's try to simply modify the datatype
#df['host_is_superhost'] = df['host_is_superhost'].astype(bool)
#no errors let's check: df.dtypes, it showes that data type is bool now, let's fix the original loop
#######################################

#response rate:

df['host_response_rate'] = df['host_response_rate'].str.replace('%', '', regex=False)
df['host_response_rate'] = pd.to_numeric(df['host_response_rate'], errors='coerce') / 100

# changing prices

price_rel_vars = ['price', 'extra_people']

for var in price_rel_vars:
    df[var] = df[var].str.replace('[\$,]', '', regex=True)
    df[var] = pd.to_numeric(df[var], errors='coerce')

### now let's drop the outliers #####


df = df[df['price'] < 1000]
df = df[df['host_response_rate'] > 0]

#check how many observations do we have now (df.shape()): 38510

### now drop all missing observations from the critical variables ###

df.dropna(subset=['host_response_rate', 'bathrooms', 'bedrooms', 'beds', 
                  'review_scores_location', 'review_scores_value'], inplace=True)

# now we have 29401 observations and 22 variables (df.shape())

# save clean dataset:

df.to_csv("data/clean/airbnb_clean.csv", index=False)


####################### data analitics ##############################################

import numpy as np
import matplotlib.pyplot as plt

#let's create a few new variables

df['price_per_person'] = df['price'] / df['accommodates']


#host variable index:
#first we make a list of host related variables

host_vars = ['host_response_rate', 'host_is_superhost', 'host_identity_verified']

# create the new variable and assign value 0 to it
df['host_quality_index'] = 0

# standardize the values add add to the created index
for var in host_vars:
    df['host_quality_index'] += (df[var] - df[var].mean()) / df[var].std()

# Divide by the number of variables to get the average
df['host_quality_index'] = df['host_quality_index'] / 3



#descriptive stat: 
print(df.describe())


#groupped statistics:
print(df.groupby('room_type')['price'].agg(['mean', 'std', 'median']))
print(df.groupby('instant_bookable')['price'].agg(['mean', 'std', 'median']))
print(df.groupby('cancellation_policy')['price'].agg(['mean', 'std', 'median']))

# Host characteristics
print(df.groupby('host_is_superhost')['price'].agg(['mean', 'std', 'median']))
print(df.groupby('host_identity_verified')['price'].agg(['mean', 'std', 'median']))
print(df.groupby('host_has_profile_pic')['price'].agg(['mean', 'std', 'median']))


####################### graphs ###################################

#price and price per person

fig, ax = plt.subplots(figsize=(10,6))
ax.hist(df['price'], bins=30, color='blue', edgecolor='black')
ax.set_title("Histogram of Prices")
ax.set_xlabel("Price")
ax.set_ylabel("Count")
fig.tight_layout()
fig.savefig("Python_output/price_histogram.pdf")
plt.show()

# Histogram of price per person
fig, ax = plt.subplots(figsize=(10,6))
ax.hist(df['price_per_person'], bins=30, color='green', edgecolor='black')
ax.set_title("Histogram of Prices per Person")
ax.set_xlabel("Price per Person")
ax.set_ylabel("Count")
fig.tight_layout()
fig.savefig("Python_output/price_per_person_histogram.pdf")
plt.show()

# Bar graph of average price by room type
avg_price = df.groupby('room_type')['price'].mean()
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(avg_price.index, avg_price.values, color='orange', edgecolor='black')
ax.set_title("Average Price by Room Type")
ax.set_xlabel("Room Type")
ax.set_ylabel("Average Price")
fig.tight_layout()
fig.savefig("Python_output/room_bar_plot.pdf")
plt.show()

# Scatter plot of price vs bedrooms
x = df['bedrooms']
y = df['price']
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(x, y, color='blue', alpha=0.5)
ax.set_title("Price vs Number of Bedrooms")
ax.set_xlabel("Bedrooms")
ax.set_ylabel("Price")
fig.tight_layout()
fig.savefig("Python_output/beds_prices_relations.pdf")
plt.show()

# Scatter plot of price and host quality index
x = df['host_quality_index']
y = df['price']
m, b = np.polyfit(x, y, 1)
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(x, y, color='purple', alpha=0.5)
ax.plot(x, m*x + b, color='red')
ax.set_title("Price vs Host Quality Index")
ax.set_xlabel("Host Quality Index")
ax.set_ylabel("Price")
fig.tight_layout()
fig.savefig("Python_output/price_hostquality.pdf")
plt.show()