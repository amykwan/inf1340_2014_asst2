""" Computer-based immigration office for Kanadia """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v5"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains all people's passport information (e.g.,
        number, name, birth date, etc.)
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    #open the json files and load information into dictionaries and lists
    with open(countries_file) as json_countries_data, \
            open(watchlist_file) as json_watchlist_data, \
            open(input_file) as json_entries_data:
        countries = json.load(json_countries_data)
        watch_list = json.load(json_watchlist_data)
        entries = json.load(json_entries_data)

    #the variable "decisions" is the final result which this method returns
    decisions = []
    #loop over all the entries in the list that come from input_file
    #form of loop -> access every elements inside a list/tuple of sting in order
    for item in entries:
            #check if customer meets quarantine criteria
            if is_quarantine(item, countries):
                decisions += ["Quarantine"]
            #check if customer meets reject criteria
            elif is_reject(item, countries):
                decisions += ["Reject"]
            #check if customer meets secondary criteria
            elif is_secondary (item, watch_list):
                decisions += ["Secondary"]
            #vistor is permitted to enter the country if he/she passes all the checked criteria
            else:
                decisions += ["Accept"]
    return decisions


def is_quarantine(entry_record, countries_dict):
    from_country = entry_record["from"]["country"].upper()
    via_country = ""
    if "via" in entry_record.keys():
        via_country = entry_record["via"]["country"].upper()

    if from_country != "" and countries_dict[from_country]["medical_advisory"] != "":
        return True
    elif via_country != "" and countries_dict[via_country]["medical_advisory"] != "":
        return True
    else:
        return False


def is_reject(entry_record, country_dict):
    from_country = entry_record["from"]["country"].upper()

    if not is_valid_entry_record(entry_record):
        return True
    elif not from_country in country_dict.keys():
        return True
    elif entry_record["entry_reason"].upper() == "TRANSIT" and \
                    country_dict[from_country]["transit_visa_required"] == "1":
        if not is_valid_visa(entry_record):
            return True
    elif entry_record["entry_reason"].upper() == "VISIT" and \
                    country_dict[from_country]["visitor_visa_required"] == "1":
        if not is_valid_visa(entry_record):
            return True
    else:
        return False


#A function used to check if the person is on the watchlist
def is_secondary(entry_record, watch_list):
    """
    Checks whether a traveller is on the watchlist
    :param entry_record: The name of a JSON formatted file that contains all people's entry record information
    :param watch_list: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :return: Boolean. Returns "True" if they are on the watchlist and "False" if they are not on the watchlist
    """
    for suspect in watch_list:
        if entry_record["first_name"].upper() == suspect["first_name"].upper() and \
           entry_record["last_name"].upper() == suspect["last_name"].upper():
            return True
        elif entry_record["passport"] == suspect["passport"]:
            return True
    return False


#A function used to check if the person has the valid visa to enter
def is_valid_visa(entry_record):
    """
    A function to check if a traveller has a valid visa.
    :param entry_record: The name of a JSON formatted file that contains traveller entry record information
    :param country_dict: A string containing the country name a traveller is from in that traveller's entry
        record as calculated in the "decide' function
    :param transit: A Boolean, either True or False, as calculated in the "decide" function
    :return: A string, either "Reject" or "Accept"
    """
    now = datetime.datetime.now()
    if "visa" not in entry_record.keys():
        return False
    #check if visitor visa required, or if traveller is in transit
    record_visa_date = datetime.date(int(entry_record["visa"]["date"][0:4]),
                                     int(entry_record["visa"]["date"][5:7]),
                                     int(entry_record["visa"]["date"][8:10]))
    earliest_issue_date = datetime.date(now.year-2,now.month,now.day)
    if record_visa_date > earliest_issue_date:
        return True
    else:
        return False


#A function used to check if the person's passport has all the info needed for entrance
def is_valid_entry_record(entry_record):
    """
    A function to check if a traveller's entry record has all the information needed for entrance.
    :param entry_record: The name of a JSON formatted file that contains traveller passport information (e.g.,
        number, name, birth date, etc.)
    :return: Boolean; True if the format is valid, False otherwise
    """
    result = True
    required_info = ["home", "first_name", "last_name", "passport", "entry_reason", "from", "birth_date"]
    for item in required_info:
        if not item in entry_record.keys():
            result = False
    if not "country" in entry_record["home"].keys() or not "city" in entry_record["home"].keys() or \
            not "region" in entry_record["home"].keys():
        result = False
    elif not "country" in entry_record["from"].keys() or not "city" in entry_record["from"].keys() or \
            not "region" in entry_record["from"].keys():
        result = False
    elif not valid_date_format(entry_record["birth_date"]):
        result = False
    elif not valid_passport_format(entry_record["passport"]):
        result = False
    elif "visa" in entry_record.keys():
        if not valid_date_format(entry_record["visa"]["date"]):
            result = False
    return result


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False