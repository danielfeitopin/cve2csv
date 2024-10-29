# cve2csv

<div align="center">

***A Python module to fetch CVE data and save it to CSV.***

[![Python](https://img.shields.io/badge/Python_3-black?logo=python&logoColor=white&labelColor=grey&color=%233776AB)](<https://www.python.org/> "Python")
[![Pandas](https://img.shields.io/badge/Pandas-black?logo=pandas&logoColor=white&labelColor=grey&color=%23150458)](<https://pandas.pydata.org/> "Pandas")

[![License: MIT](<https://img.shields.io/github/license/danielfeitopin/cve2csv>)](LICENSE "License")
[![GitHub issues](https://img.shields.io/github/issues/danielfeitopin/cve2csv)](<https://github.com/danielfeitopin/cve2csv> "Issues")
[![GitHub stars](https://img.shields.io/github/stars/danielfeitopin/cve2csv)](<https://github.com/danielfeitopin/cve2csv/stargazers> "Stars")

</div>


## Table of Contents

- [cve2csv](#cve2csv)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Use](#use)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Description

This module extracts CVE vulnerability information from the MITRE CVE database and saves the results to a CSV file. It performs web scraping to fetch CVE records based on keywords provided via the command line and converts the results into a pandas `DataFrame` for easy processing.

## Installation

```sh
pip install -r requirements.txt
```

## Use

```sh
python cve2csv.py
```

Help menu:

```
python cve2csv.py -h
```

```
usage: cve2csv.py [-h] [-o OUTPUT] [-v] keyword

Fetch CVE data and save to CSV.

positional arguments:
  keyword                     Search keyword for CVE entries.

options:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  Output CSV file name.
  -v, --verbose               Increase output verbosity.
```

## Contributing

Contributions are welcome! If you have improvements, bug fixes, or new modules to add, feel free to submit a pull request.

## License

The content of this repository is licensed under the [BSD-3-Clause License](LICENSE).

## Contact

Feel free to get in touch with me!

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-%23181717?style=for-the-badge&logo=github&logoColor=%23181717&color=white)](<https://github.com/danielfeitopin>)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-white?style=for-the-badge&logo=linkedin&logoColor=white&color=%230A66C2)](<https://www.linkedin.com/in/danielfeitopin/>)

</div>