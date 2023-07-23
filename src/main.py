import sys
import argparse
import pandas as pd;
import random

def function_with_logging(func):
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
    args = parseArguments(sys.argv[1:])
    headers, driverData, riders = readCarpoolData(args.src_file[0])
    matches = matchRandomRiders(driverData, riders)
    matches.to_csv(args.out_file[0])
    return 0

@function_with_logging
def parseArguments(args):
    # Setup the command line parser
    parser = argparse.ArgumentParser(prog='CarpoolCreator', description='parse file name and script flags')
    parser.add_argument('src_file', nargs=1, help="CSV source file path for the carpool data")
    parser.add_argument('out_file', nargs=1, help="CSV output file path to store the carpool matchmaking")
    args = parser.parse_args(args)
    return args

@function_with_logging
def readCarpoolData(csv_file):
    headers = pd.read_csv(csv_file, nrows=0).columns.tolist()
    driverData = (pd.read_csv(csv_file, usecols=['Driver', 'Capacity']))
    driverData.dropna(inplace=True)
    riders = pd.read_csv(csv_file, usecols=['Riders'])
    riders.dropna(inplace=True)
    riders = riders['Riders'].tolist()
    return headers, driverData, riders

@function_with_logging
def matchRandomRiders(driverData, riders):
    driverCapacity: int = (int)(driverData['Capacity'].sum(numeric_only=True))
    if (driverCapacity < len(riders)):
        print("CANNOT MATCH ALL RIDERS TO A DRIVER")
        exit(-1)

    # Initialize variables for 
    riders_to_match = riders
    matches =  dict.fromkeys(driverData['Driver'].tolist())
    for i in driverData.index:
        matches[driverData['Driver'][i]] = list()

    # While there are riders, give each driver a random rider
    while riders_to_match:
        for i in driverData.index:
            try:
                if len(matches[driverData['Driver'][i]]) < driverData['Capacity'][i]:
                    riderToAdd = riders_to_match.pop(random.randint(0, len(riders_to_match)-1))
                    matches[driverData['Driver'][i]].append(riderToAdd)
                else:
                    matches[driverData['Driver'][i]].append('')
            except:
                matches[driverData['Driver'][i]].append('')         

    return pd.DataFrame(matches)

if __name__ == '__main__':
    main()