# 🏀 NBA Discord Bot

A Discord bot that provides **NBA live scores, schedules, and player statistics** using official NBA data sources.
Built with **Python** and **discord.py**, the bot follows a **clean, modular architecture** and is suitable for learning, experimentation, and portfolio demonstration.

---

## 📌 Overview
This bot allows Discord users to:
- View live NBA scores
- Check upcoming schedules
- Query historical scoreboards
- Fetch recent player performance with key stats

The project emphasizes:
- Separation of concerns
- Safe handling of secrets
- Extensibility for future features

---

## ✨ Features

### 📊 Scores & Schedules
- Today’s NBA live scores
- Tomorrow’s NBA schedule
- Scoreboard for any date (`YYYY-MM-DD`)
- Automatic **ET → AEDT** time conversion
- Fallback to official season schedule when live data is unavailable

### 🧑‍💻 Player Statistics
- Last **5 games** for any NBA player
- Per-game stats:
  - Win / Loss (W/L)
  - Points (PTS)
  - 3-point shooting (3PM / 3PA / %)
  - Rebounds (REB)
  - Defensive stats (STL, BLK)
- Summary of last-5-game averages

### 🧱 Architecture
- Modular command system
- Dedicated services layer for data access
- Rate-limited HTTP client
- Config isolation (no secrets committed)
- Easy to extend with new commands or APIs

---

## 🧑‍💻 Bot Commands

### NBA Scores & Schedule
- !nba scores
- !nba tomorrow
- !scoreboard YYYY-MM-DD

### Player Stats
- !player LeBron James
- !player Stephen Curry
- !player Luka Doncic

---

## 📂 Project Structure
```bash
NBA_discord_bot/
├── bot.py
├── commands/
│ ├── nba_cmd.py
│ ├── scoreboard_cmd.py
│ ├── player_cmd.py
│ └── init.py
├── services/
│ ├── nba_data.py
│ ├── http_client.py
│ ├── timezones.py
│ └── init.py
├── config.example.py
├── .gitignore
├── LICENSE
├── README.md

```


## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
```bash
git clone https://github.com/Hrithik028/NBA-discord-bot.git
cd NBA_discord_bot
```
2️⃣ Create a virtual environment
```bash
python -m venv venv
Activate it:

.\venv\Scripts\Activate.ps1
Git Bash

source venv/Scripts/activate
```
3️⃣ Install dependencies
```bash
pip install discord.py nba_api requests pytz
(Optional)
pip freeze > requirements.txt
```
## 🔐 Configuration (Required)

4️⃣ Create a local config file
```bash
cp config.example.py config.py
```
5️⃣ Edit config.py
```bash
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
COMMAND_PREFIX = "!"
```
⚠️ Never commit config.py
It is excluded via .gitignore to protect your Discord token.

▶️ Running the Bot
```bash
python bot.py
Successful startup:

✅ Logged in as <your-bot-name>
```
---

📦 Data Sources
- Official NBA JSON endpoints
- stats.nba.com (via nba_api)
- NBA season schedule feeds
- All data is read-only and publicly accessible.

🔒 Security Notes
- No secrets are committed to the repository
- config.py is ignored via .gitignore
- Safe to host publicly on GitHub
- Tokens should be rotated if ever exposed

🧪 Troubleshooting
- Bot does not start
- Ensure the virtual environment is activated
- Confirm dependencies are installed
- Verify DISCORD_TOKEN is set correctly
- Commands not responding
- Ensure the bot has Message Content Intent enabled in Discord Developer Portal
- Confirm command prefix matches COMMAND_PREFIX

API errors
- NBA endpoints may temporarily restrict access
- The bot automatically falls back to schedule data when possible

🤝 Contributing
This is a personal/learning project, but contributions are welcome.
- Suggested workflow:
- Fork the repository
- Create a feature branch
- Commit changes
- Open a Pull Request

📜 License
- This project is licensed under the MIT License.
- You are free to use, modify, and distribute it with attribution.

👤 Author
- Hrithik Jadhav
- Built as a learning and portfolio project using official NBA data.
