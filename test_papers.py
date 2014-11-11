""" Module to test papers.py  """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v7"

# imports one per line
import pytest
from papers import decide


def test_basic():
    """
    Basic tests to tests provided to test for: accepting returning citizens,
    for traveller's who are on the watchlist and should be flagged to
    secondary, and for traveller's who should be flagged to quarantine.
    """
    assert decide("test_returning_citizen.json", "watchlist.json",
                  "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json",
                  "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json",
                  "countries.json") == ["Quarantine"]


def test_quarantine():
    """
    Inputs a watchlist JSON file, a countries JSON file,
    and a JSON file with entry records of
    travellers who should all be quarantined.

    Included cases: whether their entry records are complete/correct;
    whether the traveller is in transit, visiting or from KAN;
    whether or not their visa is valid; and whether or not
    the traveller is on the watchlist.
    """
    assert decide("test_JSON_files/test_01.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_02.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_03.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_04.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_05.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_06.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_07.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_08.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_09.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_10.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_11.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_12.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_13.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_14.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_15.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_16.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_17.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_18.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_19.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_20.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_21.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_22.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_23.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_24.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/test_25.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/test_26.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]


def test_secondary():
    """
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file
    with entry records of travellers who should all be "Secondary";
    (i.e., who are on the watchlist).

    Included cases: whether traveller is in transit or visiting with valid or
    invalid visa, or in transit or visiting from a country with no visa needed.
    """
    assert decide("test_JSON_files/test_27.json",
                  "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/test_28.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_33.json",
                  "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/test_35.json",
                  "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/test_37.json",
                  "watchlist.json", "countries.json") == ["Secondary"]


def test_accept():
    """
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file
    with entry records of travellers who should all be accepted.

    Included cases: whether the traveller is in transit, or visiting with
    visa required and visa is valid, in transit or visiting with no visa
    required, or traveller is from KAN.

    Also includes tests of fields with both upper and lower case values.
    """
    assert decide("test_JSON_files/test_28.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/test_32.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/test_34.json",
                  "watchlist.json", "countries.json") == ["Accept"]

    assert decide("test_JSON_files/test_38.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/test_39.json",
                  "watchlist.json", "countries.json") == ["Accept"]

    assert decide("test_JSON_files/test_lower_case.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/test_upper_case.json",
                  "watchlist.json", "countries.json") == ["Accept"]


def test_reject():
    """
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file with
    entry records of travellers who should all be rejected.

    Included cases: incomplete or incorrect entry records whether traveller is
    in transit, visiting or from KAN; whether or not a visa is required but
    out of date range, wrong code length or not present; and whether or not
    the traveller is on a the watchlist.

    Also includes tests for entry records where birthdays are future dated
    or earlier than 150 years ago (assumption is no one is older than this
    age), missing keys and/or values, invalidly formatted dates or passport
    numbers, and countries that are not on the country list.
    """
    assert decide("test_JSON_files/test_29.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_30.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_36.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_40.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_41.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_42.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_43.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_44.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_45.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_46.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_47.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_48.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_49.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_50.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_51.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/test_52.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_dates.json", "watchlist.json",
                  "countries.json") == ["Reject", "Reject", "Reject",
                                        "Reject", "Reject", "Reject"]

    assert decide("test_JSON_files/test_invalid_country.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/test_missing_entry_pairs.json",
                  "watchlist.json", "countries.json") == ["Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject"]

    assert decide("test_JSON_files/test_missing_keys.json",
                  "watchlist.json", "countries.json") == ["Reject", "Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject"]

    assert decide("test_JSON_files/test_missing_values.json",
                  "watchlist.json", "countries.json") == ["Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject",
                                                          "Reject", "Reject"]


def test_files():
    """
    Function to raise error if file is not found.
    """
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
