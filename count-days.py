import argparse
from datetime import date, datetime

"""
A simple script that computes the difference in days between two dates.

Arguments:
--start: start date, defaults to current date if not provided.
--end: end date, defaults to current date if not provided.
--format: format of both start and end date, by default %Y%m%d is used, see
https://docs.python.org/3/library/datetime.html#format-codes for further info.
--message: message that will be printed.
--placeholder: piece of text in output message that will be replaced by days difference.
"""


# given two dates, compute difference in days (will be negative if end is before start)
def compute_days_difference(start_date_string, end_date_string, dates_format):
    # set start/end date as current date if not provided
    if start_date_string:
        start_date = datetime.strptime(start_date_string, dates_format).date()
    else:
        start_date = date.today()
    if end_date_string:
        end_date = datetime.strptime(end_date_string, dates_format).date()
    else:
        end_date = date.today()
    # return difference in days
    return (end_date - start_date).days


# main function
def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="")
    parser.add_argument("--end", default="")
    parser.add_argument("--format", default="%Y%m%d")
    parser.add_argument("--message", default="Difference in days is <>")
    parser.add_argument("--placeholder", default="<>")
    args = parser.parse_args()
    # compute difference
    days_difference = compute_days_difference(args.start, args.end, args.format)
    print(args.message.replace(args.placeholder, str(days_difference)))


# invoke main function
if __name__ == "__main__":
    main()
