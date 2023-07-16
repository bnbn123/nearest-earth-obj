"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    try:
        with open(neo_csv_path, "r") as f:
            reader = csv.DictReader(f)
            # iterate through each row in the csv file
            # and create a NearEarthObject object for each row
            # and add it to the output list
            output = [NearEarthObject(**row) for row in reader]
            return output
    except FileNotFoundError:
        print("File not found")
    finally:
        f.close()


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.

    """
    try:
        with open(cad_json_path, "r") as f:
            # load the json data
            # create index variables for each field
            jsonData = json.load(f)
            destinationIndex = jsonData["fields"].index("des")
            timeIndex = jsonData["fields"].index("cd")
            distanceIndex = jsonData["fields"].index("dist")
            velocityIndex = jsonData["fields"].index("v_rel")
            #
            # lambda function to create a CloseApproach object for each item in the data using created index variables
            # map each item in the data to the lambda function
            # return the list of CloseApproach objects as list of CloseApproach objects
            return list(
                map(
                    lambda item: CloseApproach(
                        designation=item[destinationIndex],
                        time=item[timeIndex],
                        distance=item[distanceIndex],
                        velocity=item[velocityIndex],
                    ),
                    jsonData["data"],
                )
            )
    except FileNotFoundError:
        print("File not found")
    finally:
        f.close()
