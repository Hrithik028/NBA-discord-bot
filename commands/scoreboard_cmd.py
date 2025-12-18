from discord.ext import commands
from datetime import datetime
from services.nba_data import get_scoreboard_for_date, get_full_schedule_for_year, season_start_year_for_date
from services.timezones import convert_et_to_aedt


def setup_scoreboard_commands(bot: commands.Bot):

    @bot.command()
    async def scoreboard(ctx, date_str: str):
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return await ctx.send("❌ Invalid date. Use `YYYY-MM-DD`.")

        await ctx.send(f"📅 Fetching NBA games for **{date_str}**...")

        today = datetime.today().date()
        delta_days = (today - target_date).days
        lines = []

        # Recent window: try date-scoreboard JSON first (may be blocked)
        if -1 <= delta_days <= 10:
            data = get_scoreboard_for_date(target_date)
            games = data.get("scoreboard", {}).get("games", [])
            if games:
                for g in games:
                    h = g["homeTeam"]["teamTricode"]
                    a = g["awayTeam"]["teamTricode"]
                    hs = g["homeTeam"]["score"]
                    as_ = g["awayTeam"]["score"]
                    status = convert_et_to_aedt(target_date, g["gameStatusText"])
                    lines.append(f"{a} {as_} @ {h} {hs} — {status}")

        # Fallback: full schedule (no scores, just times/status)
        if not lines:
            season_year = season_start_year_for_date(target_date)
            schedule = get_full_schedule_for_year(season_year)
            if not schedule:
                return await ctx.send(f"⚠️ Could not load schedule for season starting {season_year}.")

            for month in schedule.get("lscd", []):
                mdata = month.get("mscd", {})
                for g in (mdata.get("g") or []):
                    if g.get("gdte") != date_str:
                        continue

                    stt = convert_et_to_aedt(target_date, g.get("stt", "TBD"))
                    h = g.get("h", {})
                    v = g.get("v", {})

                    h_tri = h.get("ta", "???")
                    h_name = h.get("tn", h_tri)
                    v_tri = v.get("ta", "???")
                    v_name = v.get("tn", v_tri)

                    lines.append(f"{v_tri} ({v_name}) @ {h_tri} ({h_name}) — {stt}")

        if not lines:
            return await ctx.send(f"No games found on **{date_str}**.")

        await ctx.send("\n".join(lines))
