""" Module to test papers.py  """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v5"

# imports one per line
import pytest
from papers import decide


def test_basic():
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
    assert decide("test_JSON_files/01-qyiytransitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/02-qyiytransitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/03-qyiytransitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/04-qyiytransitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/05-qyiytransitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/06-qyiytransitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/07-qyiyvisitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/08-qyiyvisitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/09-qyiyvisitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/10-qyiyvisitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/11-qyiyvisitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/12-qyiyvisitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/13-qyiyfromvnavvnahywn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/14-qyintransitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/15-qyintransitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/16-qyintransitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/17-qyintransitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/18-qyintransitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/19-qyintransitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/20-qyinvisitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/21-qyinvisitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/22-qyinvisitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/23-qyinvisitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/24-qyinvisitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/25-qyinvisitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/26-qyinfromvnavvnahywn.json",
                  "watchlist.json", "countries.json") == ["Quarantine"]


def test_secondary():
    """
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file
    with entry records of travellers who should all be "Secondary";
    (i.e., who are on the watchlist).

    Included cases: whether traveller is in transit or visiting with valid or
    invalid visa, or in transit or visiting from a country with no visa needed.
    """
    assert decide("test_JSON_files/27-qniytransitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/31-qniytransitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/33-qniyvisitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/35-qniyvisitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/37-qniyvisitvnvvnahnwy.json",
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
    assert decide("test_JSON_files/28-qniytransitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/32-qniytransitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/34-qniyvisitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Accept"]

    assert decide("test_JSON_files/38-qniyvisitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/39-qniyfromvnavvnahywn.json",
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

    Also includes tests for entry records where birthdays are after "today" or
    earlier than 120 years ago, missing keys and/or values,
    invalidly formatted dates or passport numbers, and countries
    that aren't on the country list.
    """
    assert decide("test_JSON_files/29-qniytransitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/30-qniytransitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/36-qniyvisitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/40-qnintransitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/41-qnintransitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/42-qnintransitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/43-qnintransitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/44-qnintransitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/45-qnintransitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/46-qninvisitvyvvyhnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/47-qninvisitvyvvyhnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/48-qninvisitvyvvnhnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/49-qninvisitvyvvnhnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/50-qninvisitvnvvnahnwy.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/51-qninvisitvnvvnahnwn.json",
                  "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/52-qninfromvnavvnahywn.json",
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
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
