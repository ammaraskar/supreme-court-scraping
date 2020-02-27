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

The schema of the `case_summaries.json` file is as follows:

```json
{
    "docket_number": {
        
    }
}
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
