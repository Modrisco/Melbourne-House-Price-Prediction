def get_average_price_history(suburb_name):
    import pandas as pd
    import numpy as np
    DF = pd.read_csv('Average Price History.csv')
    year=0
    average_price=0.0
    year_list=[]
    average_price_list=[]

    for index,row in DF.iterrows():
        year=int(row[0])
        year_list.append(year)
        average_price=row[suburb_name]
        average_price_list.append(average_price)

    return year_list,average_price_list


if __name__ == "__main__":
    suburb_name="Abbotsford"
    year_list,average_price_list = get_average_price_history(suburb_name)
    print(f"\nPrice history in {suburb_name}:")
    for i in range(len(year_list)):
        print(f"In year {year_list[i]}, the average price in {suburb_name} is ${average_price_list[i]} per square feet.")
