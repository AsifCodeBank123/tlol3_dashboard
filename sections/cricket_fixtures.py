# sections/cricket_fixtures.py
"""
Cricket fixtures — shows redesigned info cards with medallion logos.
Added: LINEUPS data and an inline <details> panel per card to display team lineup.
Local images under assets/teams/... are embedded as data-URIs.
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import mimetypes
import base64
import html

# ----- Fixtures (example) -----------------------------------------------------
FIXTURES = [
    ("Dabangg Dynamos", "Gully Gang"),
    ("Rockstar Rebels", "Badshah Blasters"),
    ("Badshah Blasters", "Dabangg Dynamos"),
    ("Gully Gang", "Rockstar Rebels"),
    ("Rockstar Rebels", "Dabangg Dynamos"),
    ("Gully Gang", "Badshah Blasters"),
]

# ----- Team image mapping (relative to assets/) -------------------------------
TEAM_IMAGES = {
    "Dabangg Dynamos": "teams/dd_logo.png",
    "Gully Gang": "teams/gg_logo.png",
    "Rockstar Rebels": "teams/rr_logo.png",
    "Badshah Blasters": "teams/bb_logo.png",
}

# ----- Lineups (player list from your pasted data) ----------------------------
# Each value is a list of (player_name, role)
LINEUPS = {
    "Badshah Blasters": [
        ("Wilfred Dsilva", "All Rounder"),
        ("Vishal Shinde", "Batsman"),
        ("Saurabh Mahadik", "Batsman"),
        ("Pritesh Menon", "All Rounder"),
        ("Samiksha Prabhu", "Bowler"),
        ("Umesh Gawade", "All Rounder"),
        ("N Pratap Kumar", "Not Available"),
        ("Vijay Chinkate", "Power Hitter"),
        ("Pooja Nandoskar", "Bowler"),
        ("Gayatri Zuting", "Batswoman"),
        ("Hitesh Ghadigaonkar", "Not Available"),
        ("Somansh Datta", "Power Hitter"),
        ("Kiran Padwal", "Batsman"),
    ],
    "Dabangg Dynamos": [
        ("Adnan Shaikh", "Power Hitter"),
        ("Nilesh Sansare", "Tentative"),
        ("Rachita Harit", "Bowler"),
        ("Nilesh Mulik", "Tentative"),
        ("Mayur Pawar", "Power Hitter"),
        ("Bijal Gala", "Bowler"),
        ("Sanskar Bagwe", "Batsman"),
        ("Lalit Chavan", "All Rounder"),
        ("Ravi Khanra", "Tentative"),
        ("Bishal Pandit", "Batsman"),
        ("Arijit Ghosh", "All Rounder"),
        ("Amit Singh", "Power Hitter"),
        ("Amitabh Singh", "Tentative"),
    ],
    "Gully Gang": [
        ("Umesh Tank", "All Rounder"),
        ("Bhaskar Patil", "Batsman"),
        ("Rahul Arjun", "Batsman"),
        ("Avinash Gowda", "Batsman"),
        ("Rahul Pokharkar", "Batsman"),
        ("Avin Chorage", "Not Available"),
        ("Vijay Sangale", "Batsman"),
        ("Jay Jagad", "All Rounder"),
        ("Bhagyashree Dhotre", "Bowler"),
        ("Pramod Patel", "Batsman"),
        ("Komal Panjwani", "Bowler"),
        ("Pritam Paparkar", "Not Available"),
    ],
    "Rockstar Rebels": [
        ("Dhananjay Kulkarni", "Power Hitter"),
        ("Suraj Kamerkar", "All Rounder"),
        ("Kishansingh Devda", "All Rounder"),
        ("Vibhuti S Dabholkar", "Not Available"),
        ("Jincy Geevarghese", "Bowler"),
        ("Arvind Arumuga Nainar", "Batsman"),
        ("Johnson Thomas", "All Rounder"),
        ("Ankit Yadav", "Batsman"),
        ("Irshad Darji", "Batsman"),
        ("Ravi Chavan", "Tentative"),
        ("Sanket Patil", "Tentative"),
        ("Asif Khan", "All Rounder"),
        ("Esakki Shummugavel", "Batswoman"),
        ("Blessen Thomas", "All Rounder"),
    ],
}

# ----- Team taglines & stats placeholders -------------------------------------
TEAM_TAGLINES = {
    "Dabangg Dynamos": "Street smart powerplay",
    "Gully Gang": "Hustle & heart",
    "Rockstar Rebels": "Style with strikes",
    "Badshah Blasters": "Power hitters",
}
TEAM_STATS = {
    "Dabangg Dynamos": (0, 0),
    "Gully Gang": (0, 0),
    "Rockstar Rebels": (0, 0),
    "Badshah Blasters": (0, 0),
}

# ----- Helpers: path resolution -> data URI -----------------------------------
def try_paths_for(local_path: str):
    if not local_path:
        return
    s = str(local_path).replace("\\", "/").strip()
    p = Path(s)
    if p.is_absolute():
        yield p
    if s.startswith("assets/"):
        yield Path.cwd() / s.lstrip("/")
    else:
        yield Path.cwd() / "assets" / s.lstrip("/")
    yield Path.cwd() / s.lstrip("/")
    yield Path(s)


def file_to_data_uri_try(local_path: str):
    if not local_path:
        return None
    for candidate in try_paths_for(local_path):
        try:
            if candidate.exists() and candidate.is_file():
                mime, _ = mimetypes.guess_type(str(candidate))
                mime = mime or "image/png"
                data = candidate.read_bytes()
                b64 = base64.b64encode(data).decode("ascii")
                return f"data:{mime};base64,{b64}"
        except Exception:
            continue
    return None


def resolve_team_image(team_name: str):
    raw = TEAM_IMAGES.get(team_name) or TEAM_IMAGES.get(team_name.strip())
    if not raw:
        return None
    s = str(raw).strip()
    if s.startswith(("http://", "https://", "data:")):
        return s
    return file_to_data_uri_try(s)

# ----- CSS (keeps the newer design, adds styles for lineup details/table) -----
CSS = r"""
:root{
  --card-width: clamp(240px, 32vw, 420px);
  --medal-size: clamp(64px, 12vw, 120px);
  --vs-size: clamp(56px, 8vw, 84px);
  --glass: rgba(255,255,255,0.6);
}

