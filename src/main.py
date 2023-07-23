"""Module providing main Carpool-Creator functionality."""

import sys
import argparse
import random
import pandas as pd

def function_with_logging(func):
    """A function which provides basic start, end, and error logs useful for debugging."""
    def decorated_func(*args, **kwargs):
        name = func.__name__
        print("Starting function: ", name)
        try:
            result = func(*args, **kwargs)
            print("Finished function: ", name)
        except:
            print("Error in function: ", name)
            raise
        return result
    return decorated_func

def main():
    """Function providing main Carpool-Creator functionality"""
    args = parse_arguments(sys.argv[1:])
    _, driver_data, riders = read_carpool_data(args.src_file[0])
    matches = match_riders_randomly(driver_data, riders)
    matches.to_csv(args.out_file[0])
    return 0

@function_with_logging
def parse_arguments(args):
    """A function which parses a list of argument strings for the ones necessary for Carpool-Creator"""
    parser = argparse.ArgumentParser(prog='CarpoolCreator', description='parse file name and script flags')
    parser.add_argument('src_file', nargs=1, help="CSV source file path for the carpool data")
    parser.add_argument('out_file', nargs=1, help="CSV output file path to store the carpool matchmaking")
    args = parser.parse_args(args)
    return args

@function_with_logging
def read_carpool_data(csv_file):
    """A function which uses pandas to read CSV data from the specified src_file"""
    headers = pd.read_csv(csv_file, nrows=0).columns.tolist()
    driver_data = pd.read_csv(csv_file, usecols=['Driver', 'Capacity'])
    driver_data.dropna(inplace=True)
    riders = pd.read_csv(csv_file, usecols=['Riders'])
    riders.dropna(inplace=True)
    riders = riders['Riders'].tolist()
    return headers, driver_data, riders

@function_with_logging
def match_riders_randomly(driver_data, riders):
    """A function which randomly matches drivers and riders"""
    maximum_riders_allowed: int = (int)(driver_data['Capacity'].sum(numeric_only=True))
    if (maximum_riders_allowed < len(riders)):
        print("CANNOT MATCH ALL RIDERS TO A DRIVER")
        exit(-1)

    # Initialize variables for
    riders_to_match = riders
    matches =  dict.fromkeys(driver_data['Driver'].tolist())
    for i in driver_data.index:
        matches[driver_data['Driver'][i]] = list()

    # While there are riders, give each driver a random rider
    while riders_to_match:
        for i in driver_data.index:
            try:
                if len(matches[driver_data['Driver'][i]]) < driver_data['Capacity'][i]:
                    rider_to_add = riders_to_match.pop(random.randint(0, len(riders_to_match)-1))
                    matches[driver_data['Driver'][i]].append(rider_to_add)
                else:
                    matches[driver_data['Driver'][i]].append('')
            except RuntimeError:
                matches[driver_data['Driver'][i]].append('')

    return pd.DataFrame(matches)

if __name__ == '__main__':
    main()
