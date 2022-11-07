from datetime import datetime
from pprint import pprint

from pyminder.pyminder import Pyminder

USERNAME = "..."  # beeminder username
TOKEN = "..."  # beeminder personal auth token (from https://www.beeminder.com/settings/account#account-permissions)


def setup_pyminder():
    """Sets up a Pyminder instance."""
    pyminder = Pyminder(user=USERNAME, token=TOKEN)
    return pyminder


def get_goal_by_slug(pyminder, slug, debug=False):
    """Returns the goal with the given slug."""
    all_goals = pyminder.get_goals()
    all_goal_slugs = [goal.slug for goal in all_goals]
    assert slug in all_goal_slugs, f"Goal with slug {slug} does not exist."
    slug_matches = [goal for goal in all_goals if goal.slug == slug]
    if debug:
        pprint(f"all_goal_slugs: {all_goal_slugs}")
        slug_matches_slugs = [goal.slug for goal in slug_matches]
        pprint(f"slug_matches_slugs: {slug_matches_slugs}")
    assert (
        len(slug_matches) == 1
    ), f"Found fewer or more than 1 slug_matches: {[g.slug for g in slug_matches]}"
    goal = slug_matches[0]
    return goal


def prepare_datapoint(value, comment):
    """Prepares the datapoint to be posted to Beeminder with value, time, and comment."""
    datapoint = {
        "value": value,
        "time": str(datetime.now()),
        "comment": comment,
    }
    return datapoint


def condense_existing_datapoint(existing_datapoint):
    """Condenses the existing datapoint to a dict with only the relevant information for debugging."""
    condensed_datapoint = {
        "value": existing_datapoint["value"],
        "daystamp": existing_datapoint["daystamp"],
        "comment": existing_datapoint["fulltext"],
    }
    return condensed_datapoint


def get_todays_date():
    """Returns the date in the format YYYYMMDD."""
    date = datetime.now()
    dateformat = "%Y%m%d"
    date = date.strftime(dateformat)
    return date


def get_datapoint_same_day(goal, debug=False):
    """Checks if there is already a datapoint for today
    # if so, return True and the value of the datapoint
    # if not, return False and None
    """
    today = get_todays_date()
    if debug:
        pprint(f"today: {today}")
    existing_datapoints = goal._data["recent_data"]
    if debug:
        pprint(
            f"last 4 existing datapoints: {[condense_existing_datapoint(d) for d in existing_datapoints[:4]]}"
        )
    for datapoint in existing_datapoints:
        if datapoint["daystamp"] == today:
            data_point_exists = True
            value = datapoint["value"]
            return data_point_exists, value
    data_point_exists = False
    value = None
    return data_point_exists, value


def post_datapoint(goal, datapoint):
    """Posts the datapoint to the goal."""
    goal.stage_datapoint(**datapoint)
    goal.commit_datapoints()


def determine_if_overwrite(value, existing_value, overwrite_mode):
    """Depending on the overwrite_mode, and the comparison of the value and existing_value, determines if the datapoint should be overwritten.
    """
    OVERWRITE_SETTINGS = (None, "only_larger", "only_smaller", "always")
    assert (
        overwrite_mode in OVERWRITE_SETTINGS
    ), f"overwrite_mode must be one of {OVERWRITE_SETTINGS}"
    if overwrite_mode == "always":
        overwrite = True
    elif overwrite_mode == "only_larger":
        overwrite = value > existing_value
    elif overwrite_mode == "only_smaller":
        overwrite = value < existing_value
    else:
        overwrite = False
    return overwrite


def post_to_beeminder(slug, value, comment, overwrite_mode=None, debug=False):
    """Posts a datapoint to Beeminder with the given slug, value, and comment. If there is already a datapoint for today, it will be overwritten depending on the overwrite_mode."""
    pyminder = setup_pyminder()
    goal = get_goal_by_slug(pyminder, slug, debug)
    datapoint_exists, existing_value = get_datapoint_same_day(goal, debug)
    overwrite = (
        determine_if_overwrite(value, existing_value, overwrite_mode)
        if datapoint_exists
        else True
    )
    if debug:
        pprint(
            f"datapoint_exists: {datapoint_exists}, existing_value: {existing_value}, overwrite_mode: {overwrite_mode}, overwrite: {overwrite}"
        )
    if not datapoint_exists or overwrite:
        datapoint = prepare_datapoint(value, comment)
        if debug:
            pprint(f"datapoint: {datapoint}")
        post_datapoint(goal, datapoint)
        pprint(f"Posted value {value} to goal {slug} with comment '{comment}'.")
    else:
        pprint(
            f"Datapoint with value {existing_value} already exists for today. Not posting."
        )