/* container */
.cricket-root { font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; padding: 14px; color:#111; }
.cricket-container { max-width: 1200px; margin: 8px auto; }
.header-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; gap:12px; }

/* matches list */
.matches { display:flex; flex-direction:column; gap:20px; }

/* each match row: left card | vs column | right card */
.match-row {
  display:grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 16px;
  align-items: center;
  padding: 8px 6px;
  position: relative;
}

/* subtle connector line behind vs */
.match-row::before {
  content: "";
  position: absolute;
  left: 8%;
  right: 8%;
  top: 50%;
  height: 1px;
  background: linear-gradient(90deg, rgba(0,0,0,0.04), rgba(0,0,0,0.0), rgba(0,0,0,0.04));
  z-index: 1;
}

/* VS column */
.vs-column { width: var(--vs-size); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; z-index: 6; }
.vs-badge { width: var(--vs-size); height: var(--vs-size); border-radius: 999px; display:flex; align-items:center; justify-content:center; color: #fff; font-weight:800; background: linear-gradient(135deg,#ff7a1a,#ffcf4d); box-shadow: 0 8px 20px rgba(0,0,0,0.14); border: 3px solid rgba(255,255,255,0.14); font-size: clamp(0.72rem, 1.6vw, 0.98rem); z-index: 6; }
.vs-meta { font-size: 0.82rem; color: #666; text-align:center; max-width: 120px; }

/* card: info tile */
.info-card { display:flex; gap:14px; align-items:center; background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(250,250,250,0.95)); border-radius: 12px; box-shadow: 0 12px 30px rgba(12,20,30,0.07); padding: 12px; min-height: 96px; transition: transform .18s ease, box-shadow .18s ease; position: relative; overflow: visible; }
.info-left { width: calc(var(--medal-size) + 12px); display:flex; align-items:center; justify-content:center; position: relative; }
.medallion { width: var(--medal-size); height: var(--medal-size); border-radius: 50%; background: radial-gradient(circle at 30% 25%, #fff 0%, #f3f3f3 60%, #eaeaea 100%); border: 4px solid rgba(255,255,255,0.96); display:flex; align-items:center; justify-content:center; box-shadow: 0 10px 28px rgba(0,0,0,0.12), inset 0 2px 6px rgba(255,255,255,0.7); overflow:hidden; }
.medallion img { width: 70%; height: auto; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.12)); transition: transform .18s ease; }
.info-right { display:flex; flex-direction:column; gap:6px; flex:1; min-width: 0; }
.team-name { font-weight:800; font-size:1.02rem; display:flex; align-items:center; gap:8px; white-space:nowrap; text-overflow: ellipsis; overflow: hidden; }
.team-tag { color:#666; font-size:0.85rem; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.stats-row { display:flex; gap:10px; align-items:center; margin-top:6px; }
.stat { display:flex; flex-direction:column; align-items:center; justify-content:center; min-width:54px; padding:6px 8px; border-radius:8px; background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(250,250,250,0.9)); box-shadow: inset 0 1px 0 rgba(255,255,255,0.6); }
.stat .num { font-weight:800; font-size:0.95rem; }
.stat .label { font-size:0.72rem; color:#666; }
.cta-row { margin-left:auto; display:flex; align-items:center; gap:8px; }
.btn { padding:8px 12px; border-radius:10px; cursor:pointer; border: none; background: linear-gradient(135deg,#0b74ff,#2bb0ff); color:#fff; font-weight:700; font-size:0.85rem; box-shadow: 0 8px 20px rgba(11,116,255,0.16); }
.btn.secondary { background: linear-gradient(135deg,#6b7280,#9aa0a6); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }

/* details / lineup table */
.details-wrap { width: 100%; margin-top: 8px; }
.details-wrap details { width:100%; border-radius:8px; overflow:hidden; background: rgba(250,250,250,0.98); border: 1px solid rgba(0,0,0,0.04); }
.details-wrap summary { padding:8px 12px; cursor:pointer; font-weight:700; background: linear-gradient(180deg, #fff, #fbfbfb); }
.lineup-table { width:100%; border-collapse: collapse; font-size:0.92rem; }
.lineup-table th, .lineup-table td { padding:8px 10px; text-align:left; border-bottom: 1px solid rgba(0,0,0,0.04); }
.lineup-table th { font-size:0.82rem; color:#444; font-weight:800; background: rgba(255,255,255,0.6); }
.lineup-role { color:#666; font-weight:600; font-size:0.88rem; }

/* small metadata row under footer if needed */
.match-meta { margin-top:8px; color:#666; font-size:0.85rem; text-align:center; }

/* separator between matches */
.match-separator { height:1px; width:92%; margin: 8px auto; border-radius:2px; background: linear-gradient(90deg, rgba(0,0,0,0.05), rgba(0,0,0,0.02)); }

/* ---------- Tight mobile compacting: force 2 cards + VS into single view ---------- */
/* Put this after your existing mobile CSS so it overrides sizes where needed */

/* ---------- Small-screen reorder: Team name, tag, icon, stats, lineup ---------- */
/* ---------- Small-screen reorder: Name → Tag → Icon → Stats → Lineup ---------- */
@media (max-width:880px) {

  /* stack elements vertically inside each card */
  .info-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 10px;
  }

  /* text content first */
  .info-right {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
    order: 1; /* first in card */
  }

  .team-name { order: 1; font-size: 1.02rem; line-height: 1.1; font-weight: 800; }
  .team-tag  { order: 2; font-size: 0.90rem; color: #666; margin-bottom: 4px; }

  /* icon (medallion) next, centered visually under text */
  .info-left {
    order: 3;
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 4px 0;
  }
  .medallion {
    --med-size: clamp(46px, 13vw, 82px);
    width: var(--med-size);
    height: var(--med-size);
    border-width: 3px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  }
  .medallion img { width: 66%; height: auto; }

  /* stats come below icon */
  .stats-row {
    order: 3;
    display: flex;
    gap: 8px;
    margin-top: 6px;
    width: 100%;
    justify-content: center; /* center stats row for neat balance */
  }
  .stat {
    min-width: 40px;
    padding: 6px 6px;
    border-radius: 8px;
    background: linear-gradient(180deg, #fff, #fafafa);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
  }
  .stat .num { font-size: 0.86rem; font-weight: 700; }
  .stat .label { font-size: 0.68rem; color: #666; }

  /* lineup details last */
  .details-wrap {
    order: 5;
    width: 100%;
    margin-top: 8px;
  }
  .details-wrap summary {
    padding: 8px 10px;
    font-size: 0.95rem;
    cursor: pointer;
  }
  .lineup-scroll {
    max-height: 180px;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    padding: 6px 2px;
  }
  .lineup-table {
    width: 100%;
    min-width: 0;
    border-collapse: collapse;
  }
  .lineup-table th, .lineup-table td {
    padding: 8px 8px;
    white-space: normal;
    word-break: break-word;
  }

  /* hide CTAs for compact view */
  .cta-row { display: none !important; }

  /* match row tightened so both cards + VS fit on screen */
  .match-row {
    grid-template-columns: minmax(90px,1fr) minmax(44px,64px) minmax(90px,1fr);
    gap: 8px;
    padding: 6px;
  }

  /* smaller separator */
  .match-separator { margin: 8px auto; width: 94%; }
}

/* extra small screen fine-tune */
@media (max-width:480px) {
  .team-name { font-size: 0.70rem; margin-top:8px; }
  .team-tag  { font-size: 0.60rem; margin-top:8px;}
  .medallion { width: clamp(70px, 16vw, 40px); height: clamp(30px, 16vw, 72px); }
  /* shrink lineup table fonts and paddings */
  .lineup-scroll {
    max-height: 140px;                /* shorter block to fit screen */
    padding: 4px 2px 6px 2px;
  }

  .lineup-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.66rem;
  }

  .lineup-table th,
  .lineup-table td {
    padding: 6px 6px;
    white-space: normal;
    word-break: break-word;
  }

  /* visually simplify: hide header, use stacked row style */
  .lineup-table thead { display: none; }

  .lineup-table tbody tr {
    display: block;
    margin-bottom: 6px;
    padding: 4px 6px;
    background: linear-gradient(180deg, #fff, #fafafa);
    border-radius: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }

  .lineup-table tbody tr td {
    display: block;
    border: none;
    padding: 3px 4px;
  }

  /* player name bold, role lighter below */
  .lineup-table tbody tr td:first-child {
    font-weight: 600;
    color: #222;
    margin-bottom: 2px;
  }
  .lineup-table tbody tr td.lineup-role {
    font-weight: 500;
    font-size: 0.70rem;
    color: #555;
  }

  /* smooth scroll and spacing */
  .details-wrap summary {
    padding: 10px 8px;
    font-size: 0.65rem;
    border-radius: 6px;
  }

  /* tighten card for small viewports */
  .info-card {
    padding: 2px;
    gap: 2px;
    min-height: auto;
  }
}
}


"""


# ----- Renderer --------------------------------------------------------------
def render_cricket_fixtures():
    st.title("🏏 Cricket — Round Robin Fixtures (Lineups Included)")
    st.caption("Click 'View Lineup' in Details to expand the player list for each team.")

    parts = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'/>",
        "<style>", CSS, "</style></head><body style='margin:0;padding:0;background:transparent;'>",
        "<div class='cricket-root'><div class='cricket-container'>",
        "<div class='header-row'><h3 style='margin:0'>Round Robin Fixtures</h3><div style='color:#666;font-size:0.9rem'>Lineups available</div></div>",
        "<div class='matches'>"
    ]

    for idx, (team_a, team_b) in enumerate(FIXTURES, start=1):
        img_a = resolve_team_image(team_a)
        img_b = resolve_team_image(team_b)

        def build_lineup_html(team):
            rows = LINEUPS.get(team, [])
            if not rows:
                return "<div style='padding:10px;color:#666'>No lineup available.</div>"
            # table header + rows
            tr_rows = []
            for name, role in rows:
                tr_rows.append(f"<tr><td>{html.escape(name)}</td><td class='lineup-role'>{html.escape(role)}</td></tr>")
            table_html = (
                "<div class='details-wrap'>"
                "<details>"
                "<summary>View Lineup</summary>"
                "<div style='padding:8px 12px'>"
                "<table class='lineup-table'>"
                "<thead><tr><th>Player</th><th>Role</th></tr></thead>"
                "<tbody>"
                + "\n".join(tr_rows) +
                "</tbody></table>"
                "</div>"
                "</details>"
                "</div>"
            )
            return table_html

        def card_html(team, img_src):
            cls = team.lower().replace(" ", "_")
            tagline = html.escape(TEAM_TAGLINES.get(team, "Team"))
            wins, losses = TEAM_STATS.get(team, (0, 0))
            lineup_block = build_lineup_html(team)
            if img_src:
                img_tag = f'<img src="{html.escape(img_src, quote=True)}" alt="{html.escape(team)}" />'
            else:
                img_tag = '<div style="width:64%;height:64%;border-radius:50%;background:linear-gradient(180deg,#eee,#ddd)"></div>'
            return f"""
            <div class="info-card {cls}">
              <div class="info-left">
                <div class="medallion">{img_tag}</div>
              </div>

              <div class="info-right">
                <div class="team-name">{html.escape(team)}</div>
                <div class="team-tag">{tagline}</div>

                <div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;">
                  <div style="display:flex;gap:8px;align-items:center">
                    <div class="stat"><div class="num">{wins}</div><div class="label">W</div></div>
                    <div class="stat"><div class="num">{losses}</div><div class="label">L</div></div>
                  </div>
                  <div class="cta-row">
                    <button class="btn">Details</button>
                    <button class="btn secondary">Lineup</button>
                  </div>
                </div>

                <!-- lineup details -->
                {lineup_block}
              </div>
            </div>
            """

        # VS meta placeholders
        match_time = "3:00 PM"
        venue = "Airoli Turf (2P)"

        parts.append(f"<div class='match-row' data-match='{idx}'>")
        parts.append(card_html(team_a, img_a))
        parts.append(f"""
          <div class="vs-column" role="group" aria-label="versus">
            <div class="vs-badge">VS</div>
            <div class="vs-meta">{html.escape(match_time)}<br/>{html.escape(venue)}</div>
          </div>
        """)
        parts.append(card_html(team_b, img_b))
        parts.append("</div>")  # end match-row

        if idx < len(FIXTURES):
            parts.append("<div class='match-separator' aria-hidden='true'></div>")

    parts.append("</div></div></div></body></html>")
    full = "\n".join(parts)

    approx_height = min(max(520, 320 * len(FIXTURES)), 2600)
    components.html(full, height=approx_height, scrolling=False)


# optional debug helper
def debug_paths():
    st.write("cwd:", Path.cwd())
    for team, path in TEAM_IMAGES.items():
        st.write(team, "->", path)
        for cand in try_paths_for(path):
            st.write("   cand:", cand, "exists:", cand.exists())
