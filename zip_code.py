"""
Created on Tue Oct 11 08:20:28 2016

"""
###################################################################################
# 1. A function to find cities near a zip code: 

# Input: a zip code and a radius to search for cities nearby
# Output: city and state within range

import pandas as pd
import math

zip_csv = pd.read_csv('C:\Users\CHENQI1I\desktop\zip_code.csv')



def cal_distance(df ):
    zip_code = raw_input("Enter a zip code: ")
    zipcode = int(zip_code.lstrip("0"))
    radius = int(raw_input("Enter distance in miles: "))

    print df[df['zip']==zipcode]

    lat1 = None
    lat1 = float( df[df['zip']==zipcode]['latitude'])
    lon1 = None
    lon1 = float(df[df['zip']==zipcode]['longitude'])

    # approximate distance in miles:
    #    sqrt(x * x + y * y)
    # where x = 69.1 * (lat2 - lat1)
    #and y = 69.1 * (lon2 - lon1) * cos(lat1/57.3) 
    
    def distance( data ):
        x= 69.1 *(float(data['latitude'])-lat1)
        y= 69.1 * (float(data['longitude']) - lon1) * math.cos(lat1/57.3) 
        miles= None
        miles= math.sqrt( x*x + y*y )
        return miles
    
    # apply this function to zip code data, add a column of distance in miles:
    df["miles"] = df.apply(distance, axis=1) 
    # add a column of whether a zip code is within the radius
    df["in_radius"] =  df["miles"] <= radius  

    # print results
    #　print df.loc[df['in_radius'] == True]
    
    # Unique city and state after removing duplicates:
    city= df.loc[df['in_radius'] == True][['primary_city', 'state','miles']].drop_duplicates()      
        
    # (1) calcualte minimum distance for each city 
    right = city.groupby(['primary_city'])['miles'].min().to_frame()
    # (2) convert index of the results to a column
    right.reset_index(level=0, inplace=True) 
    # (4) a list of unique cities
    left = city[['primary_city', 'state']].drop_duplicates()
    # (5) merge unique city with minimum distance 
    result = pd.merge(left, right, on='primary_city').sort_values('miles')
    return result
# End of function------------------------


nearby_city = cal_distance(zip_csv)
print nearby_city 
###################################################################################
# 
