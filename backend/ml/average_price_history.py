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
