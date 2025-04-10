import argparse
from datetime import date, datetime, timedelta

"""
A simple script that can add/subtract days to a date or compute a difference in days between two dates.

Arguments used to add/subtract days to a date:
--start: start date, defaults to current date if not provided.
--diff: number of days to add (if negative will be subtracted).

Arguments to compute difference in days between two dates:
--start: start date, defaults to current date if not provided.
--end: end date, defaults to current date if not provided.

Common arguments:
--format: format of dates, by default %Y%m%d is used, see
https://docs.python.org/3/library/datetime.html#format-codes for further info.
--message: message that will be printed.
--placeholder: piece of text in output message that will be replaced by desired information.
"""


# parse a string to obtain a date, returning current date if input string is null or empty
def parse_date_string(date_string, date_format):
    if date_string:
        parsed_date = datetime.strptime(date_string, date_format).date()
    else:
        parsed_date = date.today()
    return parsed_date


# given two dates, compute difference in days (will be negative if end is before start)
def compute_days_difference(start_date_string, end_date_string, date_format):
    # parse start and end date
    start_date = parse_date_string(start_date_string, date_format)
    end_date = parse_date_string(end_date_string, date_format)
    # return difference in days
    return (end_date - start_date).days


# given a date, add/subtract specified number of days
def add_days(start_date_string, date_format, days):
    start_date = parse_date_string(start_date_string, date_format)
    new_date = start_date + timedelta(days=days)
    new_date_string = new_date.strftime(date_format)
    return new_date_string


# print a message replacing placeholder string with desired infomation
def print_message(message, default_message, placeholder, replacement):
    if not message:
        message = default_message
    print(message.replace(placeholder, replacement))


# main function
def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="")
    parser.add_argument("--diff", default="")
    parser.add_argument("--end", default="")
    parser.add_argument("--message", default="")
    parser.add_argument("--placeholder", default="<>")
    parser.add_argument("--format", default="%Y%m%d")
    args = parser.parse_args()
    # add/subtract days if requested
    if args.diff:
        new_date = add_days(args.start, args.format, int(args.diff))
        print_message(args.message, "Computed date is <>", args.placeholder, new_date)
    # compute difference if requested
    else:
        days_difference = compute_days_difference(args.start, args.end, args.format)
        print_message(
            args.message,
            "Difference in days is <>",
            args.placeholder,
            str(days_difference),
        )


# invoke main function
if __name__ == "__main__":
    main()
