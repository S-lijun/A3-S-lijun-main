import pandas as pd
import pytest
from mec import clean


def test_expand_zip():
    zips = pd.Series(["63130-0000", "63130", ""])
    actual = clean.expand_zip(zips)
    pd.testing.assert_frame_equal(
        actual,
        pd.DataFrame({"Zip": ["63130", "63130", ""], "+4": ["0000", "", ""]}),
    )


def test_standardize_series():
    input = pd.Series(["A.", "?-b", "C", "!!"])
    pd.testing.assert_series_equal(
        clean.standardize_series(input), pd.Series(["A", "B", "C", ""])
    )


def test_standardize_frame():
    addresses = pd.DataFrame(
        {
            "Address 1": ["123 main street."],
            "Address 2": [""],
            "City": ["st. louis"],
            "State": ["MO"],
            "Zip": ["63130"],
        },
    )
    actual = clean.standardize_frame(addresses)
    pd.testing.assert_frame_equal(
        actual,
        pd.DataFrame(
            {
                "Address 1": ["123 MAIN STREET"],
                "Address 2": [""],
                "City": ["ST LOUIS"],
                "State": ["MO"],
                "Zip": ["63130"],
            },
        ),
    )


@pytest.mark.parametrize(
    ("element", "expected"),
    [("SAINT LOUIS", "ST LOUIS"), ("SAINT CHARLES", "ST CHARLES")],
)
def test_saint_to_st(element, expected):
    actual = clean.saint_to_st(element)
    assert actual == expected


@pytest.mark.parametrize(
    ("element", "expected"),
    [
        ("123 MAIN STREET", "123 MAIN ST"),
        ("1600 PENNSYLVANIA AVENUE", "1600 PENNSYLVANIA AVE"),
    ],
)
def test_street_suffixes(element, expected):
    actual = clean.street_types_to_abbr(element)
    assert actual == expected


def test_filter_states():
    states = pd.DataFrame({"State": ["MO", "12", ""]})
    pd.testing.assert_frame_equal(
        clean.filter_states(states),
        pd.DataFrame(
            {"State": ["MO"]},
        ),
    )


def test_filter_zips():
    zips = pd.DataFrame({"Zip": ["63130", "ABCDE", "06463"]})
    pd.testing.assert_frame_equal(
        clean.filter_zips(zips),
        pd.DataFrame(
            {"Zip": ["63130"]},
        ),
    )


def test_clean_addresses():
    addresses = pd.DataFrame(
        {
            "Address 1": ["123 main street.", "", ""],
            "Address 2": ["", "", ""],
            "City": ["saint louis", "", ""],
            "State": ["MO", "12", "MO"],
            "Zip": ["63130-4862", "63130", "06463"],
        },
    )
    cleaned = clean.clean_addresses(addresses)
    pd.testing.assert_frame_equal(
        cleaned,
        pd.DataFrame(
            {
                "Address 1": ["123 MAIN ST"],
                "Address 2": [""],
                "City": ["ST LOUIS"],
                "State": ["MO"],
                "Zip": ["63130"],
                "+4": ["4862"],
            },
        ),
    )


def test_strip_column_name_spaces():
    contributions = pd.DataFrame({" MECID": []})
    assert set(clean.strip_column_names(contributions).columns) == {"MECID"}
