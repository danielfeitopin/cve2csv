"""
cve2csv.py

This module extracts CVE vulnerability information from the MITRE CVE database 
and saves the results to a CSV file. It performs web scraping to fetch CVE records 
based on keywords provided via the command line and converts the results into a 
pandas `DataFrame` for easy processing.

Functions:
----------
- get_results_number(soup: BeautifulSoup) -> int:
    Extracts and returns the number of vulnerability search results.

- extract_table_data(soup: BeautifulSoup) -> DataFrame | None:
    Extracts CVE table data from the HTML page and converts it into a pandas `DataFrame`.

Usage:
------
Run this module from the command line with keywords for the search, for example:

    python cve2csv.py keyword

This generates a file `cve.csv` in the current directory containing the CVE search 
results in CSV format.

Dependencies:
-------------
This module requires the following libraries:
- pandas
- requests
- BeautifulSoup (from bs4)

"""

import pandas as pd
import requests
from pandas import DataFrame
from requests import Response
from bs4 import BeautifulSoup
from sys import argv

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


if __name__ == '__main__':

    URL: str = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
    keyword: str = '%20'.join(argv[1:]) if len(argv) > 1 else ''
    print(f'Getting results from {URL}{keyword}')
    response: Response = requests.get(URL + keyword)

    if response.status_code == 200:  # Ok
        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        n_results: int = get_results_number(soup)
        print(f"There are {n_results} CVE Records that match your search.")

        if n_results > 0:
            df: DataFrame = extract_table_data(soup)
            df.to_csv(CSV_FILE_NAME, index=False)

    else:
        print(f"Error al obtener la página: {response.status_code}")
