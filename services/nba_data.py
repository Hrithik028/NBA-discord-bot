from datetime import date
from typing import Dict, Any
from services.http_client import limited_get, safe_json

SCHEDULE_CACHE: Dict[int, Dict[str, Any]] = {}


def season_start_year_for_date(d: date) -> int:
    # Aug–Dec => season starts this year, Jan–Jul => previous year
    return d.year if d.month >= 8 else d.year - 1


def get_full_schedule_for_year(season_start_year: int) -> Dict[str, Any]:
    if season_start_year in SCHEDULE_CACHE:
        return SCHEDULE_CACHE[season_start_year]

    url = (
        "https://data.nba.com/data/10s/v2015/json/mobile_teams/"
        f"nba/{season_start_year}/league/00_full_schedule.json"
    )
    resp = limited_get(url)
    data = safe_json(resp, log_prefix=f"FULL_SCHEDULE_{season_start_year}")
    if data:
        SCHEDULE_CACHE[season_start_year] = data
    return data


def get_scoreboard_today() -> Dict[str, Any]:
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    resp = limited_get(url)
    return safe_json(resp, log_prefix="TODAY_SCOREBOARD")


def get_scoreboard_for_date(d: date) -> Dict[str, Any]:
    datestr = d.strftime("%Y%m%d")
    url = f"https://cdn.nba.com/static/json/liveData/scoreboard/scoreboard_{datestr}.json"
    resp = limited_get(url)
    return safe_json(resp, log_prefix=f"DATE_SCOREBOARD_{datestr}")
