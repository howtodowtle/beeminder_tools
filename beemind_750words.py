#!/usr/bin/env python3

import re
from datetime import datetime

from install_if_na import install_packages_if_not_installed
from post_to_beeminder import post_to_beeminder

install_packages_if_not_installed(["requests", "pyminder"], debug=False)


SIGNIN_URL = "https://750words.com/auth/signin"
EMAIL = "..."  # 750 words email
PASSWORD = "..."  # 750 words password


def login(url, email, password):
    """Logs in to url with email and password. Returns the logged in session."""
    import requests  # importing here because it needs to be after 'install_packages_if_not_installed' is called

    session = requests.Session()
    payload = {
        "person[email_address]": email,
        "person[password]": password,
    }
    _ = session.post(url, data=payload)
    session.headers.update()
    return session


def find_current_year_and_month():
    """Finds the current year and month and returns them as a tuple."""
    now = datetime.now()
    return now.year, now.month


def find_this_month_url():
    """Finds the url for the 'this month' page and returns it."""
    year, month = find_current_year_and_month()
    return f"https://750words.com/statistics/{year}/{str(month).zfill(2)}"


def get_stats(session):
    """Gets the response/contents of the 'this month' page."""
    res = session.get(find_this_month_url())
    res.raise_for_status()
    return res


def get_completed_pages(res):
    """Finds the number of completed pages in the response/contents of the 'this month' page.
    # find this pattern:
    # userProperties.num_completed_entries = "296";
    # and return the number of pages (296)
    """
    pattern = r"userProperties.num_completed_entries = \"(\d+)\";"
    match = re.search(pattern, res.text)
    return int(match.group(1))


def login_and_get_completed_pages():
    """Logs into 750words.com and returns the number of completed pages."""
    session = login(SIGNIN_URL, EMAIL, PASSWORD)
    res = get_stats(session)
    return get_completed_pages(res)


def prepare_data():
    """Prepares the data to be posted to beeminder."""
    slug = "750"
    value = login_and_get_completed_pages()
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = f"posted via API (t: {time}), code/beeminder/..."
    return slug, value, comment


if __name__ == "__main__":
    post_to_beeminder(*prepare_data(), overwrite_mode="only_larger")
