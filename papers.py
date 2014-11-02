#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
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

        via_country = ""
        transit = False
        if "via" in item.keys():
            via_country = item["via"]["country"]
        if item["entry_reason"] == "transit":
            transit = True
        if "from" in item.keys() and "home" in item.keys():
            from_country = item["from"]["country"].upper()
            home_country = item["home"]["country"].upper()
            #Check if the country where the visitor "came from" is medical_advisory
            if from_country != "" and countries[from_country]["medical_advisory"]== "1":
                decisions += ["Quarantine"]
            #Check if the country where the visitor "via" is medical_advisory
            elif via_country != "" and countries[via_country]["medical_advisory"] == "1":
                decisions += ["Quarantine"]
            #uses the not_valid_passport method created to check if all the required info is in the passport
            elif not valid_passport_info(item):
                decisions += ["Reject"]
            #Check if the from_country is in the country file
            elif not from_country in countries.keys():
                decisions += ["Reject"]
            #Use check_watchlist method created to check if the person is on the watchlist
            elif not check_watchlist(item, watch_list):
                decisions += ["Secondary"]
            #check if the person's home country is KAN and is he/she is returning home, accept
            elif home_country.upper() == "KAN" and item["entry_reason"].upper() == "RETURNING":
                decisions += ["Accept"]
            #check if the person's visa or via visa is valid
            elif transit or item["entry_reason"].upper() == "VISIT":
                decisions += [check_visa(item, countries[from_country], transit)]
            #vister is permitted to enter the country if he/she passes all the checked criteria
            else:
                decisions += ["Accept"]
        else:
            decisions += ["Reject"]
    return decisions

#A method used to check if the person is on the watchlist


#A method used to check if the person has the valid visa to enter


#To check if the person's passport has all the info needed for entrance


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

