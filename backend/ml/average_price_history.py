###############################
# input: 
    # suburb_name (str)

# output:
    # Price history in {surburb_name}:
    # ${price}, {nb_bedrooms} bedroom(s), {nb_bathrooms} bathroom(s), {year}
    # ${average_price} in year {year}
    # Same condition in other surburbs:

    # for example
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

surburb_name=input("Name of the surburb:")

def create_price_history():
    #pd.set_option('display.expand_frame_repr',False)
    print('Creating word_frequency.')
    df = pd.read_csv('Words in Books Data.csv')
    df2=get_frequency(df)
    print('Saving as: word_frequency_books.csv.')
    df2.to_csv('word_frequency_books.csv')
    return df2

def print_dataframe(dataframe,print_column=True,print_rows=True):
    if print_column:
        print(",".join([column for column in dataframe]))
    if print_rows:
        for index,row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))
    return

