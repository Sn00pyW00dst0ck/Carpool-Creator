"""Module providing main Carpool-Creator functionality."""

# pylint: disable=C0413, E0401
import sys
import argparse
import pandas as pd
# pylint: enable=C0413, E0401

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

def main(argv=None):
    """Function providing main Carpool-Creator functionality"""
    args = parse_arguments(argv)
    _, driver_data, rider_data = read_carpool_data(args.src_file[0])
    matches = match_riders_randomly(driver_data, rider_data)
    matches.to_csv(args.out_file[0])
    return 0

@function_with_logging
def parse_arguments(args):
    """Function providing argument string parsing for Carpool-Creator"""
    parser = argparse.ArgumentParser(
        prog='CarpoolCreator',
        description='parse file name and script flags')
    parser.add_argument(
        'src_file',
        nargs=1,
        help="CSV source file for the carpool data")
    parser.add_argument(
        'out_file',
        nargs=1,
        help="CSV output file to store the carpool matchmaking")
    args = parser.parse_args(args)
    return args

@function_with_logging
def read_carpool_data(csv_file):
    """A function which uses pandas to read CSV data from the specified src_file"""
    headers = pd.read_csv(csv_file, nrows=0).columns.tolist()
    driver_data = pd.read_csv(csv_file, usecols=['Driver', 'Capacity'])
    driver_data.dropna(inplace=True)
    rider_data = pd.read_csv(csv_file, usecols=['Rider', 'Rider Address'])
    rider_data.dropna(inplace=True, how='all')
    return headers, driver_data, rider_data

@function_with_logging
def match_riders_randomly(driver_data: pd.DataFrame, rider_data: pd.DataFrame):
    """A function which randomly matches drivers and riders"""
    maximum_riders_allowed: int = (int)(driver_data['Capacity'].sum(numeric_only=True))
    if maximum_riders_allowed < len(rider_data['Rider'].tolist()):
        print("CANNOT MATCH ALL RIDERS TO A DRIVER")
        sys.exit(-1)

    # Initialize variables for
    riders_to_match = rider_data.sample(frac = 1).set_index('Rider')
    matches = dict.fromkeys(driver_data['Driver'].tolist())
    for i in driver_data.index:
        matches[driver_data['Driver'][i]] = []

    # While there are riders, give each driver a random rider    
    while not riders_to_match.empty:
        for i in driver_data.index:
            try:
                if len(matches[driver_data['Driver'][i]]) < driver_data['Capacity'][i]:
                    rider_to_add = riders_to_match.head(1)
                    pretty_output = "Rider: " + rider_to_add.index[0] + " - Address: " + rider_to_add['Rider Address'][0]
                    matches[driver_data['Driver'][i]].append(pretty_output)
                    riders_to_match = riders_to_match.tail(-1)
                else:
                    matches[driver_data['Driver'][i]].append('')
            except IndexError:
                matches[driver_data['Driver'][i]].append('')

    return pd.DataFrame(matches)

@function_with_logging
def match_riders_with_google(driver_data, riders):
    """A function which attempts to match drivers to riders using the google maps API"""

    # Initialize the matches output
    matches = dict.fromkeys(driver_data['Driver'].tolist())
    for i in driver_data.index:
        matches[driver_data['Driver'][i]] = []

    

    return pd.DataFrame(matches)




if __name__ == '__main__':
    main(sys.argv[1:])
