#!/usr/bin/env python3
import re
import os
import sys 
from argparse import ArgumentParser

def is_merge_request():
    return "CI_MERGE_REQUEST_ID" in os.environ

def get_merge_request_title():
    return os.environ.get("CI_MERGE_REQUEST_TITLE")

def check_pr_title(title_regexp):
    if not is_merge_request():
        print("Not a merge request - Skipping")
        return 0

    title = get_merge_request_title()
    if title.startswith("Draft:") or title.startswith("WIP:"):
        print("Merge request is a draft - Skipping")
        return 0

    if not re.match(title_regexp, title):
        print(f"Merge request title '{title}' does not match the format '{title_regexp}'")
        return 1

    return 0


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--format", required=True, help="Regular used to verify the merge request title")
    options = parser.parse_args()

    sys.exit(check_pr_title(options.format))
