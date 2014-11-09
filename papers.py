""" Computer-based immigration office for Kanadia """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v8"

# imports one per line
import re
import os
import datetime
import json
from datetime import date


def decide(input_file, watchlist_file, countries_file):
    """
    decides whether a traveller's entry into Kanadia should be accepted
    :param input_file: name of a JSON formatted file that contains all people's entry record and passport
        information (e.g., number, name, birth date, etc.) in alphanumeric format
    :param watchlist_file: name of a JSON formatted file that contains names and passport numbers on a watchlist in
        alphanumeric format
    :param countries_file: name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory in alphanumeric format
    :return: list of strings; possible values of strings are: "Quarantine", "Reject", "Secondary", and "Accept"
    """
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"
    #open the json files and load information into dictionaries and lists
    with open(__location__ + countries_file) as json_countries_data, \
            open(__location__ + watchlist_file) as json_watchlist_data, \
            open(__location__ + input_file) as json_entries_data:
        countries = json.load(json_countries_data)
        watch_list = json.load(json_watchlist_data)
        entries = json.load(json_entries_data)

    #the variable "decisions" is the final result which this method returns
    decisions = []
    #loop over all the entries in the list that come from input_file
    #form of loop -> access every elements inside a list/tuple of string in order
    for item in entries:
            #check if traveller meets quarantine criteria
            if is_valid_passport_for_quarantine(item, countries):
                decisions += ["Reject"]
            elif is_quarantine(item, countries):
                decisions += ["Quarantine"]
            #check if traveller meets reject criteria
            elif is_reject(item, countries):
                decisions += ["Reject"]
            #check if traveller meets secondary criteria
            elif is_secondary(item, watch_list):
                decisions += ["Secondary"]
            #traveller is permitted to enter the country if he/she passes all the checked criteria
            else:
                decisions += ["Accept"]
    return decisions


def is_valid_passport_for_quarantine(entry_record, countries_dict):
    """

    :param entry_record:
    :param countries_dict:
    :return:
    """
    if not "home" in entry_record.keys() or not "from" in entry_record.keys():
        return True
    if not "country" in entry_record["home"].keys() or not "country" in entry_record["from"].keys():
        return True

    if not entry_record["home"]["country"].upper() in countries_dict.keys() and \
            entry_record["home"]["country"].upper() != "KAN":
        return True
    elif not entry_record["from"]["country"].upper() in countries_dict.keys():
        return True

    return False


def is_quarantine(entry_record, countries_dict):
    """
    checks whether traveller meets condition for quarantine
    :param entry_record: the traveller's entry record information
    :param countries_dict: list of countries requiring a visa, and countries with medical advisories
    :return: Boolean; Return True if the record meets quarantine criteria, False otherwise
    """

    #check if "from" country is flagged for medical advisory
    if "from" in entry_record.keys():
        if "country" in entry_record["from"].keys():
            from_country = entry_record["from"]["country"].upper()
            if countries_dict[from_country]["medical_advisory"] != "":
                return True
    #check if "via" country is flagged for medical advisory
    if "via" in entry_record.keys():
        if "country" in entry_record["via"].keys():
            via_country = entry_record["via"]["country"].upper()
            if countries_dict[via_country]["medical_advisory"] != "":
                return True
    else:
        return False


def is_reject(entry_record, country_dict):
    """
    checks whether traveller meets condition for rejection of entry
    :param entry_record: the traveller's entry record information
    :param country_dict: list of countries requiring a visa, and countries with medical advisories
    :return: Boolean; True if the record meets the reject criteria, False otherwise
    """
    #check if entry record is incomplete
    if not is_valid_entry_record(entry_record, country_dict):
        return True
    #check if "from" country is in the country file
    from_country = entry_record["from"]["country"].upper()

    if not from_country in country_dict.keys() and from_country != "KAN":
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
    checks whether traveller is on the watchlist and must be sent to secondary
    :param entry_record: the traveller's entry record information
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
    checks whether traveller has a valid visa to enter
    :param entry_record: the traveller's entry record information
    :return: Boolean; False if visa entry not in record or if the visa is older than 2 years, True otherwise
    """
    #establish the current date
    now = datetime.datetime.now()
    #check if traveller has a visa
    if "visa" not in entry_record.keys():
        return False

    if not valid_date_format(entry_record["visa"]["date"]):
        return False

    #convert the visa date from str to datetime format
    record_visa_date = datetime.date(int(entry_record["visa"]["date"][0:4]),
                                     int(entry_record["visa"]["date"][5:7]),
                                     int(entry_record["visa"]["date"][8:10]))
    #compute the earliest acceptable visa date
    earliest_issue_date = datetime.date(now.year-2, now.month, now.day)

    #compare the visa date to check if within 2 years
    if record_visa_date > earliest_issue_date:
        return True
    else:
        return False


def is_valid_entry_record(entry_record, countries_dict):
    """
    checks whether traveller's entry record has all the information needed for entrance
    :param entry_record: the traveller's entry record information
    :return: Boolean; True if the format is valid, False otherwise
    """
    #list of all the required info from the traveller's passport
    required_info = ["home", "first_name", "last_name", "passport", "entry_reason", "from", "birth_date"]
    #loop to check every item in the required info list is in the record entry
    for item in required_info:
        if not item in entry_record.keys():
            return False
    #check if the traveller's "home" information is complete
    if not "country" in entry_record["home"].keys() or not "city" in entry_record["home"].keys() \
            or not "region" in entry_record["home"].keys() or not entry_record["home"]["country"] != "":
        return False
    #check if the traveller's "from" information is complete
    elif not "country" in entry_record["from"].keys() or not "city" in entry_record["from"].keys() \
            or not "region" in entry_record["from"].keys()or not entry_record["from"]["country"] != "":
        return False
    #check if traveller's birth date format is correct
    elif not valid_date_format(entry_record["birth_date"])or not entry_record["birth_date"] != "":
        return False
    #check if format of traveller's passport is correct
    elif not valid_passport_format(entry_record["passport"])or not entry_record["passport"] != "":
        return False
    #if traveller has a visa, check if visa date format is complete
    elif "visa" in entry_record.keys():
        if not valid_date_format(entry_record["visa"]["date"])or not entry_record["visa"]["date"] != "":
            return False
    return True


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
        time = datetime.datetime.strptime(date_string, '%Y-%m-%d')

        if time.year > date.today().year:
            return False
        elif time.year == date.today().year and time.month > date.today().month:
            return False
        elif time.year == date.today().year and time.month == date.today().month and time.day > date.today().day:
            return False

        if time.year < (date.today().year - 100):
            return False

        return True
    except ValueError:
        return False