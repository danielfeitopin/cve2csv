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

import logging
import pandas as pd
import requests
import sys
from argparse import ArgumentParser
from pandas import DataFrame
from requests import Response
from bs4 import BeautifulSoup

URL: str = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
CSV_FILE_NAME: str = 'cve.csv'


def fetch_cve_data(keyword: str) -> str:
    """
    Fetches the raw HTML content from the MITRE CVE database for a given search 
    keyword.

    This function builds a URL using the specified keyword to search the MITRE 
    CVE database and sends an HTTP GET request to retrieve the HTML content. If
    the request is successful, it returns the raw HTML as a string. In case of a 
    request error (e.g., network issues, invalid URL), an error message is 
    logged, and the program exits.

    Parameters
    ----------
    keyword : str
        The search keyword used to filter CVE records in the MITRE CVE database.

    Returns
    -------
    str
        The raw HTML content of the CVE search results page as a string.

    Raises
    ------
    SystemExit
        If the HTTP request fails, the function logs the error and exits the 
        program.

    Example
    -------
    >>> html_content = fetch_cve_data("buffer overflow")
    >>> isinstance(html_content, str)
    True
    """

    try:
        response: Response = requests.get(URL + keyword)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        sys.exit(1)


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

    if (div := soup.find(id='TableWithRules')) and (table := div.find('table')):

        rows: list = [[ele.text.strip() for ele in row.find_all(['th', 'td'])]
                      for row in table.find_all('tr')]
    
        if not rows or len(rows) < 2:
            logging.warning("No valid data found in table.")
            return None
        
        if len(rows[0]) != len(rows[1:][0]):
            logging.error("Mismatch between header and row columns.")
            return None
        
        return pd.DataFrame(rows[1:], columns=rows[0])
    
    logging.warning("No table found with id 'TableWithRules'.")
    return None


def save_to_csv(df: DataFrame, output_file: str, delimiter: str = ',',
                encoding: str = 'utf-8'):
    """Saves DataFrame to a CSV file with the specified delimiter and encoding.
    """
    df.to_csv(output_file, index=False, sep=delimiter, encoding=encoding)
    logging.info(f"Data saved to '{output_file}' with delimiter '{delimiter}' "
                 + f"and encoding '{encoding}'.")


def create_parser() -> ArgumentParser:
    """
    Creates and configures the argument parser for the script.

    Returns
    -------
    argparse.ArgumentParser
        Configured ArgumentParser with expected arguments for the script.
    """

    parser = ArgumentParser(
        description="Fetch CVE data from MITRE and save to CSV.")
    parser.add_argument("keyword", help="Search keyword for CVE entries.")
    parser.add_argument("-o", "--output", default=CSV_FILE_NAME,
                        help="Output CSV file name.")
    parser.add_argument("-d", "--delimiter", default=',',
                        help="CSV delimiter.")
    parser.add_argument("-e", "--encoding",
                        default='utf-8', help="CSV encoding.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Increase output verbosity.")
    return parser


def main(keyword, output, delimiter, encoding):
    """Main function to fetch CVE data and save to CSV."""
    
    logging.info(f'Getting results from {URL}{keyword}')
    soup: BeautifulSoup = BeautifulSoup(fetch_cve_data(keyword), 'html.parser')
    n_results: int = get_results_number(soup)
    logging.info(f"There are {n_results} Records that match your search.")
        
    if n_results > 0:
        if (df := extract_table_data(soup)) is not None:
            save_to_csv(df, output, delimiter=delimiter, encoding=encoding)
        else:
            logging.warning("No valid data to save; exiting.")
    else:
        logging.info("No CVE records found for the given keyword.")


if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()

    if args.verbose:
        # Logging
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    main(args.keyword, args.output, args.delimiter, args.encoding)
