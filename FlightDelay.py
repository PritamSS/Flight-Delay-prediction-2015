#!/usr/bin/env python
# coding: utf-8

# Importing relevant libraries

# In[3]:


import datetime, warnings, scipy 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Importing the main dataset and storing it as 'data'

# In[4]:


data = pd.read_csv("C:/Users/runaj/OneDrive/Desktop/KJSCE Sem 5/PDS/flights.csv")
print(data)


# Import 2 more dataset 

# In[5]:


airport= pd.read_csv("C:/Users/runaj/OneDrive/Desktop/KJSCE Sem 5/PDS/airports.csv")
airline = pd.read_csv("C:/Users/runaj/OneDrive/Desktop/KJSCE Sem 5/PDS/airlines.csv")


# Finding out infromation about the data

# In[6]:


data.info()


# In[7]:


data.shape


# In[8]:


data.describe()


# In[9]:


print(data.columns)


# In[10]:


data.duplicated().sum()


# Checking for NULL values

# In[11]:


print("Missing Values: \n", data.isnull().sum());


# Finding percentages of NULL values for each columns

# In[12]:


total = data.isnull().sum().sort_values(ascending=False)
percent_1 = data.isnull().sum()/data.isnull().count()*100
percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '% missing'])
print(missing_data)


# Drop the columns with more than 70% NULL values

# In[13]:


data1 = data.dropna(subset = ["TAIL_NUMBER",'DEPARTURE_TIME','DEPARTURE_DELAY','TAXI_OUT','WHEELS_OFF','SCHEDULED_TIME',
             'ELAPSED_TIME','AIR_TIME','WHEELS_ON','TAXI_IN','ARRIVAL_TIME','ARRIVAL_DELAY'])


# In[14]:


# Creating Dataset w.r.t different Types of Delays
data11 = data1.dropna(subset = ['AIR_SYSTEM_DELAY','SECURITY_DELAY','AIRLINE_DELAY','LATE_AIRCRAFT_DELAY','WEATHER_DELAY'])
data11 = data11.drop(['YEAR','MONTH','DAY','DAY_OF_WEEK','TAIL_NUMBER','SCHEDULED_DEPARTURE','DEPARTURE_TIME','SCHEDULED_TIME',
                     'SCHEDULED_ARRIVAL','ARRIVAL_TIME','DIVERTED','CANCELLED','CANCELLATION_REASON','FLIGHT_NUMBER','WHEELS_OFF',
                     'WHEELS_ON','AIR_TIME'],axis = 1)


# In[15]:


data1.shape


# In[16]:


data11.isnull().sum()


# In[17]:


print("Missing Values: \n", airport.isnull().sum());


# In[18]:


airport = airport.dropna(subset = ['LATITUDE','LONGITUDE'])


# In[19]:


airport.head()


# In[20]:


airline


# In[21]:


data11.info()


# ### Data Analysis for Flight delays 

# In[22]:


# The other Dataset
Flight_Delays = data11


# In[23]:


# Creating Dataset by removing null values by not focussing fully on different types of Delays
data2 = data1.drop(['CANCELLATION_REASON','AIR_SYSTEM_DELAY','SECURITY_DELAY','AIRLINE_DELAY',
                    'LATE_AIRCRAFT_DELAY','WEATHER_DELAY'],axis = 1)


# In[24]:


data2.isnull().sum()


# The departure time above is not very informative. Coverting it to datetime format so that we get a better idea of the time.

# In[25]:


# Creating a function to change the way of representation of time in the column
def Format_Hourmin(hours):
        if hours == 2400:
            hours = 0
        else:
            hours = "{0:04d}".format(int(hours))
            Hourmin = datetime.time(int(hours[0:2]), int(hours[2:4]))
            return Hourmin


# In[26]:


data2['Actual_Departure'] =data1['DEPARTURE_TIME'].apply(Format_Hourmin)
data2['Actual_Departure']


# Convert Date to Datetime format for better analysis

# In[27]:


# Creating Date in the Datetime format
data2['Date'] = pd.to_datetime(data2[['YEAR','MONTH','DAY']])
data2.Date


# In[28]:


# Applying the function to required variables in the dataset
data2['Actual_Departure'] =data1['DEPARTURE_TIME'].apply(Format_Hourmin)
data2['Scheduled_Arrival'] =data1['SCHEDULED_ARRIVAL'].apply(Format_Hourmin)
data2['Scheduled_Departure'] =data1['SCHEDULED_DEPARTURE'].apply(Format_Hourmin)
data2['Actual_Arrival'] =data1['ARRIVAL_TIME'].apply(Format_Hourmin)


# # Merge all 3 datasets

# All 3 datasets are merged to have an easier approach to handle the relevant data for Flight Delay

# In[29]:


# Merging on AIRLINE and IATA_CODE
data2 = data2.merge(airline, left_on='AIRLINE', right_on='IATA_CODE', how='inner')


# In[30]:


data2 = data2.drop(['AIRLINE_x','IATA_CODE'], axis=1)


# In[31]:


data2 = data2.rename(columns={"AIRLINE_y":"AIRLINE"})


# In[32]:


