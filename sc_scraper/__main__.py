from pathlib import Path
import requests
import json
from datetime import datetime, timedelta


def parse_unix_timestamp_even_negative(timestamp):
    # Needed because windows can't natively handle negative timestamps :|
    return datetime(1970, 1, 1) + timedelta(seconds=timestamp)


def main():
    base_folder = Path(__file__) / ".." / ".."

    oyez_data_file = base_folder / "oyez_data.json"
    if not oyez_data_file.exists():
        download_oyez_data(oyez_data_file)

    with open(oyez_data_file, "r") as f:
        oyez_data = json.load(f)
    with open(base_folder / "cases.json", "r") as f:
        latest_confirmed = json.load(f)

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

        case_summaries[docket_number] = {
            "docket_number": docket_object["docket_number"],
            "date": last_event_time,
            "title": docket_object["name"],
            "details_url": docket_object["href"],
            "term": docket_object["term"],
            "description": docket_object["description"],
            "question": docket_object["question"],
        }

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

    # Order the cases by date
    sorted_by_time = sorted(
        case_summaries.values(), key=lambda x: x["date"], reverse=True
    )
    cases = []
    for c in sorted_by_time:
        cases.append(case_summaries[c["docket_number"]])

    with open(base_folder / "case_summaries.json", "w") as f:
        json.dump(cases, f, indent=4, default=str)


def download_oyez_data(file_to_save_to):
    r = requests.get(
        "https://raw.githubusercontent.com/walkerdb/supreme_court_transcripts/master/oyez/case_summaries.json"
    )
    r.raise_for_status()

    with open(file_to_save_to, "w") as f:
        f.write(r.text)


if __name__ == "__main__":
    main()
