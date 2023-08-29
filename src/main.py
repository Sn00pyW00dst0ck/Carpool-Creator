"""Module providing main Carpool-Creator functionality."""

# pylint: disable=C0413, E0401
import sys
import argparse
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderQueryError
from geopy.adapters import AdapterHTTPError

from geopy.extra.rate_limiter import RateLimiter

# pylint: enable=C0413, E0401

# Custom exception for geocoding errors
class CustomGeocodingError(Exception):
    """Custom Geocoding Exception Type"""

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
    try:
        matches = match_riders_from_addresses(driver_data, rider_data)
    except: # pylint: disable=bare-except
        matches=match_riders_randomly(driver_data, rider_data)
    matches.to_csv(args.out_file[0])
    return 0


@function_with_logging
def parse_arguments(args):
    """Function providing argument string parsing for Carpool-Creator"""
    parser = argparse.ArgumentParser(
        prog="CarpoolCreator", description="parse file name and script flags"
    )
    parser.add_argument(
        "src_file", nargs=1, help="CSV source file for the carpool data"
    )
    parser.add_argument(
        "out_file", nargs=1, help="CSV output file to store the carpool matchmaking"
    )
    args = parser.parse_args(args)
    return args


@function_with_logging
def read_carpool_data(csv_file):
    """A function which uses pandas to read CSV data from the specified src_file"""
    headers = pd.read_csv(csv_file, nrows=0).columns.tolist()
    driver_data = pd.read_csv(csv_file, usecols=["Driver", "Capacity"])
    driver_data.dropna(inplace=True)
    rider_data = pd.read_csv(csv_file, usecols=["Rider", "Rider Address"])
    rider_data.dropna(inplace=True, how="all")
    return headers, driver_data, rider_data


@function_with_logging
def match_riders_randomly(driver_data: pd.DataFrame, rider_data: pd.DataFrame):
    """A function which randomly matches drivers and riders"""
    maximum_riders_allowed: int = (int)(driver_data["Capacity"].sum(numeric_only=True))
    if maximum_riders_allowed < len(rider_data["Rider"].tolist()):
        print("CANNOT MATCH ALL RIDERS TO A DRIVER")
        sys.exit(-1)

    # Initialize variables for matching
    riders_to_match = rider_data.sample(frac=1).set_index("Rider")
    matches = dict.fromkeys(driver_data["Driver"].tolist())
    for i in driver_data.index:
        matches[driver_data["Driver"][i]] = []

    # While there are riders, give each driver a random rider
    while not riders_to_match.empty:
        for i in driver_data.index:
            try:
                if len(matches[driver_data["Driver"][i]]) < driver_data["Capacity"][i]:
                    rider_to_add = riders_to_match.head(1)
                    pretty_output = (
                        rider_to_add.index[0] + " - " + rider_to_add["Rider Address"][0]
                    )
                    matches[driver_data["Driver"][i]].append(pretty_output)
                    riders_to_match = riders_to_match.tail(-1)
                else:
                    matches[driver_data["Driver"][i]].append("")
            except IndexError:
                matches[driver_data["Driver"][i]].append("")

    return pd.DataFrame(matches)


@function_with_logging
def match_riders_from_addresses(driver_data, rider_data):
    """A function which randomly matches drivers and riders"""
    maximum_riders_allowed: int = (int)(driver_data["Capacity"].sum(numeric_only=True))
    if maximum_riders_allowed < len(rider_data["Rider"].tolist()):
        print("CANNOT MATCH ALL RIDERS TO A DRIVER")
        sys.exit(-1)

    geocode = RateLimiter(custom_geocode, min_delay_seconds=1)

    # Use geocode to get lat lon from addresses and construct a distance matrix from that
    try:
        rider_data["Location"] = rider_data["Rider Address"].apply(geocode)
    except GeocoderQueryError as err:
        raise GeocoderQueryError("Could Not Geocode All Addresses.") from err

    rider_data["Rider Address"].replace(np.nan, "No Address Provided", inplace=True)
    locations = pd.DataFrame(
        # Read lat lon from locations we geocoded into a locations matrix
        rider_data["Location"].apply(
            lambda x: [
                x.latitude if hasattr(x,'latitude') and (x.latitude is not None) else None,
                x.longitude if hasattr(x,'longitude') and (x.longitude is not None) else None
            ]
        ).values.tolist(),
        columns=["Lat", "Lon"],
        index=rider_data["Rider"] + " - " + rider_data["Rider Address"]
    )
    distances = pd.DataFrame(
        distance_matrix(locations.values, locations.values),
        index=locations.index,
        columns=locations.index,
    )
    print(locations)

    # Create Matches From Distance Matrix
    drivers_max_capacity = driver_data["Capacity"].max()
    matches = dict.fromkeys(driver_data["Driver"].tolist())
    for i in driver_data.index:
        matches[driver_data["Driver"][i]] = []
        try:
            distances, closest_locations = find_closest_x_locations(
                distances, driver_data["Capacity"][i]
            )
            matches[driver_data["Driver"][i]] = closest_locations
        except: # pylint: disable=bare-except
            pass
        # Add blanks to allow making the DataFrame for output
        while len(matches[driver_data["Driver"][i]]) < drivers_max_capacity:
            matches[driver_data["Driver"][i]].append("")

    return pd.DataFrame(matches)


def find_closest_x_locations(dist_matrix: pd.DataFrame, x: int): # pylint: disable=invalid-name
    """Helper function that finds the x closest locations in the distance matrix"""
    closest_locations = set()  # Use a set to ensure uniqueness of locations

    while len(closest_locations) < x:
        min_distance = dist_matrix.values.min()
        min_i, min_j = np.where(dist_matrix.values == min_distance)
        min_i, min_j = min_i[0], min_j[0]

        closest_locations.add(dist_matrix.index[min_i])

        # Exclude the rows and columns for min_i and min_j to find the next closest pair
        dist_matrix = reduce_matrix(dist_matrix, min_i)

    return dist_matrix, list(closest_locations)

def reduce_matrix(matrix, i):
    """Helper function to reduce the distance matrix"""
    # Remove row i and column i
    matrix = matrix.drop([matrix.index[i]]).drop(columns=[matrix.columns[i]])
    return matrix

def custom_geocode(address):
    """
    Custom geocode function that will raise a custom error 
    for proper try catching when addresses are invalid
    """
    geolocator = Nominatim(user_agent="my_request")
    try:
        # Geocode the address
        location = geolocator.geocode(address)
        if location is None:
            raise CustomGeocodingError("Geocoding failed for address: " + address)
        return location
    except Exception as err:
        raise CustomGeocodingError("Geocoding failed for address: " + address) from err

if __name__ == "__main__":
    main(sys.argv[1:])
