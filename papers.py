""" Computer-based immigration office for Kanadia """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v8"

# imports one per line
import re
import datetime
import json
from datetime import date
import os


def decide(input_file, watchlist_file, countries_file):
    """
    decides whether each traveller's entry into Kanadia should be accepted
    :param input_file: name of a JSON formatted file that contains all people's
        passport information (e.g., number, name, birth date, etc.)
    :param watchlist_file: name of a JSON formatted file that contains names
        and passport numbers on a watchlist
    :param countries_file: name of a JSON formatted file that contains country
        data, such as whether an entry or transit visa is required, and whether
        there is currently a medical advisory
    :return: list of strings; possible values of strings are: "Quarantine",
        "Reject", "Secondary", and "Accept"
    """

    #enables test file to be executed in PyCharm
    __location__ = "{0}\\".format(os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))))

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
    for item in entries:
            #check if traveller meets quarantine criteria
            if is_quarantine(item, countries):
                decisions += ["Quarantine"]
            #check if traveller meets reject criteria
            elif is_reject(item, countries):
                decisions += ["Reject"]
            #check if traveller meets secondary criteria
            elif is_secondary(item, watch_list):
                decisions += ["Secondary"]
            #permitted to enter country if passes all checked criteria
            else:
                decisions += ["Accept"]
    return decisions


def is_quarantine(entry_record, countries_dict):
    """
    checks whether traveller meets condition for quarantine
    :param entry_record: the traveller's entry record information
    :param countries_dict: list of countries requiring a visa,
        and countries with medical advisories
    :return: Boolean; Return True if the record meets quarantine
        criteria, False otherwise
    """

    #check if "from" country is flagged for medical advisory
    if "from" in entry_record.keys():
        if "country" in entry_record["from"].keys():
            from_country = entry_record["from"]["country"].upper()
            if entry_record["from"]["country"].upper() \
                    in countries_dict.keys():
                if countries_dict[from_country]["medical_advisory"] != "":
                    return True

    #check if "via" country is flagged for medical advisory
    if "via" in entry_record.keys():
        if "country" in entry_record["via"].keys():
            via_country = entry_record["via"]["country"].upper()
            if entry_record["via"]["country"].upper() in countries_dict.keys():
                if countries_dict[via_country]["medical_advisory"] != "":
                    return True
    else:
        return False


def is_reject(entry_record, country_dict):
    """
    checks whether traveller meets condition for rejection of entry
    :param entry_record: the traveller's entry record information
    :param country_dict: list of countries requiring a visa,
        and countries with medical advisories
    :return: Boolean; True if the record meets the reject
        criteria, False otherwise
    """

    #check if entry record is incomplete
    if not is_valid_entry_record(entry_record):
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

    #checks the traveller's name against the watchlist
    for suspect in watch_list:
        if entry_record["first_name"].upper() \
                == suspect["first_name"].upper() \
                and entry_record["last_name"].upper() \
                == suspect["last_name"].upper():
            return True
        elif entry_record["passport"] == suspect["passport"]:
            return True
    return False


def is_valid_visa(entry_record):
    """
    checks whether traveller has a valid visa to enter
    assumption: visa dates are based on issue date, not expiry date
    :param entry_record: the traveller's entry record information
    :return: Boolean; False if visa entry not in record or if visa
        is older than 2 years, True otherwise
    """

    #establish the current date
    now = datetime.datetime.now()

    #check whether traveller has a visa
    if "visa" not in entry_record.keys():
        return False
    #checks whether visa date format and date range are correct
    if not valid_date_format(entry_record["visa"]["date"]):
        return False

    #convert the visa date to date/time format
    record_visa_date = datetime.datetime.strptime(
        entry_record["visa"]["date"], '%Y-%m-%d')

    #compute the earliest acceptable visa date
    earliest_issue_date = datetime.date(now.year-2, now.month, now.day)

    #compare the visa date to check if within 2 years
    if datetime.date(record_visa_date.year, record_visa_date.month,
                     record_visa_date.day) > earliest_issue_date:
        return True
    else:
        return False


def is_valid_entry_record(entry_record):
    """
    checks if traveller's entry record has all info needed for entrance
    :param entry_record: the traveller's entry record information
    :return: Boolean; True if the format is valid, False otherwise
    """

    #list of all the required info from the traveller's passport
    required_info = ["home", "first_name", "last_name", "passport",
                     "entry_reason", "from", "birth_date"]
    #list of all the required country information
    required_country_info = ["city", "region", "country"]
    #list of all the required visa information
    required_visa_info = ["date", "code"]

    #check every item in the required info list is in the record entry
    for item in required_info:
        if not item in entry_record.keys():
            return False
        elif entry_record[item] == "":
            return False
        #check if information for "home" and "from" is complete
        if item == "home" or item == "from":
            for sub_item in required_country_info:
                if not sub_item in entry_record[item].keys():
                    return False
                elif entry_record[item][sub_item] == "":
                    return False

    #checks for "via" information if this information is included
    if "via" in entry_record.keys():
        #check every sub_item in the required info list is in the record entry
        for via_item in required_country_info:
            if not via_item in entry_record["via"].keys():
                return False
            elif entry_record["via"][via_item] == "":
                return False

    #check for "visa" information if this information is included
    if "visa" in entry_record.keys():
        #check every sub_item in the required info list is in the record entry
        for visa_item in required_visa_info:
            if not visa_item in entry_record["visa"].keys():
                return False
            elif entry_record["visa"][visa_item] == "":
                return False

    #check if the traveller's "home" information is complete
    if not "country" in entry_record["home"].keys() \
            or not "city" in entry_record["home"].keys() \
            or not "region" in entry_record["home"].keys():
        return False
    #check if the traveller's "from" information is complete
    elif not "country" in entry_record["from"].keys() \
            or not "city" in entry_record["from"].keys() \
            or not "region" in entry_record["from"].keys():
        return False
    #check if traveller's birth date format is correct
    elif not valid_date_format(entry_record["birth_date"]):
        return False
    #check if format of traveller's passport is correct
    elif not valid_passport_format(entry_record["passport"]):
        return False
    #if traveller has a visa, check if visa date format is complete
    elif "visa" in entry_record.keys():
        if not valid_date_format(entry_record["visa"]["date"]):
            return False
    return True


def valid_passport_format(passport_number):
    """
    checks whether a passport number is five sets of five
        alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """

    passport_format = re.compile('^.{5}-.{5}-.{5}-.{5}-.{5}$')
    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    checks whether a date has the format YYYY-mm-dd in numbers
    checks whether the date range is valid (i.e., no future dated dates,
        birth date within 150 years)
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, True if date range
        is valid, False otherwise
    """

    try:
        time = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        if datetime.date(time.year, time.month, time.day) > date.today():
            return False
        if time.year < (date.today().year - 150):
            return False
        return True
    except ValueError:
        return False
