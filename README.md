# supreme-court-scraping

Scraping from the Supreme Court website to gather data on granted cases. Then
merges it with data from the [Oyez](https://www.oyez.org/) api for a fuller list
of cases.

## Usage

```
$ scrapy runspider sc_scraper/scraper.py -o cases.json
```

Will run the scrapper and output the granted cases to a `cases.json` file.

```
$ python -m sc_scraper
```

will then merge the data with the Oyez data for a fully populated
`case_summaries.json` file.

### Schema

The cases in `case_summaries.json` are sorted by their dates (newest on top)
and have this schema:

```json
[
    {
        "docket_number": "The docket number used to reference the case in court",
        "date": "The last known date assosciated with the case",
        "title": "Plantiff v. Defendant (e.g Roe v. Wade)",
        "details_url": "Link to more details on the case (if available)",
        "term": "Which term of the Supreme Court the case was brought forward (if available)",
        "description": "A basic description of the case (if available)",
        "question": "The questions put forth in the case (if available)"
    },
    {
        "docket_number": "70-18",
        "date": "1973-01-22 06:00:00",
        "title": "Roe v. Wade",
        "details_url": "https://api.oyez.org/cases/1971/70-18",
        "term": "1971",
        "description": "A case in which the court held that a woman's right to an abortion fell within the right to privacy granted in the Fourteenth Amendment.",
        "question": "<p>Does the Constitution embrace a woman's right to terminate her pregnancy by abortion?</p>\n"
    },
]
```

## Installation

A virtualenv is highly recommended to keep `supreme-court-scraping`'s
dependencies isolated from your system.

### Linux

```
python3 -m venv venv
. venv/bin/activate
```

### Windows

```
python3 -m venv venv
venv\Scripts\activate.bat
```

### Installing the project

After you've created and activated the virtualenv, you can install the project
with `pip install -e .`

## Testing

```
pip install -e ".[test]"
pytest
```

## Formatting

Use [black](https://github.com/psf/black) for formatting the code:

```shell
pip install black
black .
```
