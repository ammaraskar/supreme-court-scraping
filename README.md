# supreme-court-scraping
Scraping data from the Supreme Court website to gather case data.

## Usage

```
$ python -m sc-scraper
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
