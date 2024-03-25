# HW3 - String Data Cleaning

Due: Tues, 3/26 5:00 PM


1. Write a function `expand_zip` that uses `-` to split the ZIP code column into two columns containing the first 5 digits and the last 4 digits. The first column should keep the name `Zip` while the second column should be named `+4`.


2. Write a function `standardize_series` that capitalizes and strips all punctuation from a string Series.

3. Write a function `standardize_frame` that loops through the columns to apply `standardize_series` to each column.

4. Write a function `street_types_to_abbr` that takes a string from an `Address 1` element as input, and replaces the last word in the element with its corresponding abbrevation in `data/street_suffixes.json` if the word is contained in the values for a key. (mapping obtained from [USPS](https://pe.usps.com/text/pub28/28apc_002.htm)).

5. Write a function `saint_to_st` to replace the word "SAINT" with "ST" in a string if "SAINT" is the first word in the string.

6. Write a function `filter_states` that filters an `Address` DataFrame to only include rows that contain a valid US state/territory abbreviation.

7. Write a function `filter_zips` that filters an `Address` DataFrame to only include rows that contain a valid ZIP code.

8. Write a function `clean_addresses` that uses the above functions to clean an entire `Address` DataFrame. Assume that the DataFrame contains *only* the columns `Address 1`, `Address 2`, `City`, `State`, and `ZIP`.

9. The column labeled ` MECID` has a leading space. Write a function `strip_column_names` rename the column by stripping the leading space with `Index.str.strip`.
