from pathlib import Path
import collections
import json
import requests
from datetime import datetime, timedelta


base_folder = Path(__file__) / ".." / ".."
OYEZ_DATA_FILE = base_folder / "oyez_data" / "oyez_data.json"
OYEZ_CATEGORY_FILE = base_folder / "oyez_data" / "oyez_categories.json"
OYEZ_CATEGORY_FOLDER = base_folder / "oyez_data" / "categories"

OYEZ_CATEGORY_FOLDER.mkdir(parents=True, exist_ok=True)


def parse_unix_timestamp_even_negative(timestamp):
    # Needed because windows can't natively handle negative timestamps :|
    return datetime(1970, 1, 1) + timedelta(seconds=timestamp)


def main():
    download_oyez_data()
    with open(OYEZ_DATA_FILE, "r") as f:
        oyez_data = json.load(f)
    with open(OYEZ_CATEGORY_FILE, "r") as f:
        oyez_categories = json.load(f)
    categories, case_categories = download_and_load_category_data(oyez_categories)

    with open(base_folder / "categories.json", "w") as f:
        categories_by_id = {}
        for category in categories:
            categories_by_id[category.id] = category.name
        json.dump(categories_by_id, f, indent=4)

    # Latest data is disabled until pdf files can be processed.
    #with open(base_folder / "cases.json", "r") as f:
    #    latest_confirmed = json.load(f)

    case_summaries = {}
    for docket_object in oyez_data:
        docket_number = docket_object["docket_number"]

        # Grab the date of the last event in the timeline
        last_event_time = docket_object["timeline"]
        if not last_event_time:
            continue
        last_event_time = last_event_time[-1]["dates"][0]
        last_event_time = parse_unix_timestamp_even_negative(last_event_time)

        # If we have a duplicate, allow the newer one to override it.
        if docket_number in case_summaries:
            old_case = case_summaries[docket_number]
            if old_case["date"] > last_event_time:
                continue

        decided = False
        for event in docket_object["timeline"]:
            if event["event"] == "Decided":
                decided = True

        case_summaries[docket_number] = {
            "docket_number": docket_object["docket_number"],
            "decided": decided,
            "categories": case_categories[docket_object["ID"]],
            "date": last_event_time,
            "title": docket_object["name"],
            "details_url": docket_object["href"],
            "term": docket_object["term"],
            "description": docket_object["description"],
            "question": docket_object["question"],
        }

    # See above for why this is disabled.
    #merge_with_latest_data(case_summaries, latest_confirmed)

    # Order the cases by date
    sorted_by_time = sorted(
        case_summaries.values(), key=lambda x: x["date"], reverse=True
    )
    cases = []
    for c in sorted_by_time:
        cases.append(case_summaries[c["docket_number"]])

    with open(base_folder / "case_summaries.json", "w") as f:
        json.dump(cases, f, indent=4, default=str)


def merge_with_latest_data(case_summaries, latest_confirmed):
    for case in latest_confirmed:
        # If we already have oyez data for this case, no need to use ours.
        docket_number = case["docket_id"]
        if docket_number in case_summaries:
            continue

        case_summaries[docket_number] = {
            "docket_number": docket_number,
            "date": parse_unix_timestamp_even_negative(case["date_granted"]),
            "title": case["title"],
            "details_url": None,
            "term": case["term"],
            "description": None,
            "question": None,
        }
        print(docket_number)


def download_oyez_data():
    if not OYEZ_DATA_FILE.exists():
        r = requests.get(
            "https://raw.githubusercontent.com/walkerdb/supreme_court_transcripts/master/oyez/case_summaries.json"
        )
        r.raise_for_status()
        with open(OYEZ_DATA_FILE, "w") as f:
            f.write(r.text)

    if not OYEZ_CATEGORY_FILE.exists():
        r = requests.get(
            "https://api.oyez.org/info/case_issues"
        )
        r.raise_for_status()
        with open(OYEZ_CATEGORY_FILE, "w") as f:
            f.write(r.text)


Category = collections.namedtuple('Category', ['id', 'name'])


def crawl_sub_categories(sub_categories, categories):    
    if "children" not in categories:
        return
    for category in categories["children"]:
        crawl_sub_categories(sub_categories, category)
        c = Category(category["id"], category["name"])
        sub_categories.append(c)


def download_single_category(category_id):
    category_file = OYEZ_CATEGORY_FOLDER / "{}.json".format(category_id)
    if category_file.exists():
        with open(category_file, "r") as f:
            cases = json.load(f)
        return cases
    # Hacky throttling
    import time
    time.sleep(0.1)

    cases = []
    r = requests.get("https://api.oyez.org/cases", 
        params={"filter": "issue:{}".format(category_id)}
    )
    print("Downloading ", category_id)
    r.raise_for_status()
    for case in r.json():
        cases.append(case["ID"])
    with open(category_file, "w") as f:
        json.dump(cases, f)
    return cases


def download_and_load_category_data(categories):
    category_ids = []
    cases_to_categories = collections.defaultdict(list)

    for category in categories:
        c = Category(category["id"], category["name"])
        category_ids.append(c)
        crawl_sub_categories(category_ids, category)

    for category in category_ids:
        cases = download_single_category(category.id)
        for case_id in cases:
            cases_to_categories[case_id].append(category.id)

    return category_ids, cases_to_categories


if __name__ == "__main__":
    main()
