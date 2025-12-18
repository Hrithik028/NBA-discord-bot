from discord.ext import commands
from datetime import datetime, timedelta
from services.nba_data import get_scoreboard_today, get_scoreboard_for_date, get_full_schedule_for_year, season_start_year_for_date
from services.timezones import convert_et_to_aedt


def setup_nba_commands(bot: commands.Bot):

    @bot.command()
    async def nba(ctx, arg: str = None):
        if arg is None:
            return await ctx.send("Usage: `!nba scores` or `!nba tomorrow`")

        arg = arg.lower()

        if arg == "scores":
            await ctx.send("🏀 Fetching today's NBA games...")
            data = get_scoreboard_today()
            games = data.get("scoreboard", {}).get("games", [])

            if not games:
                return await ctx.send("No games today.")

            lines = []
            today = datetime.today().date()
            for g in games:
                h = g["homeTeam"]["teamTricode"]
                a = g["awayTeam"]["teamTricode"]
                hs = g["homeTeam"]["score"]
                as_ = g["awayTeam"]["score"]
                status = convert_et_to_aedt(today, g["gameStatusText"])
                lines.append(f"{a} {as_} @ {h} {hs} — {status}")

            return await ctx.send("\n".join(lines))

        if arg == "tomorrow":
            await ctx.send("📆 Fetching tomorrow's NBA schedule...")
            tomorrow = datetime.today().date() + timedelta(days=1)

            sb = get_scoreboard_for_date(tomorrow)
            games = sb.get("scoreboard", {}).get("games", [])

            lines = []
            if games:
                for g in games:
                    h = g["homeTeam"]["teamTricode"]
                    a = g["awayTeam"]["teamTricode"]
                    status = convert_et_to_aedt(tomorrow, g["gameStatusText"])
                    lines.append(f"{a} @ {h} — {status}")
            else:
                season_year = season_start_year_for_date(tomorrow)
                schedule = get_full_schedule_for_year(season_year)
                if not schedule:
                    return await ctx.send("Could not load schedule.")

                for month in schedule.get("lscd", []):
                    mdata = month.get("mscd", {})
                    for g in (mdata.get("g") or []):
                        if g.get("gdte") != tomorrow.strftime("%Y-%m-%d"):
                            continue
                        h = g.get("h", {})
                        v = g.get("v", {})
                        stt = convert_et_to_aedt(tomorrow, g.get("stt", "TBD"))
                        lines.append(f"{v.get('ta','???')} @ {h.get('ta','???')} — {stt}")

            if not lines:
                return await ctx.send("No games tomorrow.")
            return await ctx.send("\n".join(lines))

        return await ctx.send("Usage: `!nba scores` or `!nba tomorrow`")
