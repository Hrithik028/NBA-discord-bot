import discord
from discord.ext import commands
from datetime import datetime
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from services.nba_data import season_start_year_for_date


def setup_player_commands(bot: commands.Bot):

    @commands.cooldown(1, 10, commands.BucketType.user)
    @bot.command()
    async def player(ctx, *, name: str):
        await ctx.send(f"📊 Fetching last 5 games for **{name}**...")

        plist = players.find_players_by_full_name(name)
        if not plist:
            return await ctx.send(f"❌ Could not find player '{name}'. Check spelling.")

        pid = plist[0]["id"]
        pname = plist[0]["full_name"]

        today = datetime.today().date()
        season_year = season_start_year_for_date(today)
        season_str = f"{season_year}-{str(season_year + 1)[-2:]}"

        try:
            gl = playergamelog.PlayerGameLog(player_id=pid, season=season_str)
            df = gl.get_data_frames()[0]

            if df.empty:
                return await ctx.send(f"No games found for {pname} in season {season_str}.")

            last5 = df.head(5).copy()

            # ---- Last 5 averages ----
            avg_pts = float(last5["PTS"].mean())
            avg_reb = float(last5["REB"].mean())
            avg_stl = float(last5["STL"].mean())
            avg_blk = float(last5["BLK"].mean())

            total_3pm = int(last5["FG3M"].sum())
            total_3pa = int(last5["FG3A"].sum())
            avg_3p_pct = (total_3pm / total_3pa * 100.0) if total_3pa > 0 else None

            # W/L record last 5
            wins = int((last5["WL"] == "W").sum())
            losses = int((last5["WL"] == "L").sum())

            header_lines = [
                f"**Last 5 summary:** {wins}-{losses}",
                f"**Averages:** {avg_pts:.1f} PTS | {avg_reb:.1f} REB | {avg_stl:.1f} STL | {avg_blk:.1f} BLK",
            ]
            if avg_3p_pct is not None:
                header_lines.append(f"**3PT (last 5):** {total_3pm}/{total_3pa} ({avg_3p_pct:.1f}%)")
            else:
                header_lines.append("**3PT (last 5):** —")

            desc = "\n".join(header_lines) + "\n\n"

            # ---- Per-game lines ----
            for _, row in last5.iterrows():
                gd = row["GAME_DATE"]
                matchup = row["MATCHUP"]
                wl = row["WL"]  # W or L

                pts = int(row["PTS"])
                reb = int(row["REB"])
                stl = int(row["STL"])
                blk = int(row["BLK"])

                fg3m = int(row["FG3M"])
                fg3a = int(row["FG3A"])
                fg3p = float(row["FG3_PCT"]) if row["FG3A"] > 0 else None
                fg3p_display = f"{fg3p * 100:.1f}%" if fg3p is not None else "—"

                desc += (
                    f"**{gd}** ({matchup}) — **{wl}**\n"
                    f"PTS: {pts} | 3PT: {fg3m}/{fg3a} ({fg3p_display})\n"
                    f"REB: {reb} | STL: {stl} | BLK: {blk}\n\n"
                )

            embed = discord.Embed(
                title=f"{pname} — last 5 games ({season_str})",
                description=desc,
                color=0x1D428A
            )
            await ctx.send(embed=embed)

        except Exception as e:
            print(f"[PLAYER ERROR] {e}")
            await ctx.send("⚠️ Error fetching player data. Try again later.")

