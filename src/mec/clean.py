import pandas as pd


def expand_zip(zips: pd.Series) -> pd.DataFrame:
    """Splits Zip column into Zip and +4 columns."""
    expanded_zips = zips.str.extract(r'^(\d{5})-?(\d{4})?$')
    expanded_zips.columns = ['Zip', '+4']
    expanded_zips= expanded_zips.fillna('')
    return expanded_zips


def standardize_series(input: pd.Series) -> pd.Series:
    """Capitalize all characters and strip all punctuation from a string."""
    clean_input = input.str.replace(r'[^0-9a-zA-Z ]', '', regex=True)
    clean_input = clean_input.str.upper()
    clean_input = clean_input.fillna("")
    return clean_input

def standardize_frame(messy_df: pd.DataFrame) -> pd.DataFrame:
    """Apply `standardize_series` to all columns in a DataFrame."""
    return messy_df.apply(standardize_series)


def street_types_to_abbr(element: str) -> str:
    """Replaces the last word in a string using the inverse of the street suffix map."""
    if element.endswith(" STREET"):
        return element.replace(" STREET", " ST")
    elif element.endswith(" AVENUE"):
        return element.replace(" AVENUE", " AVE")
    else:
        return element

def saint_to_st(element: str) -> str:
    """Replace 'SAINT' with 'ST' if 'SAINT' is the first word in the string."""
    if element.startswith("SAINT "):
        return element.replace("SAINT ", "ST ")
    else:
        return element


def filter_states(states: pd.DataFrame) -> pd.DataFrame:
    """Filter a DataFrame to only include rows with valid U.S. States or territories."""
    valid_states = [
        "AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FM", "FL", "GA",
        "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MH", "MD", "MA",
        "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND",
        "MP", "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT",
        "VT", "VI", "VA", "WA", "WV", "WI", "WY"
    ]
    valid_rows = states[states["State"].isin(valid_states)]
    return valid_rows


def filter_zips(zips: pd.DataFrame) -> pd.DataFrame:
    """Filter a DataFrame to only include rows with valid zipcodes."""
    pattern = r"^[1-9]\d{4}$"
    valid_rows = zips[zips["Zip"].str.match(pattern)]
    return valid_rows


def clean_addresses(addresses: pd.DataFrame) -> pd.DataFrame:
    """Catch-all function to apply all of the above to an Addresses DataFrame."""
    # expand zip
    a= expand_zip(addresses["Zip"])
    addresses["Zip"] = a["Zip"]
    addresses["+4"] = a["+4"]   
    
    # standardize
    addresses = standardize_frame(addresses)
    
    # change addresses
    addresses["Address 1"] = addresses["Address 1"].apply(street_types_to_abbr)
    addresses["Address 2"] = addresses["Address 2"].apply(street_types_to_abbr)
    
    # change city 
    addresses["City"] = addresses["City"].apply(saint_to_st)
    
    # filters
    return filter_zips(filter_states(addresses))


def strip_column_names(contributions: pd.DataFrame) -> pd.DataFrame:
    """Strip leading and trailing whitespace from a DataFrame's column names."""
    return contributions.rename(columns=lambda x: x.strip())
