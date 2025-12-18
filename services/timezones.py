import pytz
from datetime import datetime, date


def convert_et_to_aedt(date_obj: date, status_str: str) -> str:
    """
    Convert '7:30 pm ET' -> '11:30 AM AEDT' based on the date.
    If it’s not an ET time (e.g., 'Final'), return unchanged.
    """
    if "et" not in status_str.lower():
        return status_str

    try:
        tclean = status_str.lower().replace("et", "").strip()
        dt_time = datetime.strptime(tclean, "%I:%M %p").time()
        naive_dt = datetime.combine(date_obj, dt_time)

        et_tz = pytz.timezone("America/New_York")
        dt_et = et_tz.localize(naive_dt)

        syd_tz = pytz.timezone("Australia/Sydney")
        dt_syd = dt_et.astimezone(syd_tz)

        out = dt_syd.strftime("%I:%M %p").lstrip("0") + " AEDT"
        return out
    except Exception as e:
        print(f"[TIME CONVERT ERROR] {status_str} on {date_obj}: {e}")
        return status_str
