# html_blocks.py/utils
import os
import base64
from utils.constants import TEAM_ABBR, TEAM_LOGOS

def encode_image(path):
    if path and os.path.exists(path):
        with open(path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""

def build_card_html(title, team1, players1, team2, players2,
                    team1_logo, team2_logo,
                    result1="", result2=""):

    # Team abbreviations
    abbr1 = TEAM_ABBR.get(team1.strip().replace(" 🏆", ""), team1[:2].upper())
    abbr2 = TEAM_ABBR.get(team2.strip().replace(" 🏆", ""), team2[:2].upper())

    # Player names
    p1 = "<br>".join(players1) if players1 else "TBD"
    p2 = "<br>".join(players2) if players2 else "TBD"

    # Logos
    show_logo1 = team1_logo if os.path.exists(team1_logo) else "assets/tbd_logo.png"
    show_logo2 = team2_logo if os.path.exists(team2_logo) else "assets/tbd_logo.png"

    if result1.lower() == "w":
        team1 += " 🏆"
        show_logo1 = "assets/winner.png"
    if result2.lower() == "w":
        team2 += " 🏆"
        show_logo2 = "assets/winner.png"

    logo1_b64 = encode_image(show_logo1)
    logo2_b64 = encode_image(show_logo2)

    html = f"""
    <div class="match-card">
      <div class="match-title">{title}</div>
      <div style="display:flex; justify-content:space-between; align-items:stretch;">
        <div class="team-box {'winner' if result1.lower()=='w' else ''}">
          <div class="team-flex">
            <img src="{logo1_b64}" class="team-img" />
            <div class="team-abbr">{abbr1}</div>
          </div>
          <div class="team-name">{team1}</div>
          <div class="player-names">{p1}</div>
        </div>
        <div class="match-versus">⚔️</div>
        <div class="team-box {'winner' if result2.lower()=='w' else ''}">
          <div class="team-flex">
            <img src="{logo2_b64}" class="team-img" />
            <div class="team-abbr">{abbr2}</div>
          </div>
          <div class="team-name">{team2}</div>
          <div class="player-names">{p2}</div>
        </div>
      </div>
    </div>
    """
    return html
