#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Amy Kwan, Jessica Mann, Susan Sim'
__email__ = "amykwan.cma@gmail.com, jessmann74@gmail.com, ses@drsusansim.org"

__copyright__ = "2014 AKJMSM"
__license__ = "MIT License"

__status__ = "v1"

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_quarantine():
    """
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file with entry records of
    travellers who should all be quarantined. Included cases: whether they are in transit,
    visiting or from KAN, whether or not their visa is valid, and whether or not they are on a watchlist.
    """
    assert decide("test_JSON_files/01-qyiytransitvyvvyhnwy.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/02-qyiytransitvyvvyhnwn.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/03-qyiytransitvyvvnhnwy.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/04-qyiytransitvyvvnhnwn.json", "watchlist.json", "countries.json") == ["Quarantine"]
    """assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_secondary():
    """"""
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file with entry records of
    travellers who should all be "Secondary"; i.e. who are on the watchlist.
    Included cases: whether they are in transit or visiting with valid or invalid visas, or
    in transit or visiting from a country with no visa needed.
    """"""
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Secondary"]


def test_accept():
    """"""
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file with entry records of
    travellers who should all be accepted.
    Included cases: whether they are in transit or visiting with visas needed and valid,
    in transit or visiting with no visa needed, or from KAN.
    """"""
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Accept"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Accept"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Accept"]


def test_reject():
    """"""
    Inputs a watchlist JSON file, a countries JSON file, and a JSON file with entry records of
    travellers who should all be accepted.
    Included cases: incomplete entry records whether they are in transit,
    visiting or from KAN, whether or not their visa is valid, and whether or not they are on a watchlist.
    Also includes rejection for complete entry records where visa is required but invalid or not present.
    """"""
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide(test_JSON_files/"xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]

    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_JSON_files/xxx.json", "watchlist.json", "countries.json") == ["Reject"]
"""

def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

# add functions for other tests