data2 = data2.merge(airport, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE', how='inner')
data2 = data2.merge(airport, left_on='DESTINATION_AIRPORT', right_on='IATA_CODE', how='inner')


# In[33]:


data2.columns


# Drop the irrelevant columns

# In[34]:


data2 = data2.drop(['LATITUDE_x', 'LONGITUDE_x',
       'STATE_y', 'COUNTRY_y', 'LATITUDE_y', 'LONGITUDE_y','STATE_x', 'COUNTRY_x'], axis=1)


# In[35]:


data2 = data2.rename(columns={'IATA_CODE_x':'Org_Airport_Code','AIRPORT_x':'Org_Airport_Name','CITY_x':'Origin_city',
                             'IATA_CODE_y':'Dest_Airport_Code','AIRPORT_y':'Dest_Airport_Name','CITY_y':'Destination_city'})


# Taking the required data into Account for visualization and the Analysis

# In[38]:


Flights = pd.DataFrame(data2[['AIRLINE','Org_Airport_Name','Origin_city',
                               'Dest_Airport_Name','Destination_city','ORIGIN_AIRPORT',
                               'DESTINATION_AIRPORT','DISTANCE','Actual_Departure','Date',
                               'Scheduled_Departure','DEPARTURE_DELAY','Actual_Arrival','Scheduled_Arrival','ARRIVAL_DELAY',
                              'SCHEDULED_TIME','ELAPSED_TIME','AIR_TIME','TAXI_IN','TAXI_OUT','DIVERTED',]])


# In[39]:



Flights


# In[40]:


axis = plt.subplots(figsize=(10,14))
Name = Flights["AIRLINE"].unique()
size = Flights["AIRLINE"].value_counts()
plt.title('% of flights per Airline company ',fontsize=20)
plt.pie(size,labels=Name,autopct='%5.0f%%')
plt.show()


# In[41]:


plt.figure(figsize=(10, 15))
plt.title('Count of flights from an Airport', fontsize=20)
axis = sns.countplot(x=Flights['Org_Airport_Name'], data = Flights,
              order=Flights['Org_Airport_Name'].value_counts().iloc[:20].index)
axis.set_xticklabels(axis.get_xticklabels(), rotation=90, ha="right")
plt.tight_layout()
plt.show()


# In[42]:


flights_small = Flights[0:100000]
flights_small


# In[43]:


sns.jointplot(data=flights_small, x="DEPARTURE_DELAY", y="ARRIVAL_DELAY")
plt.title('Jointplot between Depature and Arrival Delay', fontsize=20)


# From the plot we infer that both arrival and departure delay are linear in nature. However, In many cases, even though the Departure delay is close to 0, the arrival delay is slightly higher. Thus, we realise there must be other paramters responsible for the delay on the flight

# In[44]:


plt.figure(figsize=(10, 10))
plt.title('How many flights depart from a City', fontsize=20)
axis = sns.countplot(x=Flights['Origin_city'], data = Flights,
              order=Flights['Origin_city'].value_counts().iloc[:20].index)
axis.set_xticklabels(axis.get_xticklabels(), rotation=90, ha="right")
plt.tight_layout()
plt.show()


# The Figure shows that Atlanta has the highest count of flight from origin city 

# In[45]:


axis = plt.subplots(figsize=(10,14))
plt.title('Arrival Delay for diiferent Airlines ', fontsize=20)
sns.despine(bottom=True, left=True)
# Observations with Scatter Plot
sns.stripplot(x="ARRIVAL_DELAY", y="AIRLINE",
              data = Flights, dodge=True, jitter=True
            )
plt.show()


# American Airlines Inc has the highest Arrival Delay.

# In[46]:


# Plot to show the Taxi In and Taxi Out Time
axis = plt.subplots(figsize=(10,14))
sns.set_color_codes("pastel")
sns.set_context("notebook", font_scale=1.5)
axis = sns.barplot(x="TAXI_OUT", y="AIRLINE", data=Flights, color="g")
axis = sns.barplot(x="TAXI_IN", y="AIRLINE", data=Flights, color="r")
axis.set(xlabel="TAXI_TIME (TAXI_OUT: green, TAXI_IN: blue)")


# In[47]:


# Dataframe correlation
del_corr = data2.corr()

# Draw the figure
f, ax = plt.subplots(figsize=(11, 9))

# Draw the heatmap
sns.heatmap(del_corr)


# In[48]:


axis = plt.subplots(figsize=(20,14))
sns.heatmap(Flights.corr(),annot = True)
plt.show()


# ### Results from Correlation Matrix
# Dividing the different correlations into two parts, the positive correlations (higher than 0.6 ) and the less positive correlations (less than 0.6 but higher than 0.2).
# 
# Positive correlations between:
# DEPARTURE_DELAY and
# ARRIVAL_DELAY,
# LATE_AIRCRAFT_DELAY,
# AIRLINE_DELAY
# 
# ARRIVAL_DELAY and
# DEPARTURE_DELAY
# LATE_AIRCRAFT_DELAY
# AIRLINE_DELAY 
# 
# Less positive correlations between:
# ARRIVAL_DELAY and
# AIR_SYSTEM_DELAY,
# WEATHER_DELAY
# 
# DEPARTURE_DELAY and
# AIR_SYSTEM_DELAY,
# WEATHER_DELAY
# 
# TAXI_OUT and
# AIR_SYSTEM_DELAY,
# ELAPSED_TIME
# 
# ### These could be the main features (except the ARRIVAL_DELAY itself) that influence partly or entirely the flight delays. This needs to be measured by a feature selection method.

# ### Very High Correlation Between Arrival Delay and Departure Delay
# It shows that maximum of the Arrival Delays are due to the Departure Delays but some flights has still arrived on time even after departed late from the Origin Airport. Now we need to check why departure Delay is happening in the origin Airport Which may be due to security Delays, Air System Delays etc.

# # Prediction

# In[49]:


Flights.head()


# In[53]:


sns.displot(Flights['AIR_TIME'])
plt.show()


# Airtime is maximum for about 100-150 mins

# In[54]:


# To check the Distribution of Elapsed Time
sns.displot(Flights['ELAPSED_TIME'])
plt.show()


# 

# In[56]:


# To check the Distribution of Taxi IN
sns.distplot(Flights['TAXI_IN'])
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




