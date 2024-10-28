"""
cve2csv.py

This module extracts CVE vulnerability information from the MITRE CVE database 
and saves the results to a CSV file. It performs web scraping to fetch CVE 
records based on keywords provided via the command line and converts the results
into a pandas `DataFrame` for easy processing.

Functions:
----------
- get_results_number(soup: BeautifulSoup) -> int:
    Extracts and returns the number of vulnerability search results.

- extract_table_data(soup: BeautifulSoup) -> DataFrame | None:
    Extracts CVE table data from the HTML page and converts it into a pandas \
        `DataFrame`.

Usage:
------
Run this module from the command line with keywords for the search, for example:

    python cve2csv.py keyword

This generates a file `cve.csv` in the current directory containing the CVE 
search results in CSV format.

Dependencies:
-------------
This module requires the following libraries:
- pandas
- requests
- BeautifulSoup (from bs4)

"""

import argparse
import logging
import pandas as pd
import requests
import sys
from pandas import DataFrame
from requests import Response
from bs4 import BeautifulSoup

CSV_FILE_NAME: str = 'cve.csv'


def get_results_number(soup: BeautifulSoup) -> int:
    """Get the rumber of results from the response.

    Response HTML example::
    .. highlight:: html
    .. code-block:: html

        <h2>Search Results</h2>
        <div class="smaller" style="...">
        There are <b>0</b> CVE Records that match your search.
        </div>

    Parameters
    ----------
        soup (BeautifulSoup): A `BeautifulSoup` object containing the parsed\
            HTML content.

    Returns
    -------
        int | None: Number of results if possible, otherwise `None`.
    """

    return int(b.text) if (h2 := soup.find('h2', string='Search Results'))\
        and (div := h2.find_next_sibling())\
        and (b := div.find('b')) else 0


def extract_table_data(soup: BeautifulSoup) -> DataFrame | None:
    """Extracts table data from a `BeautifulSoup` object and converts it into a 
    pandas `DataFrame`.

    This function searches for a `<div>` element with the id 'TableWithRules' 
    within the provided `BeautifulSoup` object. If such a `<div>` is found and 
    it contains a <table> element, the function extracts the text content of all
    `<th>` and `<td>` elements within the table, organizes them into rows, and 
    converts these rows into a pandas `DataFrame`. The first row of the table 
    is used as the column headers for the `DataFrame`.

    Parameters
    ----------
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML\
            content.

    Returns
    -------
        DataFrame | None: A pandas `DataFrame` containing the table data if the\
            table is found, otherwise `None`.
    """

    if (div := soup.find(id='TableWithRules'))\
            and (table := div.find('table')):

        rows: list = [[ele.text.strip() for ele in row.find_all(['th', 'td'])]
                      for row in table.find_all('tr')]

        return pd.DataFrame(rows[1:], columns=rows[0])


def main(keyword: str, output: str = CSV_FILE_NAME):
    """Main function to fetch CVE data and save to CSV."""

    URL: str = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
    keyword: str = '%20'.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    logging.info(f'Getting results from {URL}{keyword}')

    try:
        response: Response = requests.get(URL + keyword)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        sys.exit(1)

    if response.status_code == 200:  # Ok
        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        n_results: int = get_results_number(soup)
        logging.info(f"There are {n_results} Records that match your search.")

        if n_results > 0:
            df: DataFrame = extract_table_data(soup)
            df.to_csv(CSV_FILE_NAME, index=False)


if __name__ == '__main__':

    # Parser
    parser = argparse.ArgumentParser(
        description="Fetch CVE data and save to CSV.")
    parser.add_argument("keyword", help="Search keyword for CVE entries.")
    parser.add_argument("-o", "--output", default=CSV_FILE_NAME,
                        help="Output CSV file name.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Increase output verbosity.")
    args = parser.parse_args()

    if args.verbose:
        # Logging
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    main(args.keyword, args.output)
