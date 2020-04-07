# Generates data for Algolia search
from pathlib import Path
import time
from datetime import datetime
import json
import re

base_folder = Path(__file__) / ".." / ".."
CASE_SUMMARIES = base_folder / "case_summaries.json"
CATEGORIES = base_folder / "categories.json"

def main():
    with open(CASE_SUMMARIES, 'r') as f:
        case_summaries = json.load(f)
    with open(CATEGORIES, 'r') as f:
        categories = json.load(f)

    records = []
    for case in case_summaries:
        date = datetime.strptime(case["date"], "%Y-%m-%d %H:%M:%S")
        unix_time = (date - datetime(1970,1,1)).total_seconds()

        record = {
            "objectID": case["docket_number"],
            "date": int(unix_time),
            "date_timestamp": date.strftime("%d %b, %Y"),
            "description": case["description"],
            "question": re.sub('<[^<]+?>', '', case["question"] or ''),
            "categories": [categories[str(id)] for id in case["categories"]],
            "title": case["title"]
        }
        records.append(record)

    print(json.dumps(records))

if __name__ == "__main__":
    main()
