# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 08:20:28 2016
Input: a zip code and a radius to search for cities nearby
Output: city and state within range

@author: CHENQI1I
"""

import pandas as pd
# import numpy as np
import math

# data cleaning: keep on type= standard, remove type= military or PO box or unique; delete country ^= US; 
# delete zip codes with latitude =0 ;

# import zip code CSV file 
df = pd.read_csv('C:\Users\CHENQI1I\desktop\zip_code.csv')
dfa = df.copy()
# look at the data
# df.head()

# input city, state and radius:  
city = raw_input("Enter a city: ")
state = raw_input("Enter a state: ")
radius = int(raw_input("Enter distance in miles: "))

center_city= None
center_city =  df[df['primary_city']== city][df['state']== state]
# print center_city
# select distinct sets of longitude and latitude: 
locations = center_city[['longitude', 'latitude']].drop_duplicates()
# take latitude and longitude of that zip code


#----------------------------------------------------------------------------
# a function to calcluate approximate distance in miles:
#    sqrt(x * x + y * y),  
# where x = 69.1 * (lat2 - lat1) and y = 69.1 * (lon2 - lon1) * cos(lat1/57.3) 
   

#----------------------------------------------------------------------------
# define a function to calculated nearby city for each set of (lon, lat)
def cal_distance( loca ):
    city_list = pd.DataFrame() 
    k=0
    for k in range(len(loca)):
        lat1 = loca.iloc[k]['latitude']
        lon1 = loca.iloc[k]['longitude']        
        # print "k=", k ,   loca.iloc[k] ,"\n"     
        k +=1        
        dfa = df.copy()  
        # apply this function to zip code data, add a column of distance in miles:
        def distance( data ):

            x= 69.1 *(float(data['latitude'])-lat1)
            y= 69.1 * (float(data['longitude']) - lon1) * math.cos(lat1/57.3) 
            miles= None
            miles= math.sqrt( x*x + y*y )
            return miles

        dfa["miles"] = dfa.apply(distance, axis=1) 
        # add a column of whether a zip code is within the radius
        dfa["in_radius"] =  dfa["miles"] <= radius  
    
        # Unique city and state after removing duplicates:

        new_city= dfa.loc[dfa['in_radius'] == True][['primary_city', 'state','miles']].\
            drop_duplicates()       
        # print new_city
        # remove duplicate in results:        
        city_list = pd.concat([city_list, new_city]).drop_duplicates()
        
 
        
    # (1) calcualte minimum distance for each city 
    right = city_list.groupby(['primary_city'])['miles'].min().to_frame()
    # (2) convert index of the results to a column
    right.reset_index(level=0, inplace=True) 
    # (4) a list of unique cities
    left = city_list[['primary_city', 'state']].drop_duplicates()
    # (5) merge unique city with minimum distance 
    result = pd.merge(left, right, on='primary_city').sort_values('miles')
    print result
    return result
 
#--------------------------------- End of function-----------------------
result = cal_distance(locations )  
