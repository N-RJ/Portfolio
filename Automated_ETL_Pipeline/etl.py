import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime
import import_data
import data_quality
import combined_data


def covid_etl(ipath, opath, stdate = "2020-01-02", enddate="2022-08-22", ctry=["United States of America", "Spain", "Italy", "Germany"]):


    data = import_data.load_df(ipath)
    

    cleaned_dict = data_quality.clean_data(data)


    final_df = combined_data.join_and_aggregate(cleaned_dict, stdate, enddate, ctry)


    final_df.to_csv(opath, index=False)



#_______________________________________________________________________________________________________________________________________


# defining a function to take the date range inputs in a specific format as Python does not have a function for this purpose    
def valid_date(date_str):
    #try block attempts to parse the string into a datatime object without abruptly stopping when an input with a different format is mentioned 
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    #except returns an error when an input of undesired format/type is entered
    except ValueError: 
        raise argparse.ArgumentTypeError(f"Invalid date: '{date_str}'. Expected format: YYYY-MM-DD")



if __name__ == '__main__':
    
    #creating argparse object
    obj = argparse.ArgumentParser()

    #adding argument variables to the object
    obj.add_argument("path", type=str, help="Source path of folder containing CSV data files")
    #os.getcwd() helps dynamically input the path of current directory 
    obj.add_argument("-o", type=str, default=os.path.join(os.getcwd(), "macro_table.csv"), help="Source path of folder to store final CSV data file")
    obj.add_argument("-start", type=valid_date, default="2020-01-02", help="The starting date to consider to build the macrotable")
    obj.add_argument("-end", type=valid_date, default="2022-08-22", help="The ending date to consider to build the macrotable")
    #nargs="+" implies that this argument expects more than one input & all are collected in a list
    obj.add_argument("-countries", nargs="+", type=str, default=["United States of America", "Spain", "Italy", "Germany"], help="Enter countries to include in the macrotable without a comma, seperated by spaces")
 
    # Parse arguments
    args = obj.parse_args()
    
    covid_etl(args.path, args.o, args.start, args.end, args.countries)