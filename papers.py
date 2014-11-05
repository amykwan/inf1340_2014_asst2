""" Computer-based immigration office for Kanadia """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "Prototype"

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
    #Open all the json files and load their information into dictionaries and lists.
    json_countries_data = open(countries_file)
    json_watchlist_data = open(watchlist_file)
    json_entries_data = open(input_file)
    countries = json.load(json_countries_data)    
    watch_list = json.load(json_watchlist_data)
    entries = json.load(json_entries_data)
    
    #the variable "decisions" is the final result which this method returns
    decisions = []
    #loop over all the entries in the list that come from input_file
    #form of loop -> access every elements inside a list/tuple of sting in order
    for item in entries:
        #load the countries' names and simplify the program
        #if the customer is in transit, gather the transit related information
        via_country = ""
        if "via" in item.keys():
            via_country = item["via"]["country"].upper()
        if item["entry_reason"].upper() == "TRANSIT":
            transit = True
        else:
            transit = False
        
        if "from" in item.keys() and "home" in item.keys():
            from_country = item["from"]["country"].upper()
            home_country = item["home"]["country"].upper()

            #Check if the country where the visitor "came from" is medical_advisory
            if from_country != "" and countries[from_country]["medical_advisory"] != "":
                decisions += ["Quarantine"]

            #Check if the country where the visitor "via" is medical_advisory
            elif via_country != "" and countries[via_country]["medical_advisory"] != "":
                decisions += ["Quarantine"]

            #uses the valid_entry_record function created to check if all the required info is in the passport
            elif not valid_entry_record(item):
                decisions += ["Reject"]

            #Check if the from_country is in the country file - not needed?
            #elif not from_country in countries.keys():
            #    decisions += ["Reject"]

            #Use check_watchlist function created to check if the person is on the watchlist
            elif not check_watchlist(item, watch_list):
                decisions += ["Secondary"]

            #check if the person's home country is KAN and is he/she is returning home, accept
            elif home_country.upper() == "KAN" and item["entry_reason"].upper() == "RETURNING":
                decisions += ["Accept"]

            #check if the person's visa or via visa is valid
            elif transit or item["entry_reason"].upper() == "VISIT":
                decisions += [check_visa(item, countries[from_country], transit)]

            #vistor is permitted to enter the country if he/she passes all the checked criteria
            else:
                decisions += ["Accept"]
        else:
            decisions += ["Reject"]
    json_countries_data.close()
    json_watchlist_data.close()
    json_entries_data.close()
    return decisions


#A function used to check if the person is on the watchlist
def check_watchlist(entry_record, watch_list):
    for suspect in watch_list:
        if entry_record["first_name"].upper() == suspect["first_name"].upper() and \
           entry_record["last_name"].upper() == suspect["last_name"].upper():
            return False
        elif entry_record["passport"] == suspect["passport"]:
            return False
    return True


#A function used to check if the person has the valid visa to enter
def check_visa(entry_record, country, transit):
    now = datetime.datetime.now()
    if "visa" not in entry_record.keys():
            return "Reject"
    #check if visitor visa required, or if traveller is in transit
    if country["visitor_visa_required"] == "1" or transit and country["transit_visa_required"] == "1":
        #compute whether the visa time is valid (visa cannot be older than 2 years)
        visa_time_valid = (now.year - int(entry_record["visa"]["date"][2:4])) * 365 + \
                      (now.month - int(entry_record["visa"]["date"][5:7])) * 30 + \
                      (now.day - int(entry_record["visa"]["date"][8:10]))
        if not valid_date_format(entry_record["visa"]["date"]):
            return "Reject"
        elif visa_time_valid > 730:
            return "Reject"
    return "Accept"


#A function used to check if the person's passport has all the info needed for entrance
def valid_entry_record(entry_record):
    valid = True
    required_info = ["home", "first_name", "last_name", "passport", "entry_reason", "from", "birth_date"]
    for item in required_info:
        if not item in entry_record.keys():
            valid = False
    if not "country" in entry_record["home"].keys() or not "city" in entry_record["home"].keys() or \
            not "region" in entry_record["home"].keys():
        valid = False
    elif not "country" in entry_record["from"].keys() or not "city" in entry_record["from"].keys() or \
            not "region" in entry_record["from"].keys():
        valid = False
    elif not valid_date_format(entry_record["birth_date"]):
        valid = False
    return valid_passport_format(entry_record["passport"]) and valid


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