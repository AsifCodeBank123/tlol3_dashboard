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
                    team1_pct, team2_pct,
                    has_voted=False, voted_abbr=None):

    abbr1 = TEAM_ABBR.get(team1.strip().replace(" 🏆", "").replace(" 🦆", ""), team1[:2].upper())
    abbr2 = TEAM_ABBR.get(team2.strip().replace(" 🏆", "").replace(" 🦆", ""), team2[:2].upper())

    p1 = " & ".join(players1) if players1 else "TBD"
    p2 = " & ".join(players2) if players2 else "TBD"

    show_logo1 = team1_logo if os.path.exists(team1_logo) else "assets/tbd_logo.png"
    show_logo2 = team2_logo if os.path.exists(team2_logo) else "assets/tbd_logo.png"

    if "🏆" in team1:
        show_logo1 = "assets/winner.png"
    elif "🦆" in team1:
        show_logo1 = "assets/blnt.jpg"
    if "🏆" in team2:
        show_logo2 = "assets/winner.png"
    elif "🦆" in team2:
        show_logo2 = "assets/blnt.png"

    logo1_b64 = encode_image(show_logo1)
    logo2_b64 = encode_image(show_logo2)

    html = f"""
    <div class="match-card">
      <div class="match-title">{title}</div>
      <div style="display:flex; justify-content:space-between; align-items:stretch;">
        <div class="team-box">
          <div class="team-flex">
            <img src="{logo1_b64}" class="team-img" />
            <div class="team-abbr">{abbr1} ({team1_pct}%)</div>
          </div>
          <div class="team-name">{team1}</div>
          <div class="player-names">{p1}</div>
        </div>
        <div class="match-versus">⚔️</div>
        <div class="team-box">
          <div class="team-flex">
            <img src="{logo2_b64}" class="team-img" />
            <div class="team-abbr">{abbr2} ({team2_pct}%)</div>
          </div>
          <div class="team-name">{team2}</div>
          <div class="player-names">{p2}</div>
        </div>
      </div>
    </div>
    """
    return html
