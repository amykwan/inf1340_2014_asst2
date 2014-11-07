""" Computer-based immigration office for Kanadia """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v7"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    decides whether a traveller's entry into Kanadia should be accepted
    :param input_file: name of a JSON formatted file that contains all people's passport information (e.g.,
        number, name, birth date, etc.)
    :param watchlist_file: name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: list of strings; possible values of strings are: "Quarantine", "Reject", "Secondary", and "Accept"
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
    #form of loop -> access every elements inside a list/tuple of string in order
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
            #customer is permitted to enter the country if he/she passes all the checked criteria
            else:
                decisions += ["Accept"]
    return decisions


def is_quarantine(entry_record, countries_dict):
    """
    checks whether customer meets condition for quarantine
    :param entry_record: the customer's entry record information
    :param countries_dict: list of countries requiring a visa, and countries with medical advisories
    :return: Boolean; Return True if the record meets quarantine criteria, False otherwise
    """
    #check if from country is flagged for medical advisory
    if "from" in entry_record.keys():
        if "country" in entry_record["from"].keys() :
            from_country = entry_record["from"]["country"].upper()
            if countries_dict[from_country]["medical_advisory"] != "":
                return True
    #check if via country is flagged for medical advisory
    elif "via" in entry_record.keys():
        if "country" in entry_record["via"].keys():
            via_country = entry_record["via"]["country"].upper()
            if countries_dict[via_country]["medical_advisory"] != "":
                return True
    else:
        return False


def is_reject(entry_record, country_dict):
    """
    checks whether customer meets condition for rejection of entry
    :param entry_record: the customer's entry record information
    :param country_dict: list of countries requiring a visa, and countries with medical advisories
    :return: Boolean; True if the record meets the reject criteria, False otherwise
    """
    #check if entry record is incomplete
    if not is_valid_entry_record(entry_record):
        return True
    #check if "from" country is in the country file
    from_country = entry_record["from"]["country"].upper()
    if not from_country in country_dict.keys():
        return True
    #check if transit visa is required, if required, check if the visa is valid
    elif entry_record["entry_reason"].upper() == "TRANSIT" \
            and country_dict[from_country]["transit_visa_required"] == "1":
        if not is_valid_visa(entry_record):
            return True
    #check if visitor visa is required, if required, check if the visa is valid
    elif entry_record["entry_reason"].upper() == "VISIT" \
            and country_dict[from_country]["visitor_visa_required"] == "1":
        if not is_valid_visa(entry_record):
            return True
    else:
        return False


def is_secondary(entry_record, watch_list):
    """
    checks whether customer is on the watchlist and must be sent to secondary
    :param entry_record: the customer's entry record information
    :param watch_list: names of travellers on the watch list
    :return: Boolean; True if the record is on the watchlist, False otherwise
    """
    for suspect in watch_list:
        if entry_record["first_name"].upper() == suspect["first_name"].upper() \
                and entry_record["last_name"].upper() == suspect["last_name"].upper():
            return True
        elif entry_record["passport"] == suspect["passport"]:
            return True
    return False


def is_valid_visa(entry_record):
    """
    checks whether customer has a valid visa to enter
    :param entry_record: the customer's entry record information
    :return: Boolean; False if visa entry not in record or if the visa is older than 2 years, True otherwise
    """
    #establish the current date
    now = datetime.datetime.now()
    #check if customer has a visa
    if "visa" not in entry_record.keys():
        return False
    #convert the visa date from str to datetime format
    record_visa_date = datetime.date(int(entry_record["visa"]["date"][0:4]),
                                     int(entry_record["visa"]["date"][5:7]),
                                     int(entry_record["visa"]["date"][8:10]))
    #compute the earliest acceptable visa date
    earliest_issue_date = datetime.date(now.year-2,now.month,now.day)
    #compare the visa date to check if within 2 years
    if record_visa_date > earliest_issue_date:
        return True
    else:
        return False


def is_valid_entry_record(entry_record):
    """
    checks whether customer's entry record has all the information needed for entrance
    :param entry_record: the customer's entry record information
    :return: Boolean; True if the format is valid, False otherwise
    """
    result = True
    #list of all the required info from the customer's passport
    required_info = ["home", "first_name", "last_name", "passport", "entry_reason", "from", "birth_date"]
    #loop to check every item in the required info list is in the record entry
    for item in required_info:
        if not item in entry_record.keys():
            result = False
    #check if the customer's "home" information is complete
    if not "country" in entry_record["home"].keys() or not "city" in entry_record["home"].keys() \
            or not "region" in entry_record["home"].keys():
        result = False
    #check if the customer's "from" information is complete
    elif not "country" in entry_record["from"].keys() or not "city" in entry_record["from"].keys() \
            or not "region" in entry_record["from"].keys():
        result = False
    #check if customer's birth date format is correct
    elif not valid_date_format(entry_record["birth_date"]):
        result = False
    #check if format of customer's passport is correct
    elif not valid_passport_format(entry_record["passport"]):
        result = False
    #if customer has a visa, check if visa date format is complete
    elif "visa" in entry_record.keys():
        if not valid_date_format(entry_record["visa"]["date"]):
            result = False
    return result


def valid_passport_format(passport_number):
    """
    checks whether a passport number is five sets of five alpha-number characters separated by dashes
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
    checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False