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

surburb_name = input("Name of the surburb:")
DF = pd.read_csv('Words in Books Data.csv')


def create_price_history():
    #pd.set_option('display.expand_frame_repr',False)
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


print("Importing.")
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
from collections import defaultdict
#import re


def create_word_frequency():
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


def get_invalid_words():
    print("Scanning IDs of invalid words.")
    invalid_word_list=[]
    invalid_word_list.append('6419')
    df = pd.read_csv('Words Mapping.csv')
    invalid_str_list=list(', . ! at in on all any been\
     mr miss mz by with have had but and or this that \
     be am is are was were in on not of the and a an \
     you your i me my mine they them their he him his \
     she her it its to for will would can could as from\
     very so too'.split())
    print('invalid_str_list = ',invalid_str_list)
    for index,row in df.iterrows():
        word=row['Word']
        word_id=row['Word ID']
        if type(word) != str:
            continue
        word=word.strip('_').strip(';').lower()
        if word in invalid_str_list:
            invalid_word_list.append(str(word_id))
    print('invalid_word_list =',invalid_word_list)
    return invalid_word_list


def get_word_mappping_dictionary():
    print("Creating word_mapping_dictionary.")
    df=pd.read_csv('Words Mapping.csv')
    word_mappping_dictionary={}
    for index,row in df.iterrows():
        word=str(row['Word'])
        word_id=str(row['Word ID'])
        word_mappping_dictionary[word_id]=word
    return word_mappping_dictionary


def get_frequency(input_df):
    global num_top
    df=input_df
    #word_set=set()
    books_frequency={}
    invalid_word_list=get_invalid_words()
    print("Calculating the word frequency.")
    for index,row in df.iterrows():
        words_count=defaultdict(int)
        book_id = row['Book ID']
        word_list = row['Words in Book'].split('|')
        num_words = len(word_list)
        for word in word_list:
            if word not in invalid_word_list:
                words_count[word]+=1
        sorted_list=sorted(words_count.items(),key = lambda words_count:words_count[1],reverse=True)
        top_10_words_count=sorted_list[:num_top]     # Displaying the top [ ] lines
        books_frequency[book_id]=top_10_words_count
    df2=pd.DataFrame(books_frequency)
    return df2


def translate(df):
    global word_mappping_dictionary
    translated_df=df
    print("Translating.")
    for index,row in translated_df.iterrows():
        for book_id in range(5000,8000):
            #id=str(book_id)
            word_count=row[book_id]
            #print("word_count =",word_count)
            word_id=word_count[0]
            #print("word_count[0] =",word_count[0],type(word_count[0]))
            #row[book_id][0] = word_mappping_dictionary[word_id]
        '''
        for count in row:
            print("count =",count)
            word_id=count[0]
            print("count[0] =",count[0])
            #row[count][0]=word_mappping_dictionary[word_id]
        '''
    print("Saving as word_frequency_books.csv")
    translated_df.to_csv('translated word_frequency_books.csv')
    return

print("Starting.")
num_top=10
word_mappping_dictionary=get_word_mappping_dictionary()
#print("word_mappping_dictionary = ",word_mappping_dictionary)
data_frame=create_word_frequency()
translate(data_frame)
print('Complete.\n\n')
