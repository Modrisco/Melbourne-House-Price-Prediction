###############################
# input: 
    # suburb_name (str)

# output:
    # Price history in {surburb_name}:
    # ${price}, {nb_bedrooms} bedroom(s), {nb_bathrooms} bathroom(s), {year}
    # ${average_price} in year {year}

    # (for example)
    # Price history in Kensington: 
    # $700,000, 2 bedrooms, 1 bathroom, 2015
    # $900,000, 3 bedrooms, 2 bathrooms, 2016
    # $200 per square feet on average in year 2015
    # $300 per square feet on average in year 2016

    # Same condition in other surburbs:
    # Kingsford $800,000
    # Randwick $700,000
###############################

print("Importing.")
import pandas as pd
import numpy as np
from collections import defaultdict
#import re

# Plan A: dictionary of price history:
# {
# Abbotsford:{2015:avg_price_2015,2016:avg_price_2016},
# Airport West:{2015:avg_price_2015,2016:avg_price_2016}
# }

# Plan B: dictionary of price history:
# {
# "Abbotsford":[2015,avg_price_2015,2016,avg_price_2016],
# "Airport West":[2015,avg_price_2015,2016,avg_price_2016]
# }


# surburb_name = input("Name of the surburb:")
surburb_name = "Abbotsford"

DF = pd.read_csv('Melbourne_housing_FULL_test.csv').dropna(how='any',axis=0)

price_history_dict={"Abbotsford":{2018:0.0}}
# price_history_dict=defaultdict(list)
suburb_list=[]

# sum_price_area_dict
# {
# Abbotsford:{2015:[sum_price,sum_area],2016:[sum_price,sum_area]},
# Airport West:{2015:[sum_price,sum_area],2016:[sum_price,sum_area]}
# }


def get_sum_price_area_dict():
    global suburb_list
    sum_price_area_dict={"Abbotsford":{2018:[0.0,0.0]}}
    # sum_price_area_dict={"Abbotsford":{2016:[10000,50]}}
    # sum_price_area_dict={"suburb":{year:[price_sum,area_sum]}}
    suburb_list=[]
    area_sum=0.0
    price_sum=0.0
    #average_price=0
    year=0
    for index,row in DF.iterrows():
        if row["Suburb"] and row["Price"] and row["Date"] and row["BuildingArea"]:
            suburb=str(row["Suburb"])
            year=int(row["Date"].split("/")[-1])
            if suburb not in suburb_list:
                suburb_list.append(suburb)
                area_sum=0
                price_sum=0
                #average_price=0
                sum_price_area_dict[suburb]={}

            if year not in sum_price_area_dict[suburb]:
                # print(f"suburb = {suburb}, year = {year}")
                sum_price_area_dict[suburb][year]=[0.0,0.0]

            price_sum=sum_price_area_dict[suburb][year][0]
            area_sum=sum_price_area_dict[suburb][year][1]
            price_sum+=float(row["Price"])
            area_sum+=float(row["BuildingArea"])
            sum_price_area_dict[suburb][year][0]=price_sum
            sum_price_area_dict[suburb][year][1]=area_sum
    return sum_price_area_dict

sum_price_area_dict=get_sum_price_area_dict()
# print("\nsuburb_list =",suburb_list)
print("\nsum_price_area_dict:",sum_price_area_dict)

def get_price_history_dict():
    global sum_price_area_dict,price_history_dict
    for suburb in sum_price_area_dict:
        if suburb not in price_history_dict:
            price_history_dict[suburb]={}
        for year in sum_price_area_dict[suburb]:
            if year not in price_history_dict[suburb]:
                price_history_dict[suburb][year]=0.0
            average_price=sum_price_area_dict[suburb][year][0]/sum_price_area_dict[suburb][year][1]
            average_price=round(average_price, 2)
            price_history_dict[suburb][year]=average_price
    return price_history_dict

price_history_dict=get_price_history_dict()
print("\nprice_history_dict =",price_history_dict)

price_history_dict_df = pd.DataFrame(price_history_dict)
price_history_dict_df.to_csv('Average Price History.csv')